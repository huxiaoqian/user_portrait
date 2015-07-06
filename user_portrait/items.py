# -*- coding: utf-8 -*-

from scrapy.item import Item, Field

class UserItem_search(Item):
    """
    search spider，字段值中有转义符
    """
    id = Field() # 用户UID, 2854532022,
    # idstr = Field() # 字符串型用户ID, 与id字段重复, 不用存, "2854532022"
    class_type = Field() # 1, ?
    screen_name = Field() # "Come_On_TAO", 用户昵称
    name = Field() # "Come_On_Tao", 友好显示名称
    province = Field() # "100", 用户所在省级ID
    city = Field() # "1000", 用户所在城市ID
    location = Field() # "\u5176\u4ed6", 用户所在地
    description = Field() # 用户自我描述
    url = Field() # 用户博客地址
    profile_image_url = Field() # 用户头像地址（中图），50×50像素
    profile_url = Field() # 用户的微博统一URL地址, http://weibo.com/profile_url就是用户微博主页
    domain = Field() # 用户个性化URL, 同上
    weihao = Field() # 用户的微号(新浪微博用户个性化纯数字号码), ""
    gender = Field() # 用户性别, 'f'
    followers_count = Field() # 粉丝数
    friends_count = Field() # 关注数
    pagefriends_count = Field() # ?
    statuses_count = Field() # 微博数
    favourites_count = Field() # 收藏数
    created_at = Field() # 注册日期, "Thu Jun 28 21:13:09 +0800 2012"
    timestamp = Field() # created_at字段转化而来的时间戳
    following = Field() # false, ?
    allow_all_act_msg = Field() # true, 是否允许所有人给我发私信，true：是，false：否
    geo_enabled = Field() # 是否允许标识用户的地理位置, false
    verified = Field() # 加V标示，是否微博认证用户, false
    verified_type = Field() # 用户认证类型, -1
    ptype = Field() # 0
    allow_all_comment = Field() # 是否允许所有人对我的微博进行评论
    avatar_large = Field() # 用户头像地址（大图），180×180像素
    avatar_hd = Field() # 用户头像地址（高清），高清头像原图
    verified_reason = Field() # 认证原因, ""
    verified_trade = Field() # "", ?
    verified_reason_url = Field() # "", ?
    verified_source = Field() # "", ?
    verified_source_url = Field() # "", ?
    follow_me = Field() # false, 该用户是否关注当前登录用户，true：是，false：否
    online_status = Field() # 用户的在线状态，0：不在线、1：在线
    bi_followers_count = Field() # 用户的互粉数
    lang = Field() # 用户当前的语言版本，"zh-cn"：简体中文，"zh-tw"：繁体中文，"en"：英语
    star = Field() # 0, ?
    mbtype = Field() # 12, ?
    mbrank = Field() # 5, ?
    block_word = Field() # 1, ?
    block_app = Field() # 1, ?
    credit_score = Field() # ?

    cover_image = Field() # 用户封面地址
    cover_image_phone = Field() # ?
    ulevel = Field() # 0, ?
    badge_top = Field() # "", ?
    extend = Field() # ?, {"privacy":{"mobile":0},"mbprivilege":"0000000000000000000000000000000000000000000000000000000000000000"}
    remark = Field() # "" ?
    verified_state = Field() # 0
    # uids list
    followers = Field() # just uids
    friends = Field() # just uids
    # 自定义字段
    first_in = Field()
    last_modify = Field()
    
    # utils.py中解析返回数据的字段
    RESP_ITER_KEYS = ['id', 'name', 'class_type', 'gender', 'province', 'city', 'location', 'url', 'domain', \
    'geo_enabled', 'verified', 'verified_type', 'description', \
    'followers_count', 'statuses_count', 'friends_count', 'favourites_count', \
    'profile_image_url', 'allow_all_act_msg', 'created_at', 'verified_reason']
    
    # mongodb pipelines中更新的字段
    PIPED_UPDATE_KEYS = ['name', 'class_type', 'gender', 'province', 'city', 'location', 'url', 'domain', \
    'geo_enabled', 'verified', 'verified_type', 'description', \
    'followers_count', 'statuses_count', 'friends_count', 'favourites_count', \
    'profile_image_url', 'allow_all_act_msg', 'created_at', 'verified_reason']

    def __init__(self, search_type):
        """
        >>> a = UserItem()
        >>> a
        {'followers': [], 'friends': []}
        >>> a.to_dict()
        {'followers': [], 'friends': []}
        """
        super(UserItem_search, self).__init__()

        default_empty_arr_keys = ['followers', 'friends']
        for key in default_empty_arr_keys:
            self.setdefault(key, [])

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (UserItem_search, WeiboItem_search)):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d

class WeiboItem_search(Item):
    """
    search spider，字段值中有转义符
    """
    id = Field() # 16位微博ID, 3752470516005693
    uid = Field() # just uid, 用户uid
    user = Field() # user info dict
    mid = Field() # 16位微博ID, "3752470516005693"
    created_at = Field() # 微博创建时间, "Mon Sep 08 10:09:10 +0800 2014"
    timestamp = Field() # created_at字段转化而来的时间戳
    text = Field() # unicode, 微博信息内容
    source = Field() # 微博来源, <a href=\"http:\/\/app.weibo.com\/t\/feed\/8crQy\" rel=\"nofollow\">Weico.iPhone<\/a>",

    favorited = Field() # false, 是否已收藏，true：是，false：否
    truncated = Field() # false, 是否被截断，true：是，false：否
    in_reply_to_status_id = Field() # "", 回复ID
    in_reply_to_user_id = Field() # "", 回复人UID
    in_reply_to_screen_name = Field() # "", 回复人昵称
    geo = Field() # null, 地理信息字段
    reposts_count = Field() # 转发数
    comments_count = Field() # 评论数
    attitudes_count = Field() # 赞数
    mlevel = Field() # 0, ?
    visible = Field() # 微博的可见性及指定可见分组信息, 该object中type取值，0：普通微博，1：私密微博，3：指定分组微博，4：密友微博; list_id为分组的组号
    
    pic_ids = Field() # queryWeiboBykw返回该字段, 微博配图id, 多图时返回多图id, 无配图返回“[]”, 转发微博无法配图此字段为[]
    pic_urls = Field() # queryUserWeibo返回该字段, [{"thumbnail_pic": "http://ww4.sinaimg.cn/thumbnail/475b3d56gw1ek4vgg9x3xj20c60ee0t7.jpg"},]
    
    pid = Field() # 3752469458416290, ?, 原创微博无该字段
    thumbnail_pic = Field() # 缩略图片地址，没有时不返回此字段, 转发微博无法配图不返回该字段
    bmiddle_pic = Field() # 中等尺寸图片地址，没有时不返回此字段, 转发微博无法配图不返回该字段
    original_pic = Field() # 原始图片地址，没有时不返回此字段, 转发微博无法配图不返回该字段
    retweeted_status = Field() # 源微博dict
    annotations = Field() # ?, 转发微博无该字段，原创微博有该字段, [{"client_mblogid":"iPhone-2849F7C0-695E-4C50-B9A9-101770EEFC70"}]
    reposts = Field() # just mids, 转发微博id列表
    comments = Field() # just ids, 评论微博id列表
    category = Field() # 31, ?, 转发微博有该字段，原创微博无该字段

    floor_num = Field() # 楼号 3
    reply_comment = Field() # 回复的评论mid

    keywords = Field() # search接口定义的话题关键词

    # ad = Field() # 微博流内的推广微博ID, 没有该字段
    # url_objects = Field() # 有该字段，但太长没有必要，?
    # idstr = Field() # 16位微博ID, 和mid重复不用存, 字符串型微博ID, "3752470516005693"
    # darwin_tags = Field() # [], ?

    # 自定义字段
    first_in = Field()
    last_modify = Field()

    search_type = Field()

    RESP_ITER_KEYS = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
    'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
    'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
    'attitudes_count']

    PIPED_UPDATE_KEYS = ['created_at', 'source', 'favorited', 'truncated', \
    'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
    'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
    'attitudes_count']

    def __init__(self, search_type):
        super(WeiboItem_search, self).__init__()
        default_empty_arr_keys = ['reposts', 'comments']
        for key in default_empty_arr_keys:
            self.setdefault(key, [])

        self.setdefault('search_type', search_type)

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, (UserItem_search, WeiboItem_search)):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d

    def get_resp_iter_keys(self):
        resp_iter_keys = []
        search_type = self.__getitem__("search_type")
        if search_type == 1:
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']

        elif search_type == 2: # 用户最新微博
            resp_iter_keys =  ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']
        
        elif search_type == 3: # 转发
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']

        elif search_type == 4: # 被转发微博
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'thumbnail_pic', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']

        elif search_type == 5: # 评论
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'pic_ids']
        
        elif search_type == 6: # 评论被回复微博
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'pic_ids']

        elif search_type == 7: # 被评论微博
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']
    
        elif search_type == 8: # showBatch
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']
    
        elif search_type == 9: # userweibo
            resp_iter_keys = ['created_at', 'id', 'mid', 'text', 'source', 'favorited', 'truncated', \
            'in_reply_to_status_id', 'in_reply_to_user_id', 'in_reply_to_screen_name', \
            'pic_urls', 'geo', 'reposts_count', 'comments_count', \
            'attitudes_count']

        return resp_iter_keys

    def get_piped_update_keys(self):
        piped_update_keys = ['favorited', 'truncated', 'reposts_count', \
        'comments_count', 'attitudes_count']

        return piped_update_keys

class FriendsItem(Item):
    id = Field() # 用户UID, 2854532022,
    friends = Field()
    followers = Field()

    PIPED_UPDATE_KEYS = ['friends', 'followers']

    def __init__(self):
        super(FriendsItem, self).__init__()
        default_empty_arr_keys = ['friends', 'followers']
        for key in default_empty_arr_keys:
            self.setdefault(key, [])

    def to_dict(self):
        d = {}
        for k, v in self.items():
            if isinstance(v, FriendsItem):
                d[k] = v.to_dict()
            else:
                d[k] = v
        return d

