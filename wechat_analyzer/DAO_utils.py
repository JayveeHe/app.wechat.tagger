# coding=utf-8
import time

__author__ = 'jayvee'


def get_article_tagsdict(a_id):
    """
    根据文章id获取
    API: /api/v1/atags    [POST]
    :param a_id: 文章id
    :return:
    """
    pass
    # /api/atags/<id>    [GET]


def get_article_by_id(article_id):
    """
    根据文章id获取一个Article实例
    后端交互API: /api/v1/article [POST]
    :param article_id:
    :return:Article实例
    """
    pass
    # /api/article/<article_id> [GET]


def get_reactions_by_userid(user_id, start_time, end_time=time.time()):
    """
    根据user_id和起止时间，返回该用户在某一时间段内的交互记录
    后端API: /api/v1/reaction [POST]
    :param user_id:
    :param start_time:
    :param end_time:
    :return: Reaction实例的list
    """
    pass


def get_reactions_by_articleid(article_id, start_time, end_time=time.time()):
    """
    根据文章id和起止时间，返回该文章在某时间段内的交互记录
    :param article_id:
    :param start_time:
    :param end_time:
    :return:Reaction实例的list
    """
    pass


def get_user_by_id(user_id):
    """
    根据user_id获取一个WechatUser实例
    后端API: /api/v1/user [POST]
    :param user_id:
    :return:
    """


def get_global_user_tags():
    """
    获取全局user_tags
    :return:
    """
    pass


def get_global_article_tags():
    """
    获取全局article_tags
    :return:
    """
    pass


def get_a_u_map():
    """
    获取所有article_tag到user_tag的映射值，map
    :return:
    """
    pass
