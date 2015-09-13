# coding=utf-8
import json
import requests

__author__ = 'jayvee'



def passage_first_level_classify(content):
    """
    given a passage content, return its first level class
    :param content:
    :return:
    """
    classify_result = json.loads(requests.post('http://bosonnlp.com/analysis/category', {'data': content}).content)[0]
    class_dict = {0: u'体育', 1: u'教育', 2: u'财经', 3: u'社会',
                  4: u'娱乐', 5: u'军事', 6: u'国内',
                  7: u'科技', 8: '互联网', 9: u'房产', 10: u'国际',
                  11: u'女人', 12: u'汽车', 13: u'游戏'}
    classify_result = class_dict[classify_result]
    return classify_result






