# coding=utf-8
import json
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from tencent_qcloud_classifier.QcloudApi.qcloudapi import QcloudApi
from wechat_analyzer.content_extractor import Extractor

__author__ = 'jayvee'


def wenzhi_analysis(content):
    """
    使用腾讯文智文本分类接口进行分析，得出
    :param content:
    :return:
    """
    module = 'wenzhi'
    action = 'TextClassify'
    config = {
        'Region': 'sz',
        'secretId': 'AKIDi1ohL0zeMXuUaxEwGHMgd2aXeQYqnYJS',
        'secretKey': 'oUEND16w54I8i6uragtks71EFK70hg8a',
        'method': 'post'
    }
    params = {
        'content': content
    }
    try:
        service = QcloudApi(module, config)
        req_url = service.generateUrl(action, params)
        # print req_url
        # result_str = requests.get(req_url)
        result_str = service.call(action, params)
        print result_str
        result = json.loads(result_str)
        return result
    except Exception, e:
        print e


def wenzhi_analyse_url(text_url):
    ext = Extractor(url=text_url, blockSize=5,
                    image=False)
    content = ext.getContext().decode('utf8').strip()
    return wenzhi_analysis(content)


if __name__ == '__main__':
    # url = 'http://mp.weixin.qq.com/s?__biz=MjAzNzMzNTkyMQ==&mid=402031652&idx=1&sn=f3b8e58b619bbe10fe0406be1cb540ef&scene=1&srcid=11301THOCp95sKFG4ldOvFSJ&key=ff7411024a07f3ebcade56e8ee0470843efef32d445949817e160e80722d57ad905e082811b608139e37fc70967edf4a&ascene=0&uin=NDEyNTkyMzIw&devicetype=iMac+MacBookAir7%2C2+OSX+OSX+10.11.1+build(15B42)&version=11020201&pass_ticket=xm0O%2FtPczdx0F15%2FojqXcvifw%2FIv9I1gwuxCqTLasDeybKwZvJI57cGvHsYMq4EF'
    # ext = Extractor(url=url, blockSize=5,
    #                 image=False)
    # content = ext.getContext().decode('utf8').strip()
    # print json.dumps(wenzhi_analysis(content), ensure_ascii=False)
    pass
