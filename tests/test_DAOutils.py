# coding=utf-8
import json
import unittest
import urllib
from app import app

__author__ = 'Jayvee'


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        super(TestFlaskApp, self).setUp()
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        super(TestFlaskApp, self).tearDown()
        app.config['TESTING'] = False

    # todo unittest DAO
    def test_insert_user(self):
        post_data = {'openid': 'foo'}
        rv = self.app.post('/api/v1/user', data=json.dumps(post_data))
        self.assertEqual(rv.status_code, 200)
        result = json.loads(rv.data)
        self.assertEqual(result['code'], 0)

    def test_invalid_insert_user(self):
        post_data = {}
        rv = self.app.post('/api/v1/user', data=json.dumps(post_data))
        self.assertEqual(rv.status_code, 500)
        result = json.loads(rv.data)
        self.assertEqual(result['code'], 103)

    def test_insert_article(self):
        post_data = {'media_id': 'test',
                     'items': [{'article_id': 'foo','article_thumb_id':'thumb_id', 'article_url': 'http://trysenz.com', 'article_title': 'test_case',
                                'article_content': '《碟中谍5》中，黑客班吉起初并没把三重保险的门禁放在眼里，'
                                                   '但当他得知必须穿越一套“步态分析系统”时，班吉彻底绝望了，'
                                                   '最后只能靠伊森.亨特屏息3分钟，通过自由式潜水强行入侵后台数据才得以攻破步态分析系统。',
                                'article_post_user': 'pycharm'}], 'update_time': 'flkjasdlkjfa'}
        rv = self.app.post('/api/v1/article', data=json.dumps(post_data))
        result = json.loads(rv.data)
        self.assertEqual(result['code'], 0)

    def test_invalid_insert(self):
        post_data = {'dafda': 'fwew'}
        rv = self.app.post('/api/v1/article', data=json.dumps(post_data))
        result = json.loads(rv.data)
        self.assertEqual(result['code'], 103)
        self.assertEqual(rv.status_code, 500)

    def test_insert_reaction(self):
        get_data = {'openid': 'foo', 'article_id': 'bar', 'redirect_url': 'http://trysenz.com'}
        rv = self.app.get('/api/v1/record?%s' % urllib.urlencode(get_data))
        # result = json.loads(rv.data)
        print rv
        # self.assertEqual(result['code'],0)
        # self.assertEqual(result[''])
