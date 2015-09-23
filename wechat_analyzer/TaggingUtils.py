# coding=utf-8
import json
import os
import gensim
import jieba
import requests
import jieba.posseg as pseg
import sys

__author__ = 'jayvee'

apath = os.path.dirname(__file__)
sys.path.append(apath)
reload(sys)
sys.setdefaultencoding('utf-8')


def passage_first_level_classify(content):
    """
    given a passage content, return its first level class
    :param content:
    :return:
    """
    for i in xrange(3):
        try:
            classify_result = \
                json.loads(requests.post('http://bosonnlp.com/analysis/category', {'data': content}).content)[0]
            class_dict = {0: u'体育', 1: u'教育', 2: u'财经', 3: u'社会',
                          4: u'娱乐', 5: u'军事', 6: u'国内',
                          7: u'科技', 8: '互联网', 9: u'房产', 10: u'国际',
                          11: u'女人', 12: u'汽车', 13: u'游戏'}
            classify_result = class_dict[classify_result]
            return classify_result
        except requests.Timeout, to:
            print to
            continue


def passage_second_level_classify(content):
    """
    given a passage content, return its second level class
    :param content:
    :return: a topic list with probablity
    """
    first_class = passage_first_level_classify(content)
    print first_class
    lda_model = gensim.models.LdaModel.load('%s/wechat_data/lda_in_classify/%s.model' % (apath, first_class))
    word_list = []
    words = pseg.cut(content)
    for item in words:
        if item.flag in [u'n', u'ns']:
            word_list.append(item.word)
    train_set = [word_list]
    dic = gensim.corpora.Dictionary(train_set)
    corpus = [dic.doc2bow(text) for text in train_set]
    doc_lda = lda_model.get_document_topics(corpus)
    count = 0
    # for j in lda_model.print_topics(20):
    #     print count, j
    #     count += 1
    # print doc_lda
    topic_list = []
    for i in lda_model[corpus]:
        for k in i:
            print lda_model.print_topic(k[0], 7), k[1]
            topic_list.append(
                {'topic_tag': u'%s-%s' % (first_class, k[0]), 'topic_content': lda_model.print_topic(k[0], 7),
                 'topic_prob': k[1]})
    return topic_list
