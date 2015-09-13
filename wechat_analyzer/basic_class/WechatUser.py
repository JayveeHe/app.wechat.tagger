# coding=utf-8
from wechat_analyzer.DAO_utils import get_article_by_id

__author__ = 'jayvee'


class WechatUser:
    def __init__(self, user_id, user_taglist, global_a_tagdict, global_u_tagdict, user_atag_vec={},
                 reaction_type_weight=None,
                 user_tags_dict={}, user_tag_score_vec={}, a_u_tagmap={}):
        """
        init wechat user
        :param user_id: 用户id
        :param user_taglist: 该用户所拥有的tags（可能与user_tag_score_vec重复）
        :param global_a_tagdict: 预设的全局文章tag词典
        :param global_u_tagdict: 预设的全局用户tag词典
        :param reaction_type_weight: 预设的交互行为权重值（dict）
        :param user_tag_score_vec: 用户所拥有的每个tag的相应分值向量
        :param a_u_tagmap:每个文章tag能够映射到用户tag的dict，其中key为文章tag，
        value为一个映射dict，该映射dict的key为能够映射到的单个tag，value为相应的映射权值
        :return:
        """
        if not reaction_type_weight:
            reaction_type_weight = {'read': 0.5, 'favor': 1.8, 'repost': 3}
        self.user_id = user_id
        self.user_taglist = user_taglist
        self.global_a_tagdict = global_a_tagdict
        self.global_u_tagdict = global_u_tagdict
        self.a_u_tagmap = a_u_tagmap
        self.reaction_type_weight = reaction_type_weight
        # init user_vec
        self.user_atag_vec = user_atag_vec  # 用户的文章tag交互向量
        for tag in user_tags_dict:
            self.user_atag_vec[tag] = 0
        self.user_tag_score_vec = user_tag_score_vec

    def user_tagging(self, reaction_list, a_u_tagmap):
        """
        根据用户一段时间的交互记录，更新用户的u_tag分数
        :param reaction_list:user_id等于当前用户id的一段时间内的交互记录
        :param a_u_tagmap:
        :return:
        """
        for reaction in reaction_list:
            weight = self.reaction_type_weight[reaction.reaction_type]
            a_id = reaction.reaction_a_id
            article = get_article_by_id(a_id)
            for a_tag_key in article.a_tags:  # 文章的tags应该是一个dict
                if a_tag_key in self.user_atag_vec:
                    self.user_atag_vec[a_tag_key] += weight * article.a_tags[a_tag_key]
                else:
                    self.user_atag_vec[a_tag_key] = weight * article.a_tags[a_tag_key]
        # 用户的atag_vec处理完毕，开始处理user_tag_score_vec
        # TODO 更好的权值赋值公式
        for a_tag_key in self.user_atag_vec:
            for u_tag_key in a_u_tagmap[a_tag_key]:
                if u_tag_key in self.user_tag_score_vec:
                    self.user_tag_score_vec[u_tag_key] += a_u_tagmap[a_tag_key][u_tag_key]
                else:
                    self.user_tag_score_vec[u_tag_key] = a_u_tagmap[a_tag_key][u_tag_key]
        return self.user_tag_score_vec
