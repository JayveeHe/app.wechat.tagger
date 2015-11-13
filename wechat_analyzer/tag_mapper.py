# coding=utf-8
from wechat_analyzer import DAO_utils

"""
用于设置和更新tag之间的映射权重
"""

__author__ = 'jayvee'

weight_map = {u'娱乐-5': {u'追星族': 0.1, u'电视迷': 0.9},
              u'娱乐-9': {u'追星族': 0.7, u'八卦': 0.3},
              u'娱乐-11': {u'追星族': 0.7, u'八卦': 0.3},
              u'互联网-2': {u'互联网业界': 1},
              u'体育-4': {u'体育装备': 0.7, u'体育历史': 0.3},
              u'体育-6': {u'体育新闻': 1},
              u'体育-11': {u'体育装备': 0.2, u'体育历史': 0.8},
              u'军事-10': {u'军事轶事': 1},
              u'军事-11': {u'军事历史': 0.9, u'军事新闻': 0.1}}


def map_atag2utag(atag):
    p = weight_map[atag]
    return p


def update_a_u_map(reaction_list, a_u_map, insert_rate=0.001):
    """
    根据一段时间的交互记录，更新文章tag到用户tag之间的映射权重值
    :param reaction_list:
    :param a_u_map:
    :param insert_rate:
    :return:
    """
    # TODO 更顺畅的权值更新公式
    for reaction in reaction_list:
        # process article tags
        reaction_a_id = reaction.reaction_a_id
        article = DAO_utils.get_article_by_id(reaction_a_id)
        article_tags = article.atags
        # get user tags
        reaction_user_id = reaction.reaction_user_id
        user = DAO_utils.get_user_by_id(reaction_user_id)
        utag_vec = user.user_tag_score_vec

        reaction_type = reaction.reaction_type
        reaction_date = reaction.reaction_date
        for atag_key in article_tags:
            # 采用稀释的方式改变映射权值
            atag_value = article_tags[atag_key]  # 文章本身的tag权值，用于衡量该篇文章的属性，0~1之间的值。
            # 首先稀释原有的权值
            a_u_inst = a_u_map[atag_key]
            for ukey in a_u_inst:
                a_u_inst[ukey] *= (1 - insert_rate)
            # 然后insert用户的tags
            for utag_key in utag_vec:
                if utag_key in a_u_inst:
                    a_u_inst[utag_key] += utag_vec[utag_key] * insert_rate * atag_value
                else:
                    a_u_inst[utag_key] = utag_vec[utag_key] * insert_rate * atag_value
        return a_u_map


def config_a_u_map(a_u_map):
    if type(a_u_map) is dict:
        DAO_utils.mongo_set_conf('a_u_tagmap', a_u_map)
    else:
        raise TypeError('a_u_map should be a dict!')


def config_reaction_type_weight(reaction_type_weight):
    if type(reaction_type_weight) is dict:
        DAO_utils.mongo_set_conf('reaction_type_weight', reaction_type_weight, is_overwrite=True)
    else:
        raise TypeError('reaction_type_weight should be a dict!')


if __name__ == '__main__':
    print map_atag2utag(u'娱乐-11')
    weight_map = {u'娱乐-5': {u'追星族': 0.1, u'电视迷': 0.9},
                  u'娱乐-9': {u'追星族': 0.7, u'八卦': 0.3},
                  u'娱乐-11': {u'追星族': 0.7, u'八卦': 0.3},
                  u'互联网-2': {u'互联网业界': 1},
                  u'体育-4': {u'体育装备': 0.7, u'体育历史': 0.3},
                  u'体育-6': {u'体育新闻': 1},
                  u'体育-11': {u'体育装备': 0.2, u'体育历史': 0.8},
                  u'军事-10': {u'军事轶事': 1},
                  u'军事-11': {u'军事历史': 0.9, u'军事新闻': 0.1}}
    config_a_u_map(weight_map)

    reaction_type_weight = {'read': 0.5, 'favor': 1.8, 'repost': 3.0}
    config_reaction_type_weight(reaction_type_weight)
