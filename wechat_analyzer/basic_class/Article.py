# coding=utf-8
import datetime

__author__ = 'jayvee'


class Article:
    def __init__(self, a_id, a_title, post_user='unknown', a_tags=dict, a_content='',
                 post_date=datetime.datetime.utcnow(), a_url=None):
        """
        文章的a_tags应该是一个dict，key为tag，value为相应的tag权值
        :param a_id:
        :param a_tags:
        :param a_title:
        :param a_content:
        :param post_date:
        :param post_user:
        :return:
        """
        self.a_id = a_id
        self.a_tags = a_tags
        self.a_content = a_content
        self.a_title = a_title
        self.post_date = post_date
        self.post_user = post_user
        self.a_url = a_url

    @staticmethod
    def get_a_tags_by_content(content):
        pass

    def get_json_object(self):
        return {'article_id': self.a_id, 'article_tags': self.a_tags, 'article_content': self.a_content,
                'article_title': self.a_title, 'article_post_date': str(self.post_date.strftime),
                'article_post_user': self.post_user, 'article_url': self.a_url}
