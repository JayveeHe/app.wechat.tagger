# coding=utf-8
import codecs
import hashlib
import json
import os
import random
import time
import datetime
from urllib import urlencode
import urllib2
from gensim_utils import lda_utils
from wechat_analyzer import TaggingUtils
import wechat_analyzer
from wechat_analyzer.TaggingUtils import passage_first_level_classify, passage_second_level_classify
import wechat_analyzer.DAO_utils
from  wechat_analyzer.basic_class import Article, Reaction, WechatUser
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'jayvee'


def classify_text_files(files_root_path, result_path):
    flist = os.listdir(files_root_path)
    for f in flist:
        print f
        ftext = codecs.open('%s/%s' % (files_root_path, f), 'r').read()
        try:
            json_obj = json.loads(ftext)
            result = passage_first_level_classify(json_obj['post_content'])
        except Exception, e:  # 懒得差各种异常了，直接重复
            print e
            continue
        try:
            fout = codecs.open('%s/%s/%s' % (result_path, result, f), 'w')
        except Exception, e:
            print e
            os.mkdir('%s/%s' % (result_path, result))
            fout = codecs.open('%s/%s/%s' % (result_path, result, f), 'w')
        fout.write(ftext)
        time.sleep(random.random())
    print 'done'


def train_lda_among_classify(class_path, model_outpath, num_topics=15, iterations=200, passes=20, is_tfidf=False):
    lda_model = lda_utils.train_model_by_rootpath(class_path, num_topics=num_topics, iterations=iterations,
                                                  passes=passes, is_tfidf=is_tfidf)
    lda_model.save(model_outpath)
    lda_model.print_topics()


# 整体流程
# 准备一个文章库，分类并打tag
def tag_article_and_save(root_path):
    dir_list = os.listdir(root_path)
    for d in dir_list:
        if os.path.isdir(os.path.join(root_path, d)):
            flist = os.listdir(os.path.join(root_path, d))
            for f in flist:
                if os.path.isfile(os.path.join(root_path, d, f)):
                    print 'processing %s ...' % f
                    fjson = json.loads(open(os.path.join(root_path, d, f)).read())
                    content = fjson['post_content']
                    post_date = datetime.datetime.strptime(fjson['post_date'], '%Y-%m-%d')
                    post_title = fjson['post_title']
                    post_user = fjson['post_user']
                    a_tags_list = passage_second_level_classify(content)
                    a_tags = {}
                    for topic in a_tags_list:
                        a_tags[topic['topic_tag']] = topic['topic_prob']
                    a_id = hashlib.md5(post_title + fjson['post_date']).hexdigest()
                    article = Article.Article(a_id, post_title, post_user, a_tags, content, post_date)
                    wechat_analyzer.DAO_utils.mongo_insert_article(article)


if __name__ == '__main__':
    # classify_text_files(u'../wechat_crawler/crawl_data/大象公会', './wechat_data/daxiang_result')

    # 生成lda模型
    # class_type = '财经'
    # train_lda_among_classify('./wechat_data/daxiang_result/%s' % class_type,
    #                          './wechat_data/lda_in_more/%s.model' % class_type, num_topics=18)
    # lm = lda_utils.loda_ldamodel_by_file('./wechat_data/lda_in_more/%s.model' % class_type)
    # for i in lm.print_topics(num_topics=50):
    #     print i

    # test_text = open('./wechat_data/sample.txt', 'r').read()
    # TaggingUtils.passage_second_level_classify(test_text)


    # 整体流程-运行
    # tag_article_and_save(
    #     r'/Users/jayvee/github_project/jobs/app.wechat.tagger/wechat_analyzer/wechat_data/daxiang_result')
    print urlencode({'redirect_uri': 'http://jiabeigongfang.avosapps.com/jiabei/login'})
