# coding=utf-8
# from wechat_analyzer.DAO_utils import get_article_by_id

__author__ = 'jayvee'


class WechatUser:
    def __init__(self, user_id, user_name='', user_atag_vec={},
                 reaction_type_weight=None, user_tag_score_vec=None):
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
        if user_id:
            if not user_tag_score_vec:
                user_tag_score_vec = {}
            if not reaction_type_weight:
                self.reaction_type_weight = {'read': 0.5, 'favor': 1.8, 'repost': 3}
            self.user_id = user_id
            self.user_name = user_name
            self.user_atag_vec = user_atag_vec  # 用户的文章tag交互向量
            self.user_tag_score_vec = user_tag_score_vec
        else:
            raise TypeError
