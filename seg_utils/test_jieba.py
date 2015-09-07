# coding=utf-8
__author__ = 'Jayvee'
import jieba
import jieba.analyse

content = open('../data/trainset', 'r').read()
tags = jieba.analyse.textrank(content, topK=10, withWeight=True, allowPOS=('ns', 'n', 'vn', 'v'))
for tag in tags:
    print '%s,%s' % (tag[0], tag[1])

print '-------------'
tags = jieba.analyse.extract_tags(content, topK=10)
for tag in tags:
    print '%s' % tag
