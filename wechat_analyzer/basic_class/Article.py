# coding=utf-8
__author__ = 'jayvee'


class Article:
    def __init__(self, a_id, a_tags={}):
        """
        文章的a_tags应该是一个dict，key为tag，value为相应的tag权值
        :param a_id:
        :param a_tags:
        :return:
        """
        self.a_id = a_id
        self.a_tags = a_tags

    @staticmethod
    def get_a_tags_by_content(content):
        pass
