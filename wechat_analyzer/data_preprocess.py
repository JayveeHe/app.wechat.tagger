# coding=utf-8
import codecs
import json
import os
import random
import time
import requests
from gensim_utils import lda_utils
from wechat_analyzer import TaggingUtils
from wechat_analyzer.TaggingUtils import passage_first_level_classify

__author__ = 'jayvee'


def classify_text_files(files_root_path, result_path):
    flist = os.listdir(files_root_path)
    for f in flist:
        print f
        ftext = open('%s/%s' % (files_root_path, f), 'r').read()
        try:
            json_obj = json.loads(ftext)
            result = passage_first_level_classify(json_obj['post_content'])
        except Exception, e:  # 懒得差各种异常了，直接重复
            print e
            continue
        try:
            fout = open('%s/%s/%s' % (result_path, result, f), 'w')
        except Exception, e:
            print e
            os.mkdir('%s/%s' % (result_path, result))
            fout = open('%s/%s/%s' % (result_path, result, f), 'w')
        fout.write(ftext)
        time.sleep(random.random())
    print 'done'


def train_lda_among_classify(class_path, model_outpath):
    lda_model = lda_utils.train_model_by_rootpath(class_path, num_topics=15, iterations=200, passes=20, is_tfidf=False)
    lda_model.save(model_outpath)
    lda_model.print_topics()


if __name__ == '__main__':
    # classify_text_files('./wechat_data/articles', './wechat_data/classify_results')

    # class_type = '财经'
    # train_lda_among_classify('./wechat_data/classify_results/%s' % class_type,
    #                          './wechat_data/lda_in_classify/%s.model' % class_type)
    # lm = lda_utils.loda_ldamodel_by_file('./wechat_data/lda_in_classify/%s.model' % class_type)
    # for i in lm.print_topics():
    #     print i

    test_text = open('./wechat_data/sample.txt', 'r').read()
    TaggingUtils.passage_second_level_classify(test_text)
    base_url = 'weixin.sogou.com'
    url = 'http://weixin.sogou.com//websearch/art.jsp?sg=MZBLgxp1jtW93xM2zcSWTCmO2N_VcC8ziusWwhqgl-UuhBZRcBze0SVUhbI6DjmhT9r9aEWewPWgoT4Owoa-kqhPwaouxIKhWx-l_kL9l1yzp49yOBkpfH1xTes07Z00PRruuatVrlw.&url=p0OVDH8R4SHyUySb8E88hkJm8GF_McJfBfynRTbN8whfbTbm5wLbve9BPtpj-923zP32-c8gmBwB4hsacJSxsGQ3JxMQ3374piIyLRtdUCxh5xIUNFbmG2VTqQzph7dD3MiLWv-Ds3xYy-5x5In7jJFmExjqCxhpkyjFvwP6PuGcQ64lGQ2ZDMuqxplQrsbk'
    print requests.get(url).content