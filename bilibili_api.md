[TOC]

# 1.获取热门视频排行榜:
## API
```
https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&pic_size=160x100&cate_id={二级分区代号}&order={排序方式}&time_from={起始时间, 格式'20180819'}&time_to={终止时间, 格式同起始时间}&page={页码}&pagesize={返回一页条目数, 最高100}&copy_right={是否原创, 是为1, 否为-1}
```
返回json
排序方式可选:
* 收藏: 'stow'
* 评论数: 'scores'
* 播放数: 'click' 也可以使用 'hot'
* 硬币数: 'coin'
* 弹幕数: 'dm'
* 投稿时间: 'pubdate'

例子:
```
https://s.search.bilibili.com/cate/search?main_ver=v3&search_type=video&view_type=hot_rank&pic_size=160x100&cate_id=17&order=stow&time_from=20180819&time_to=20180819&page=1&pagesize=20&copy_right=1
```

## API函数: 
```python
def getHotVideo(begintime, endtime, tid=33, sortType=TYPE_BOFANG, page=1, pagesize=20, original=False):
```

* 功能:
    * 获取各区热门视频排行榜(默认获取新番区tid=33)
* 输入：
    * begintime: 起始时间, 三元数组[year1, month1, day1] 如 [2018, 8, 2]
    * endtime: 终止时间, 三元数组[year2, month2, day2]
    * sortType: 字符串, 排序方式, 参照TYPE_开头的常量
    * tid: 整数, 投稿子分区代号(二级分区的序号), 参照文档说明
    * page: 整数, 页数, 默认1
    * pagesize: 单页拉取的视频数, 默认是20, 上限100
* 返回：
    * 视频列表, 列表中的Video类包含AV号, 标题, 观看数, 收藏数, 弹幕数, 投稿日期, 封面, UP的id号和名字, tag, 视频描述, 视频地址, 评论数等, 具体见参考文档
    * 实际爬取的b站排行页面url, 便于查错, 可以使用'_'不接收该返回值
* 备注:
    * 时间间隔应小于3个月
    * 这个api无论是否为搜索番剧区返回的信息格式都相同, 故没有区分是Video还是Episode, 都使用了Video类
    * 这个搜索视频的api只能用 `二级分区代号`


### 参数详细说明: 
好多参数几个函数都是相同的

#### sortType: 排序方式
* 收藏: TYPE_SHOUCANG
* 评论数: TYPE_PINGLUN
* 播放数: TYPE_BOFANG
* 硬币数: TYPE_YINGBI
* 弹幕数: TYPE_DANMU
* **投稿时间**: TYPE_TOUGAO (从新到旧排列)

#### tid: 分区代号
* 全站 0
* **动画**: 1
    * AMD·AMV: 24
    * MMD·3D: 25
    * 短片·手书·配音: 47
* **番剧**: 13
    * 连载动画: 33
    * 完结动画: 32
    * 资讯: 51
    * 官方延伸: 152
* **国创**:  167
    * 国产动画: 153
    * 国产原创相关: 168
    * 布袋戏: 169
    * 资讯: 170
* **音乐**: 3
    * 原创音乐: 28
    * 翻唱: 31
    * VOCALOID·UTAU: 30
    * 演奏: 59
    * 三次元音乐: 29
    * OP/ED/OST: 54
    * 音乐选集: 130
* **舞蹈** 129
    * 宅舞: 20
    * 三次元舞蹈: 154
    * 舞蹈教程: 156
* **游戏**: 4
    * 单机游戏: 17
    * 电子竞技: 171
    * 手机游戏: 172
    * 网络游戏: 65
    * 桌游棋牌: 173
    * GMV: 121
    * 音游: 136
    * Mugen: 19
* **科技**: 36
    * 趣味科普人文: 124
    * 野生技术协会: 122
    * 演讲·公开课: 39
    * 星海: 96
    * 数码: 95
    * 机械: 98
    * 汽车: 176
* **生活**: 160
    * 搞笑: 138
    * 日常: 21
    * 美食圈: 76
    * 动物圈: 75
    * 手工: 161
    * 绘画: 162
    * 运动: 163
    * 其他: 174
* **鬼畜**: 119
    * 鬼畜调教: 22
    * 音MAD: 26
    * 人力VOCALOID: 126
    * 教程演示: 127
* **时尚**: 155
    * 美妆: 157
    * 服饰: 158
    * 健身: 164
    * 资讯: 159
* **广告**: 165 166
* **娱乐**: 5
    * 综艺: 71
    * 明星: 137
    * Korea相关: 131
* **影视**: 181
    * 影视杂谈: 182
    * 影视剪辑: 183
    * 短片: 85
    * 预告·资讯: 184
    * 特摄: 86 
* **纪录片**: 177 
    * 人文历史: 37
    * 科学探索: 178
    * 热血军事: 179
    * 舌尖上的旅行: 180
* **电影**: 23  
    * 华语电影: 147
    * 欧美电影: 145
    * 日本电影: 146
    * 其他国家: 83
* **电视剧**: 11 
    * 国产剧: 185
    * 海外剧: 187

**注意**: b站的视频排行现在只有各分区的子分区(即二级分区)才有排行, 故参数tid只能取二级分区代号

#### 返回Video类中填充的字段:
* video.aid
* video.title
* video.play
* video.desc
* video.pubdate
* video.review
* video.pic
* video.mid
* video.arcurl
* video.tag
* video.danmaku
* video.author
* video.favorites
* video.duration
* video.type

Video类中具体字段的含义见Video类的说明 >_<

---

# 2.获取视频信息

## API

### 获取视频热度信息(播放数, 收藏数, 硬币数等)
```
https://api.bilibili.com/x/web-interface/archive/stat?aid={av号}
```
返回json
包含字段:
* 'view' : 播放数
* 'danmaku' : 弹幕数
* 'reply' : 评论数
* 'favorite' : 收藏数
* 'coin' : 硬币数
* 'share' : 分享数
* 'like' : 点赞数(不明)
* 'now_rank' : 当前排名
* 'his_rank' : 历史最高排名
* 'copyright' : 版权

例子:
```
https://api.bilibili.com/x/web-interface/archive/stat?aid=28463616
```

### 获取视频当前观看人数
```
https://interface.bilibili.com/player?id=cid:{弹幕池号}&aid={av号}
```
返回类似xml格式字符串
其中`online_count`字段即当前观看人数

例子:
```
https://interface.bilibili.com/player?id=cid:49247744&aid=28463616
```

### 获取视频(非番剧)源地址
```
http://interface.bilibili.com/v2/playurl?appkey={appkey}&cid={弹幕池号}&otype={返回类型, json或xml}&qn={视频质量}&quality={视频质量}&type=&sign={签名}
```
视频质量一般可选:
* 112: 1080+p
* 80: 1080p
* 64: 720p
* 32: 480p
* 16: 360p

1080+p大会员用户专享, 普通用户在登陆状态下最高可观看1080p, 在未登陆情况下通常480p. 此API可可获取大会员1080+p以下的清晰度, 即最高1080p(具体还要受限于实际上传视频的清晰度).

**注意**: 此API需要appkey与计算sign所用的secretkey, 这两个key需要申请, 此API我是参考了[you-get](https://github.com/soimort/you-get)项目的, **故请勿滥用**. 此处sign的算法可见`getVideoSrcurl`与`getSign`函数

### 获取剧集视频源地址(包括番剧, 电影等)
```
http://bangumi.bilibili.com/player/web_api/playurl?cid={弹幕池号}&module=bangumi&player=1&qn={视频质量}&ts={1}&sign={签名}
```

**注意**: 此API需要计算sign所用的secretkey, 此API我是参考了[you-get](https://github.com/soimort/you-get)项目的, **请勿滥用**. 此处sign的算法可见`getEpisodeSrcurl`与`getSign`函数
**注意**: 此API只能获取xml格式信息, 应该是旧版的API, 新版API地址为`https://bangumi.bilibili.com/player/web_api/v2/playurl?`, 但目前不知secretkey有待更新

## API函数

## 获取视频aid(av号)

```python
def getAid(url):
```

- 输入:
    - url: 视频url
- 返回:
    - aid: 视频av号

### 获取视频热度信息
```python
def getVedioStat(aid):
```

* 获取视频的热度信息, 番剧通用
* 输入:
    * aid: av号
* 返回:
    * result: 包含热度信息的字典类型, 字典中的内容即API返回json的内容

### 获取视频当前观看人数
```python
def getOnlineCount(aid, cid):
```

* 获取某视频当前在线观看人数, 番剧通用
* 输入:
    * aid: av号
    * cid: 弹幕池号
* 返回:
    * 该视频当前在线观看人数

### 获取视频(非番剧)源地址
```python
def getVideoSrcurl(cid):
```

* 获取视频源地址(非番剧), 即下载地址, 这里实现获取非大会员能看的最高清晰度的版本, 即最高1080p
* 输入:
    * cid: 弹幕池号
* 返回:
    * 由视频源地址构成的列表, 因为部分太长视频是分片的, 故有好几个地址, 获取失败返回None

### 获取剧集视频源地址(包括番剧, 电影等)
```python
def getEpisodeSrcurl(cid):
```
* 获取剧集源地址(番剧), 这里实现获取非大会员能看的最高清晰度的版本, 即最高1080p
* 输入:
    * cid: 弹幕池号
* 返回:
    * 由视频源地址构成的列表, 因为部分太长视频是分片的, 故有好几个地址, 获取失败返回None

### 获取视频信息(video 与 episode)
结合以上所有API, 用于获取视频完整的信息的函数, 以上API以外的信息通过直接抓取视频页面分析得到
```python
def getVideoInfo(aid, pid=1):
```
* 功能:
    * 由av号获取视频信息
* 输入: 
    * aid: av号
    * pid: 分p号, 对于番剧没有分p, 一个av号对应一集
* 返回:
    * 视频类Video 或 剧集类Episode 注意两个类的属性有所不同, 若视频不存在则返回None

对于返回Video类填充的字段有:

* video.aid
* video.tid
* video.videos
* video.pid
* video.tname
* video.pic
* video.title
* video.pubdate
* video.ctime
* video.desc
* video.state
* video.attribute
* video.duration
* video.mid
* video.face
* video.name
* video.dislike
* video.cid
* video.tag
* video.play
* video.danmaku
* video.review
* video.favorite
* video.coin
* video.share
* video.like
* video.now_rank
* video.his_rank
* video.copyright
* video.online_count
* video.arcurl
* video.srcurl

对于返回Episode类填充的字段有:

* episode.aid
* episode.cover
* episode.title
* episode.index_title
* episode.index
* episode.pub_real_time
* episode.duration
* episode.mid
* episode.cid
* episode.media_id
* episode.episode_status
* episode.ep_id
* episode.vid
* episode.play
* episode.danmaku
* episode.review
* episode.favorite
* episode.coin
* episode.share
* episode.like
* episode.now_rank
* episode.his_rank
* episode.copyright
* episode.online_count
* episode.link
* episode.srcurl

---

# 3.搜索B站视频(非番剧)
这里直接抓取搜索页面实现

```python
def biliVideoSearch(keyword, sortType=TYPE_BOFANG, duration=0, tids_1=0, tids_2=0, page=1):
```
* 根据关键词搜索视频(非番剧)
* 输入: 
    * keyword: 关键词
    * order: 排序方式, 参照TYPE_开头的常量
    * duration: 视频时长, 0:全部时长 1:10分钟以下 2:10-30分钟 3:30-60分钟 4:60分钟以上
    * tids_1: 一级分区代号, 见B站分区代号
    * tids_2: 二级分区代号
    * page: 页码
* 返回:
    * 1.Video类列表, 若无结果返回空列表[]
    * 2.抓取的搜索页面地址
* 备注:
    * 该函数不能获取番剧剧集, 搜索番剧请用 biliBangumiSearch函数

Video类填充的字段:
* video.aid
* video.title
* video.play
* video.desc
* video.pubdate
* video.review
* video.pic
* video.mid
* video.arcurl
* video.tag
* video.danmaku
* video.author
* video.favorites
* video.duration
* video.type
* video.arcurl

---

# 4.搜索B站番剧
这里也是直接抓取搜索页面实现

```python
def biliBangumiSearch(keyword, page=1):
```
* 搜索B站番剧
* 输入:
    * keyword: 关键字
    * page: 结果页码, 1页最多20个条目
* 返回:
    * 1.Bangumi类列表, 无结果返回空列表[]
    * 2.抓取的搜索页面地址

Bangumi类填充的字段:
* 基本信息
    * bangumi.cover
    * bangumi.actors
    * bangumi.alias
    * bangumi.areas_id
    * bangumi.areas_name
    * bangumi.evaluate
    * bangumi.jp_title
    * bangumi.link
    * bangumi.media_id
    * bangumi.newest_ep
    * bangumi.is_finish
    * bangumi.is_started
    * bangumi.pub_time
    * bangumi.weekday
    * bangumi.season_status
    * bangumi.season_title
    * bangumi.season_type
    * bangumi.square_cover
    * bangumi.staff
    * bangumi.coins
    * bangumi.danmakus
    * bangumi.favorites
    * bangumi.views
    * bangumi.reply
    * bangumi.share
    * bangumi.style
    * bangumi.title
    * bangumi.total_ep
    * bangumi.pub_ep
* 评分
    * bangumi.score
    * bangumi.user_count
* 剧集列表
    * bangumi.episodes
* up
    * bangumi.avatar
    * bangumi.mid
    * bangumi.uname
* 权限信息
    * bangumi.allow_bp
    * bangumi.allow_download
    * bangumi.allow_review
    * bangumi.copyright
    * bangumi.is_preview
    * bangumi.watch_platform
* 不明
    * bangumi.is_paster_ads
    * bangumi.mode

其中bangumi.episodes字段为Episode类列表, 其中每个Episode类填充字段有:

* episode.title
* episode.aid
* episode.cid
* episode.cover
* episode.duration
* episode.ep_id
* episode.episode_status
* episode.From
* episode.index
* episode.index_title
* episode.pub_real_time
* episode.link

---

# 5.获取弹幕
## API
```
http://comment.bilibili.com/{弹幕池号cid}.xml
```
返回弹幕xml

例子:
```
http://comment.bilibili.com/49247744.xml
```

## API函数

### 获取弹幕xml
```python
def getDanmuku(cid):
```
* 获取弹幕, 返回xml格式字符串
* 输入:
    * cid: 弹幕池号
* 返回: 
    * 返回xml格式字符串

### 弹幕xml格式转换为ass格式
此函数实现基于[danmaku2ass](https://github.com/m13253/danmaku2ass)项目, 我使用了其Danmaku2ASS函数.

```python
def danmaku2ass(xmlfile, asspath=os.path.expanduser('~')+'/Desktop/'):
```

* 弹幕xml转换成ass格式
* 输入:
    * xmlfile: 弹幕xml文件地址
    * asspath: 转换成ass保存地址, 默认asspath地址为当前路径
* 备注:
    * ass文件名与xml文件相同
* 依赖:
    * Danmaku2ASS()

### 下载视频弹幕保存为ass
即是以上两个函数的合并

```python
def saveDanmuku(cid, path=os.path.expanduser('~')+'/Desktop/'):
```

* 指定路径保存弹幕为ass文件
* 输入:
    * cid: 弹幕池号
    * path: 保存弹幕ass文件地址, 默认为当前路径
* 备忘:
    * 保存的ass文件名为cid
* 依赖:
    * getDanmuku()
    * danmaku2ass()

---

# 其他函数
## 调用mpv播放视频

```python
def mpvPlayVideo(aid, pid=1):
```

* 调用mpv播放视频(包括番剧)
* 输入:
    * aid: av号
    * pid: 分p号, 默认1
* 依赖:
    * mpv

---

# 简单应用: 一个用mpv播放B站视频的脚本bilifun.py
使用方法
```
> python bilifun.py {B站某视频播放地址}
```

例子:
```
> python bilifun.py https://www.bilibili.com/video/av28463616

> python bilifun.py https://www.bilibili.com/bangumi/play/ep84776

> python bilifun.py https://www.bilibili.com/bangumi/play/ss12364
```

**注意**: 此脚本并不能获取只有VIP才有权限看的视频

---

# 接口类的说明
biclass.py中定义了目前用到的几个类, 主要是类的字段
* Video类
* Episode类
* Bangumi类

## Video类
```python
class Video():
    """
    视频类(非番剧剧集) 
    """
    def __init__(self, aid = None, title = None):
        self.aid = aid # article id 即av号  json中的 'id' 与此相同
        self.title = title # 标题 或 番剧名
        self.cid = None # chat id 即弹幕池号
        self.copyright = None # 是否拥有版权 官方2 用户1 没有-1
        self.desc = None # 视频描述
        self.author = None # 作者
        self.pic = None # 视频封面 或 番剧该集的封面
        self.pubdate = None # 发布时间 有时是按秒计有时是时间字符串 
        self.tname = None # 投稿分区名   json中的 'typename' 与此相同
        self.tid = None # 投稿分区的序号
        self.videos = None # 猜测是 分p数
        self.arcurl = None # 视频地址
        self.srcurl = None # 视频源地址
        self.tag = None # 视频标签
        self.type = None # 稿件类型 如 'video'
        self.duration = None # 片长
        self.online_count = None # 在线观看人数
        self.pid = None # 当前分p
        self.part = None # 分p标题       还有个 'partname' 与 part 相同 
        self.From = None # 从什么页面跳转来的
        # 视频所有者 owner
        self.face = None # 用户头像url
        self.mid = None # 用户ID
        self.name = None # 用户名
        # 热度信息
        self.play = None # 播放量  json中的 'view' 与此相同
        self.danmaku = None # 弹幕总量 json中的 'vedio_review' 与此相同
        self.review = None # 评论数  json中的 'reply' 与此相同
        self.favorites = None # 收藏数 番剧的话是追番人数
        self.coin = None # 硬币
        self.share = None # 分享数
        self.like = None
        self.now_rank = None # 当前排名
        self.his_rank = None # 历史排名
        # 意义不明 或 没有用到
        self.attribute = None
        self.ctime = None  # 好像与pubtime是一样的
        self.dynamic = None  # 不明 有的是标签 但是与tag格式不同 有的不知道是什么信息
        self.state = None
        self.dislike = None
```

## Episode类
```python
class Episode():
    """
    剧集类(番剧剧集) 
    """
    def __init__(self, aid = None, title = None):
        self.aid = aid 
        self.title = title # 番剧名
        self.cid = None 
        self.cover = None
        self.duration = None
        self.ep_id = None # 剧集号
        self.episode_status = None
        self.From = None
        self.index = None # 第几话
        self.index_title = None # 该话标题
        self.pub_real_time = None # 发布时间
        self.link = None # 观看地址
        self.srcurl = None # 视频源地址
        self.media_id = None # 番剧号
        self.episode_status = None
        # 热度
        self.play = None
        self.danmaku = None
        self.review = None
        self.favorite = None
        self.coin = None
        self.share = None
        self.like = None
        self.now_rank = None
        self.his_rank = None
        self.copyright = None
        self.online_count = None
        # up
        self.mid = None 
        # 不明
        self.vid = None
```

## Bangumi类
```python
class Bangumi():
    """
    番剧类(包括电影等)
    """
    def __init__(self):
        # 番剧
        self.cover = None # 封面
        self.actors = None 
        self.alias = None # 番剧别名
        self.areas_id = None
        self.areas_name = None
        self.evaluate = None # 简介
        self.jp_title = None
        self.link = None # 番剧主页
        self.media_id = None # 番剧号     season_id 与此相同
        self.newest_ep = None # 最新一话
        self.is_finish = None
        self.is_started = None
        self.pub_time = None # 开播时间
        self.weekday = None # 更新礼拜
        self.season_status = None
        self.season_title = None # 类型  如 TV
        self.season_type = None
        self.square_cover = None # 番剧方形封面
        self.staff = None
        self.coins = None
        self.danmakus = None
        self.favorites = None
        self.views = None
        self.reply = None
        self.share = None
        self.style = None
        self.title = None
        self.total_ep = None
        self.pub_ep = None # 已经放送的话数
        self.score = None # 评分
        self.user_count = None # 评分人数
        # 剧集列表
        self.episodes = None
        # up
        self.avatar = None
        self.mid = None
        self.uname = None
        # 权限信息
        self.allow_bp = None
        self.allow_download = None
        self.allow_review = None
        self.copyright = None # 版权信息
        self.is_preview = None
        self.watch_platform = None
        # 不明
        self.is_paster_ads = None # 贴广告?
        self.mode = None
```























