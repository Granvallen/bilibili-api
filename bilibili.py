# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17  16:34:00 2018

@author: Granvallen
"""
from support import *
from biclass import *
from danmaku2ass import Danmaku2ASS
from xml.dom.minidom import parseString
import logging

# 常量定义 #

# 排序方式 #
# 综合
# TYPE_ZONGHE = 'totalrank'
# 收藏
TYPE_SHOUCANG = 'stow'
# 评论数
TYPE_PINGLUN = 'scores'
# 播放数 
TYPE_BOFANG = 'click' # 也可以使用 'hot'
# 硬币数
TYPE_YINGBI = 'coin'
# 弹幕数
TYPE_DANMU = 'dm'
# 投稿时间 在给定时段内从新到旧排列 
TYPE_TOUGAO = 'pubdate'


# b站分区代号
bilizone = {
    0 : [0, 1, 13, 167, 3, 129, 4, 36, 160, 119, 155, 165, 5, 181, 177, 23, 11],
    1 : [24, 25, 47],
    13 : [33, 32, 51, 152],
    167 : [153, 168, 169, 170],
    3 : [28, 31, 30, 59, 29, 54, 130],
    129 : [20, 154, 156],
    4 : [17, 171, 172, 65, 173, 121, 136, 19],
    36 : [124, 122, 39, 96, 95, 98, 176],
    160 : [138, 21, 76, 75, 161, 162, 163, 174],
    119 : [22, 26, 126, 127],
    155 : [157, 158, 164, 159],
    165 : [166],
    5 : [71, 137, 131],
    181 : [182, 183, 85, 184, 86],
    177 : [37, 178, 179, 180],
    23 : [147, 145, 146, 83],
    11 : [185, 187]
}

# 常量定义结束 #

def getHotVideo(begintime, endtime, tid=33, sortType=TYPE_BOFANG, page=1, pagesize=20, original=False):
    """
    功能:
        获取各区热门视频排行榜(默认获取新番区tid=33)
    输入: 
        begintime: 起始时间, 三元数组[year1, month1, day1] 如 [2018, 8, 2]
        endtime: 终止时间, 三元数组[year2, month2, day2]
        sortType: 字符串, 排序方式, 参照TYPE_开头的常量
        tid: 整数, 投稿子分区代号(二级分区的序号), 参照文档说明
        page: 整数, 页数, 默认1
        pagesize: 单页拉取的视频数, 默认是20, 上限100
    返回: 
        1.视频列表, 列表中的Video类包含AV号, 标题, 观看数, 收藏数, 弹幕数, 投稿日期, 封面, UP的id号和名字, tag, 视频描述, 视频地址, 评论数等, 具体见参考文档
        *2.实际爬取的b站排行页面url, 便于查错, 可以使用'_'不接收该返回值
    备注: 
        1.时间间隔应小于3个月
        2.这个api无论是否为搜索番剧区返回的信息格式都相同, 故没有区分是Video还是Episode, 都使用了Video类
        3.这个搜索视频的api只能用  二级分区代号
    """
    #判断是否原创
    if original:
        ori1 = '&copy_right=1'
        ori2 = '&original=true'
    else:
        ori1 = '&copy_right=-1'
        ori2 = ''

    url1 = 'https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&pic_size=160x100&cate_id={0}&order={1}&time_from={2[0]}{2[1]:0>2}{2[2]:0>2}&time_to={3[0]}{3[1]:0>2}{3[2]:0>2}&page={4}&pagesize={5}{6}'.format(tid, sortType, begintime, endtime, page, pagesize, ori1)

    # url1 = 'https://api.bilibili.com/archive_rank/getarchiverankbypartion?&type=jsonp&tid={0}&pn={1}{2}'.format(tid, page, ori1)

    url2 = 'https://www.bilibili.com/list/rank-{0}.html#!&order={1}&range={2[0]}-{2[1]:0>2}-{2[2]:0>2}%2C{3[0]}-{3[1]:0>2}-{3[2]:0>2}&page={4}{5}'.format(tid, sortType, begintime, endtime, page, ori2)
    jsoninfo = JsonInfo(getURLContent(url1))
    VideoList = []
    if jsoninfo.error:
        return VideoList, url2
    for video_idx in iter(jsoninfo['result']):
        video = Video(video_idx['id'], video_idx['title'])
        video.play = video_idx['play']
        video.desc = video_idx['description']
        video.pubdate = video_idx['pubdate']
        video.review = video_idx['review']
        video.pic = video_idx['pic']
        video.mid = video_idx['mid']
        video.arcurl = video_idx['arcurl']
        video.tag = video_idx['tag'].split(',')
        video.danmaku = video_idx['video_review']
        video.author = video_idx['author']
        video.favorites = video_idx['favorites']
        video.duration = num2duration(video_idx['duration'])
        video.type = video_idx['type']
        VideoList.append(video)
    return VideoList, url2

def getVideoInfo(aid, pid=1):
    """
    功能:
        由av号获取视频信息
    输入: 
        aid: av号
        pid: 分p号, 对于番剧没有分p, 一个av号对应一集
    返回:
        视频类Video 或 剧集类Episode 注意两个类的属性有所不同
        若视频不存在则返回None
    """
    url1 = 'https://www.bilibili.com/video/av{0}/?p={1}'.format(aid, pid)
    content = getURLContent(url1)
    VideoInfo = getREsearch(content, r'<script>window.__INITIAL_STATE__=({.*});\(')
    if VideoInfo:
        VideoInfo = VideoInfo.group(1)
    else:
        print('正则表达式寻找视频信息失败(')
        return None
    jsoninfo = JsonInfo(VideoInfo)
    if jsoninfo.error:
        return None

    if 'aid' in jsoninfo.keys(): # 判断一下是不是番剧
        # 非番剧
        video = Video(aid)
        video.tid = jsoninfo['videoData', 'tid']
        video.videos = jsoninfo['videoData', 'videos']
        video.pid = pid if pid <= video.videos else 1
        video.tname = jsoninfo['videoData', 'tname']
        video.pic = jsoninfo['videoData', 'pic']
        video.title = jsoninfo['videoData', 'title']
        video.pubdate = num2time(jsoninfo['videoData', 'pubdate']) # 看下这里pubtime有没有可能为字符串 否则处理错误
        video.ctime = num2time(jsoninfo['videoData', 'ctime'])
        video.desc = jsoninfo['videoData', 'desc']
        video.state = jsoninfo['videoData', 'state']
        video.attribute = jsoninfo['videoData', 'attribute']
        video.duration = num2duration(jsoninfo['videoData', 'pages'][video.pid-1]['duration'])
        video.mid = jsoninfo['videoData', 'owner', 'mid']
        video.face = jsoninfo['videoData', 'owner', 'face']
        video.name = jsoninfo['videoData', 'owner', 'name']
        video.dislike = jsoninfo['videoData', 'stat', 'dislike']
        video.cid = jsoninfo['videoData', 'pages'][video.pid-1]['cid'] # 提示错误 不明 运行没问题
        video.tag = []
        for tag in iter(jsoninfo['tags']):
            video.tag.append(tag['tag_name'])
        # 获取视频热度信息 播放量 硬币 收藏 评论 分享 弹幕
        jsoninfo = getVideoStat(video.aid)
        video.play = jsoninfo['view']
        video.danmaku = jsoninfo['danmaku']
        video.review = jsoninfo['reply']
        video.favorite = jsoninfo['favorite']
        video.coin = jsoninfo['coin']
        video.share = jsoninfo['share']
        video.like = jsoninfo['like']
        video.now_rank = jsoninfo['now_rank']
        video.his_rank = jsoninfo['his_rank']
        video.copyright = jsoninfo['copyright']
        # 获取当前观看人数
        video.online_count = getOnlineCount(video.aid, video.cid)
        video.arcurl = getREsub(url1, str(video.pid), r'(\d+)$') if pid > 1 else 'https://www.bilibili.com/video/av{0}/'.format(aid) # 视频地址 处理输入错误的pid
        video.srcurl = getVideoSrcurl(video.cid)
        return video
    else:
        # 番剧
        episode = Episode(aid)
        episode.cover = jsoninfo['epInfo', 'cover']
        episode.title = jsoninfo['mediaInfo', 'title']
        episode.index_title = jsoninfo['epInfo', 'index_title']
        episode.index = jsoninfo['epInfo', 'index']
        episode.pub_real_time = jsoninfo['epInfo', 'pub_real_time'] # 看下这里pubtime有没有可能为字符串
        # 新版返回的api返回的json中没有视频时长信息 只能通过解析xml方式获得
        # episode.duration = num2duration(jsoninfo['epInfo', 'duration'] // 1000)
        episode.mid = jsoninfo['epInfo', 'mid']
        episode.cid = jsoninfo['epInfo', 'cid']
        episode.media_id = jsoninfo['mediaInfo', 'media_id']
        episode.episode_status = jsoninfo['epInfo', 'episode_status']
        episode.ep_id = jsoninfo['epInfo', 'ep_id']
        episode.vid = jsoninfo['epInfo', 'vid']
        # 获取剧集热度信息 播放量 硬币 收藏 评论 分享 弹幕   这是单一剧集的热度 而不是整个番剧的
        jsoninfo = getVideoStat(episode.aid)
        episode.play = jsoninfo['view']
        episode.danmaku = jsoninfo['danmaku']
        episode.review = jsoninfo['reply']
        episode.favorite = jsoninfo['favorite']
        episode.coin = jsoninfo['coin']
        episode.share = jsoninfo['share']
        episode.like = jsoninfo['like']
        episode.now_rank = jsoninfo['now_rank']
        episode.his_rank = jsoninfo['his_rank']
        episode.copyright = jsoninfo['copyright']
        # 获取当前观看人数
        episode.online_count = getOnlineCount(episode.aid, episode.cid)
        episode.link = 'https://www.bilibili.com/bangumi/play/ep{0}'.format(episode.ep_id)
        episode.srcurl = getEpisodeSrcurl(episode.cid)
        return episode

def biliVideoSearch(keyword, sortType=TYPE_BOFANG, duration=0, tids_1=0, tids_2=0, page=1):
    """
    根据关键词搜索视频(非番剧)
    输入: 
        keyword: 关键词
        order: 排序方式, 参照TYPE_开头的常量
        duration: 视频时长, 0:全部时长 1:10分钟以下 2:10-30分钟 3:30-60分钟 4:60分钟以上
        tids_1: 一级分区代号, 见文档
        tids_2: 二级分区代号
        page: 页码
    返回:
        1.Video类列表, 若无结果返回空列表[]
        2.抓取的搜索页面地址
    备注:
        该函数不能获取番剧剧集, 搜索番剧请用 biliBangumiSearch函数
    """
    url = 'https://search.bilibili.com/video?keyword={0}&order={1}&duration={2}&tids_1={3}&tids_2={4}&page={5}'.format(UrlEncode(keyword), sortType, duration, tids_1, tids_2, page)
    content = getURLContent(url) # 惊了 事实证明只要请求header有cookie字段就能正常返回信息
    VideoInfo = getREsearch(content, r'<script>window.__INITIAL_STATE__(.?)=(.?)({.*});(.?)\(')
    if VideoInfo:
        VideoInfo = VideoInfo.group(3) # 获取捕获组
        jsoninfo = JsonInfo(VideoInfo)
        if jsoninfo['apiErrorCode'] != 0: # 确认是否成功获取搜索信息
            logging.error('获取搜索信息失败 >_<')
            return [], url
    else:
        logging.error('正则表达式查找视频信息失败 >_<')
        return [], url
    VideoList = []
    for video_idx in iter(jsoninfo['videoData']):
        video = Video(video_idx['id'], getREsub(video_idx['title'], '', '<[^>]+>')) # 若title有关键字会用Html标签标记 需要去掉
        video.play = video_idx['play']
        video.desc = video_idx['description']
        video.pubdate = num2time(video_idx['pubdate'])
        video.review = video_idx['review']
        video.pic = video_idx['pic']
        video.mid = video_idx['mid']
        video.arcurl = video_idx['arcurl']
        video.tag = video_idx['tag'].split(',')
        video.danmaku = video_idx['video_review']
        video.author = video_idx['author']
        video.favorites = video_idx['favorites']
        video.duration = video_idx['duration']
        video.type = video_idx['type']
        video.arcurl = 'https://www.bilibili.com/video/av{0}'.format(video.aid)
        VideoList.append(video)
    return VideoList, url

def biliBangumiSearch(keyword, page=1):
    """
    搜索B站番剧
    输入:
        keyword: 关键字
        page: 结果页码, 1页最多20个条目
    返回:
        1.Bangumi类列表, 无结果返回空列表[]
        2.抓取的搜索页面地址
    """
    url1 = 'https://search.bilibili.com/bangumi?keyword={0}&page={1}'.format(UrlEncode(keyword), page)
    content = getURLContent(url1)
    VideoInfo = getREsearch(content, r'<script>window.__INITIAL_STATE__(.?)=(.?)({.*});(.?)\(')
    if VideoInfo:
        VideoInfo = VideoInfo.group(3) # 获取捕获组
        jsoninfo = JsonInfo(VideoInfo)
        if jsoninfo['apiErrorCode'] != 0: # 确认是否成功获取搜索信息
            logging.error('获取搜索信息失败 >_<')
            return [], url1
    else:
        logging.error('正则表达式查找视频信息失败 >_<')
        return [], url1
    media_id = getRE(VideoInfo, r'"media_id":(\d+),')
    media_score = getRE(VideoInfo, r'"media_score":(.+?),"c')
    bangumis = []
    for idx, val in enumerate(media_id):
        url2 = 'https://bangumi.bilibili.com/view/web_api/season?media_id=' + val
        jsoninfo = JsonInfo(getURLContent(url2))
        result = jsoninfo['result']

        bangumi = Bangumi()
        bangumi.cover = result['cover']
        bangumi.actors = result['actors']
        bangumi.alias = result['alias']
        bangumi.areas_id = result['areas'][0]['id']
        bangumi.areas_name = result['areas'][0]['name']
        bangumi.evaluate = result['evaluate']
        bangumi.jp_title = result['jp_title']
        bangumi.link = result['link']
        bangumi.media_id = result['media_id']
        bangumi.newest_ep = result['newest_ep']
        bangumi.is_finish = result['publish']['is_finish']
        bangumi.is_started = result['publish']['is_started']
        bangumi.pub_time = result['publish']['pub_time']
        bangumi.weekday = result['publish']['weekday']
        bangumi.season_status = result['season_status']
        bangumi.season_title = result['season_title']
        bangumi.season_type = result['season_type']
        bangumi.square_cover = result['square_cover']
        bangumi.staff = result['staff']
        bangumi.coins = result['stat']['coins']
        bangumi.danmakus = result['stat']['danmakus']
        bangumi.favorites = result['stat']['favorites']
        bangumi.views = result['stat']['views']
        bangumi.reply = result['stat']['reply']
        bangumi.share = result['stat']['share']
        bangumi.style = result['style']
        bangumi.title = result['title']
        bangumi.total_ep = result['total_ep']
        bangumi.pub_ep = int(result['newest_ep']['index'])
        # 评分
        if media_score[idx] != 'null':
            scoreinfo = JsonInfo(media_score[idx])
            bangumi.score = scoreinfo['score']
            bangumi.user_count = scoreinfo['user_count']
        # 剧集列表
        episodes = []
        for ep in result['episodes']:
            episode = Episode()
            episode.title = bangumi.title
            episode.aid = ep['aid']
            episode.cid = ep['cid']
            episode.cover = ep['cover']
            episode.duration = num2duration(ep['duration'] // 1000)
            episode.ep_id = ep['ep_id'] # 剧集号
            episode.episode_status = ep['episode_status']
            episode.From = ep['from']
            episode.index = ep['index'] # 第几话
            episode.index_title = ep['index_title'] # 该话标题
            episode.pub_real_time = ep['pub_real_time'] # 发布时间
            if episode.ep_id:
                episode.link = 'https://www.bilibili.com/bangumi/play/ep{0}'.format(episode.ep_id) # 观看地址
            # 热度信息   这里要获取热度信息 很费时间
            # url3 = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={0}'.format(episode.aid)
            # stat = JsonInfo(getURLContent(url3))
            # episode.play = stat['data', 'view']
            # episode.danmaku = stat['data', 'danmaku']
            # episode.review = stat['data', 'reply']
            # episode.favorite = stat['data', 'favorite']
            # episode.coin = stat['data', 'coin']
            # episode.share = stat['data', 'share']
            # episode.like = stat['data', 'like']
            # episode.now_rank = stat['data', 'now_rank']
            # episode.his_rank = stat['data', 'his_rank']

            # up
            episode.mid = ep['mid'] 
            # 不明
            episode.vid = ep['vid']
            episodes.append(episode)

        bangumi.episodes = episodes

        # up
        if 'up_info' in result.keys():
            bangumi.avatar = result['up_info']['avatar']
            bangumi.mid = result['up_info']['mid']
            bangumi.uname = result['up_info']['uname']
        # 权限信息
        bangumi.allow_bp = result['rights']['allow_bp']
        bangumi.allow_download = result['rights']['allow_download']
        bangumi.allow_review = result['rights']['allow_review']
        bangumi.copyright = result['rights']['copyright']
        bangumi.is_preview = result['rights']['is_preview']
        bangumi.watch_platform = result['rights']['watch_platform']
        # 不明
        bangumi.is_paster_ads = result['is_paster_ads']
        bangumi.mode = result['mode']

        bangumis.append(bangumi)
    return bangumis

def getVideoStat(aid):
    """
    获取视频的热度信息, 番剧通用
    输入:
        aid: av号
    返回:
        result: 包含热度信息的字典类型
    """
    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={0}'.format(aid)
    stat = JsonInfo(getURLContent(url))
    result = {
        'view' : None,
        'danmaku' : None,
        'reply' : None,
        'favorite' : None,
        'coin' : None,
        'share' : None,
        'like' : None,
        'now_rank' : None,
        'his_rank' : None,
        'copyright' : None
    }
    result['play'] = stat['data', 'view']
    result['danmaku'] = stat['data', 'danmaku']
    result['review'] = stat['data', 'reply']
    result['favorite'] = stat['data', 'favorite']
    result['coin'] = stat['data', 'coin']
    result['share'] = stat['data', 'share']
    result['like'] = stat['data', 'like']
    result['now_rank'] = stat['data', 'now_rank']
    result['his_rank'] = stat['data', 'his_rank']
    result['copyright'] = stat['data', 'copyright']
    return result

def getOnlineCount(aid, cid):
    """
    获取某视频当前在线观看人数, 番剧通用
    输入:
        aid: av号
        cid: 弹幕池号
    返回:
        该视频当前在线观看人数
    """
    url = 'https://interface.bilibili.com/player?id=cid:{0}&aid={1}'.format(cid, aid)
    online_count = getREsearch(getURLContent(url), r'<online_count>(\d+)</online_count>')
    if online_count:
        return int(online_count.group(1))
    else:
        logging.error('获取在线观看人数失败 >_<')
        return None

def getVideoSrcurl(cid):
    """
    获取视频源地址(非番剧), 即下载地址, 只能获取非大会员能看的最高清晰度的版本, 最高1080p
    输入:
        cid: 弹幕池号
    返回:
        由视频源地址构成的列表, 因为部分太长视频是分片的, 故有好几个地址, 获取失败返回None
    """
    video_api_url = 'http://interface.bilibili.com/v2/playurl?'
    secretkey = 'aHRmhWMLkdeMuILqORnYZocwMBpMEOdt'
    params = 'appkey=iVGUTjsxvpLeuDCf&cid={0}&otype=json&qn=80&quality=80&type='.format(cid)
    api_url = video_api_url + params + '&sign=' + getSign(params, secretkey)

    jsoninfo = JsonInfo(getURLContent(api_url))
    if jsoninfo.error:
        return None
    srcurls = []
    for val in jsoninfo['durl']:
        srcurls.append(val['url'])
    return srcurls

def getEpisodeSrcurl(cid):
    """
    获取剧集源地址(番剧), 这里实现获取非大会员能看的最高清晰度的版本, 即最高1080p
    输入:
        cid: 弹幕池号
    返回:
        由视频源地址构成的列表, 因为部分太长视频是分片的, 故有好几个地址, 获取失败返回None
    备注:
        其实还有个 https://bangumi.bilibili.com/player/web_api/v2/playurl? 的api, 但目前得不到secretkey 有待更新
    """
    bangumi_api_url = 'http://bangumi.bilibili.com/player/web_api/playurl?' # 此api只能返回xml格式
    secretkey = '9b288147e5474dd2aa67085f716c560d'
    params = 'cid={0}&module=bangumi&player=1&qn=80&ts={1}'.format(cid, str(time.time()))
    api_url = bangumi_api_url + params + '&sign=' + getSign(params, secretkey)
    xml = parseString(getURLContent(api_url))
    durls = xml.getElementsByTagName('durl')
    srcurls = []
    for durl in durls:
        srcurls.append(durl.getElementsByTagName('url')[0].firstChild.nodeValue)
    return srcurls

def mpvPlayVideo(aid, pid=1):
    """
    调用mpv播放视频(包括番剧)
    输入:
        aid: av号
        pid: 分p号, 默认1
    依赖:
        mpv
    """
    video = getVideoInfo(aid, pid)
    logging.info('弹幕装填中...')
    saveDanmuku(video.cid)
    assfile = r'./{}.ass'.format(video.cid)
    index_title = ''
    logging.info('解析视频地址...')
    if video:
        if isinstance(video, Video):
            srcurls = getVideoSrcurl(video.cid)
        else:
            srcurls = getEpisodeSrcurl(video.cid)
            index_title = video.index_title
        paraurls = ''
        for val in srcurls:
            paraurls += '"{}"'.format(val) + ' '
        cmd = 'mpv --http-header-fields="Referer:https://www.bilibili.com/" --merge-files --force-media-title="{} {}" --sub-file="{}" {}'.format(video.title, index_title, assfile, paraurls)
    else:
        logging.error('获取视频信息失败 >_<')
        return
    logging.info('启动mpv进行播放...')
    os.system(cmd)
    logging.info('播放完毕, 回收弹幕残骸...')
    os.remove(assfile)
    logging.info('Done!')

def getDanmuku(cid):
    """
    获取弹幕, 返回xml格式字符串
    输入:
        cid: 弹幕池号
    返回: 
        返回xml格式字符串
    """
    url = "http://comment.bilibili.com/{0}.xml".format(cid)
    content = str(zlib.decompressobj(-zlib.MAX_WBITS).decompress(getURLContent(url)), 'utf-8')
    return content

def danmaku2ass(xmlfile, asspath='./'):
    """
    弹幕xml转换成ass格式, 注意路径使用原始字符串
    输入:
        xmlfile: 弹幕xml文件地址
        asspath: 转换成ass保存地址, 默认asspath地址为当前路径
    备注:
        ass文件名与xml文件相同
    依赖:
        Danmaku2ASS()
    """
    xmlname = getREsearch(xmlfile, r'[\\/]([^\\/]*?).xml$')
    if xmlname:
        xmlname = xmlname.group(1)
    else:
        logging.error('弹幕xml文件名匹配失败 >_<')
        return
    try:
        Danmaku2ASS(xmlfile, 'autodetect', r'{0}{1}.ass'.format(asspath, xmlname), 1920, 1080, 0, 'sans-serif', 48, 0.8, 10, 10, None, False)
    except:
        logging.error('弹幕xml2ass转换失败 >_<')
        return
    logging.info('弹幕转换成功 >v<')

def saveDanmuku(cid, path='./'):
    """
    指定路径保存弹幕为ass文件
    输入:
        cid: 弹幕池号
        path: 保存弹幕ass文件地址, 默认为当前路径
    备忘:
        保存的ass文件名为cid
    依赖:
        getDanmuku()
        danmaku2ass()
    """
    content = getDanmuku(cid)
    xmlfile = path + '{0}.xml'.format(cid)
    with open(xmlfile, 'w', encoding='utf-8') as fp:
        fp.write(content)
    danmaku2ass(xmlfile, path)
    os.remove(xmlfile)



if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    mpvPlayVideo(28463616) # 普通视频测试
    # mpvPlayVideo(33160847) # 番剧测试
    # a = biliBangumiSearch("jojo")
    pass
