# coding=utf-8
import codecs
import hashlib
import json
import os
import random
import re
import time
import datetime
from urllib import urlencode
import urllib2
from gensim_utils import lda_utils
from wechat_analyzer import tagging_utils
import wechat_analyzer
from wechat_analyzer.tagging_utils import passage_first_level_classify, passage_second_level_classify
import wechat_analyzer.DAO_utils
from  wechat_analyzer.basic_class import Article, Reaction, WechatUser
import requests
import sys

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'jayvee'


def classify_text_files(files_root_path, result_path):
    count = 0
    flist = os.listdir(files_root_path)
    for f in flist:
        print '%s:%s' % (count, f)
        count += 1
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

        time.sleep(random.random()*3)
    print 'done'


def classify_rawtext_files(files_root_path, result_path, pass_num=-1):
    count = 0
    flist = os.listdir(files_root_path)
    for f in flist:

        print '%s:%s' % (count, f)
        count += 1
        if count < pass_num:
            continue
        ftext = codecs.open(os.path.join(files_root_path, f), 'r').read()
        try:
            # json_obj = json.loads(ftext)
            result = passage_first_level_classify(ftext)
        except Exception, e:  # 懒得差各种异常了，直接重复
            print e
            continue
        try:
            fout = codecs.open(os.path.join(result_path, result, f), 'w')
        except Exception, e:
            print e
            os.mkdir(os.path.join(result_path, result))
            fout = codecs.open(os.path.join(result_path, result, f), 'w')
        fout.write(ftext)

        time.sleep(random.random()*3+0.2)
    print 'done'


def train_lda_among_classify(class_path, model_outpath, num_topics=20, iterations=100, passes=10, is_tfidf=False):
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


def process_weixinpage_data(fin_root="/alidata/weichat_article_data/splits/",
                            fout_root="/alidata/weichat_article_data/classified/"):
    """
   处理weixin_page这样的大文件，从网页源码中提取信息

   :param fin_path:
   :return:
   """

    dir_list = os.listdir(fin_root)
    for d in dir_list:
        if not os.path.isdir(os.path.join(fin_root, d)):
            fin = codecs.open(os.path.join(fin_root, d), 'r').read()
            pages = fin.split('</ID>')
            for page in pages:
                try:
                    result = re.compile('<URL>(.*)</URL>').findall(page)
                    url = re.compile('<URL>(.*)</URL>').findall(page)[0]
                    title = re.compile('<TITLE>(.*)</TITLE>').findall(page)[0]
                    post_time = re.compile('<TIME>(.*)</TIME>').findall(page)[0]
                    post_date = re.compile('<DATE>(.*)</DATE>').findall(page)[0]
                    body_result = re.compile('<BODY>(.*)</BODY>', re.S).findall(page)
                    body = body_result[0]
                    soup = BeautifulSoup(body)
                    content_text = ''
                    for item in soup.select('div p'):
                        new_text = item.text.replace('\n', '')
                        new_text = new_text.replace('\r\n', '')
                        content_text += new_text + '\n'

                    print url, title
                    #                    print isinstance(content_text,str)
                    #                    print isinstance(content_text,unicode)
                    fout = codecs.open(os.path.join(fout_root, title), 'w', encoding='utf-8')
                    fout.write(content_text)
                    fout.close()
                except Exception, ie:
                    continue


if __name__ == '__main__':
    # classify_text_files(u'../wechat_crawler/crawl_data/大象公会', './wechat_data/daxiang_result')

    classify_rawtext_files(u'/Users/jayvee/weixin_article/articles/',
                           '/Users/jayvee/weixin_article/classified',131)

    # 生成lda模型
    # class_type = '财经'
    # train_lda_among_classify('./wechat_data/daxiang_result/%s' % class_type,
    #                          './wechat_data/lda_in_more/%s.model' % class_type, num_topics=)
    # lm = lda_utils.loda_ldamodel_by_file('./wechat_data/lda_in_more/%s.model' % class_type)
    # for i in lm.print_topics(num_topics=):
    #     print i

    # test_text = open('./wechat_data/sample.txt', 'r').read()
    # TaggingUtils.passage_second_level_classify(test_text)


    # 整体流程-运行
    # tag_article_and_save(
    #     r'/Users/jayvee/github_project/jobs/app.wechat.tagger/wechat_analyzer/wechat_data/daxiang_result')
    # print urlencode({'redirect_uri': 'http://jiabeigongfang.avosapps.com/jiabei/login'})
    # process_weixinpage_data("/Users/jayvee/weixin_article/weixin_5k.txt")
