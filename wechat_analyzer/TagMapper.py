# coding=utf-8
__author__ = 'jayvee'

weight_map = {u'娱乐-5': {u'追星族': 0.1, u'电视迷': 0.9},
              u'娱乐-9': {u'追星族': 0.7, u'八卦': 0.3},
              u'娱乐-11': {u'追星族': 0.7, u'八卦': 0.3},
              u'互联网-2': {u'互联网业界': 1}}


def map_atag2utag(atag):
    p = weight_map[atag]
    return p

if __name__ == '__main__':
    print map_atag2utag(u'娱乐-11')
