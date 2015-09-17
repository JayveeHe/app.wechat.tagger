# coding=utf-8
import json
import os
import re
from wechat_analyzer import TaggingUtils
import sys
from wechat_analyzer.basic_class.Article import Article
from wechat_analyzer.basic_class.Reaction import Reaction
from wechat_analyzer.basic_class.WechatUser import WechatUser
import wechat_analyzer.TagMapper

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'jayvee'

fpath = os.path.dirname(__file__)
print 'demo_main, path:' + fpath

weight_map = {u'娱乐-5': {u'追星族': 0.1, u'电视迷': 0.9},
              u'娱乐-9': {u'追星族': 0.7, u'八卦': 0.3},
              u'娱乐-11': {u'追星族': 0.7, u'八卦': 0.3},
              u'互联网-2': {u'互联网业界': 1},
              u'体育-4': {u'体育装备': 0.7, u'体育历史': 0.3},
              u'体育-6': {u'体育新闻': 1},
              u'体育-11': {u'体育装备': 0.2, u'体育历史': 0.8},
              u'军事-10': {u'军事轶事': 1},
              u'军事-11': {u'军事历史': 0.9, u'军事新闻': 0.1}}


def show_content_topic_prob(text_path):
    test_text = open(text_path, 'r').read()
    topics = TaggingUtils.passage_second_level_classify(test_text)
    for i in topics:
        print i['topic_tag'], i['topic_prob']
    return topics


def user_vec_update(user, u_tags_updates):
    pass


def init_articles():
    rootpath = '%s/demo_articles' % fpath
    article_map = {}
    for f in os.listdir(rootpath):
        print f
        topics = show_content_topic_prob(os.path.join(rootpath, f))
        a_tags = {}
        for i in topics:
            a_tags[i['topic_tag']] = i['topic_prob']

        article_map[f] = Article(f, a_tags=a_tags)
    return article_map


if __name__ == '__main__':
    # rootpath = '/Users/jayvee/github_project/jobs/app.wechat.tagger/wechat_analyzer/demo_related/demo_articles'
    # for f in os.listdir(rootpath):
    #     print f
    #     show_content_topic_prob(os.path.join(rootpath, f))

    a_map = init_articles()
    wechat_user = WechatUser('123', [], {}, {}, {})
    reaction = Reaction('333', 'read', 'TFBOYS为什么这样红 | 大象公会.txt', '123')
    print json.dumps(wechat_user.user_tagging([reaction], weight_map, a_map=a_map), ensure_ascii=False)
    reaction = Reaction('334', 'read', '球衣往事 | 大象公会.txt', '123')
    print json.dumps(wechat_user.user_tagging([reaction], weight_map, a_map=a_map), ensure_ascii=False)
    reaction = Reaction('334', 'read', '体育与阶层 | 大象公会.txt', '123')
    print json.dumps(wechat_user.user_tagging([reaction], weight_map, a_map=a_map), ensure_ascii=False)
