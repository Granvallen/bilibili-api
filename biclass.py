# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17  16:34:00 2018

@author: Granvallen
"""

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

class Bangumi():
    """
    番剧类
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
