# coding=utf-8
import os
import time
import sys
from wechat_analyzer.basic_class.Article import Article
from wechat_analyzer.basic_class.WechatUser import WechatUser

__author__ = 'jayvee'
apath = os.path.dirname(__file__)
sys.path.append(apath)
reload(sys)
sys.setdefaultencoding('utf-8')


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


# ------------ directly DAO utils --------------

# init mongoDB
import pymongo

client = pymongo.MongoClient('112.126.80.78', 27017)
wechat_analysis_collection = client['wechat_analysis']
a_db = wechat_analysis_collection['Articles']
u_db = wechat_analysis_collection['Users']
re_db = wechat_analysis_collection['Reactions']
conf_db = wechat_analysis_collection['Configs']


def mongo_insert_article(inst_article, article_db=a_db):
    """
    直接连接mongo数据库，插入文章数据
    :param inst_article: Article实例
    :return:
    """

    article = {'title': inst_article.a_title, 'article_id': inst_article.a_id, 'tags': inst_article.a_tags,
               'content': inst_article.a_content, 'post_date': inst_article.post_date,
               'post_user': inst_article.post_user, 'article_url': inst_article.a_url}
    article_db.insert(article)
    return article


def mongo_get_article(a_id, article_db=a_db):
    """
    根据文章id获取article实例
    :param a_id:
    :return:
    """
    find_result = article_db.find_one({'article_id': a_id})
    article = Article(a_id, a_title=find_result['title'], post_user=find_result['post_user'],
                      a_tags=find_result['tags'], post_date=find_result['post_date'])
    return article


def mongo_insert_user(inst_user, user_db=u_db):
    """

    :param inst_user:
    :param user_db:
    :return:
    """
    user = {'user_id': inst_user.user_id, 'user_name': inst_user.user_name, 'article_vec': inst_user.user_atag_vec,
            'user_tag_vec': inst_user.user_tag_score_vec}
    user_db.insert(user)
    # user_db.save()


def mongo_get_user(user_id, user_db=u_db):
    """

    :param user_id:
    :param user_db:
    :return:
    """
    find_result = u_db.find_one({'user_id': user_id})
    user = WechatUser(user_id=user_id, user_name=find_result['user_name'], user_atag_vec=find_result['article_vec'],
                      user_tag_score_vec=find_result['user_tag_vec'])
    return user


def mongo_insert_reactions(inst_reaction, reaction_db=re_db):
    """

    :param inst_reaction:
    :param reaction_db:
    :return:
    """
    reaction = {'reaction_id': inst_reaction.reaction_id, 'reaction_type': inst_reaction.reaction_type,
                'reaction_a_id': inst_reaction.reaction_a_id, 'reaction_user_id': inst_reaction.reaction_user_id,
                'reaction_date': inst_reaction.reaction_date}
    reaction_db.insert(reaction)
    # reaction_db.save()


def mongo_get_global_user_tags(config_db=conf_db):
    """

    :return:
    """
    find_result = config_db.find_one({'name': 'global_user_tags'})
    return find_result['value']


def mongo_get_global_article_tags(config_db=conf_db):
    """

    :return:
    """
    find_result = config_db.find_one({'name': 'global_articles_tags'})
    return find_result['value']


def mongo_get_reaction_type_weight(config_db=conf_db):
    """

    :return:
    """
    find_result = config_db.find_one({'name': 'reaction_type_weight'})
    return find_result['value']


def mongo_get_a_u_tagmap(config_db=conf_db):
    find_result = config_db.find_one({'name': 'a_u_tagmap'})
    return find_result['value']


def mongo_set_conf(config_name, config_value, config_db=conf_db):
    conf_db.insert({'name': config_name, 'value': config_value})
    # conf_db.save()
    return 0
