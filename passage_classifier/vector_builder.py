# coding=utf-8
import codecs
import os
from gensim import corpora, models, similarities
import jieba

__author__ = 'Jayvee'
import jieba.posseg as pseg

proj_path = os.path.dirname(os.path.dirname(__file__))


class VectorBuilder:
    def __init__(self, base_vec_path='%s/data/allvec_500.txt' % proj_path,
                 tfidf_path='%s/data/tfidf.model' % proj_path,
                 dic_path='%s/data/lda_dic' % proj_path,
                 stoplist_path='%s/data/WordFilter.dic' % proj_path):
        allvec_in = open(base_vec_path, 'r')
        self.base_vec = {}
        for input_line in allvec_in:
            word = input_line.split('\t')[1].replace('word=', '').decode('utf8')
            self.base_vec[word] = 0

        self.tfidf_model = models.TfidfModel.load(tfidf_path)
        self.dic = corpora.Dictionary.load(dic_path)
        self.stoplist = []
        for stopline in open(stoplist_path, 'r'):
            self.stoplist.append(stopline.strip())

    def build_base_tfidf_vec(self, root_dir_path, vec_size=100, encoding='utf8'):
        train_set = []
        stoplist = []
        for line in open('../data/WordFilter.dic', 'r'):
            stoplist.append(line.strip())
        walk = os.walk(root_dir_path)
        dcount = 0
        fcount = 0
        for root, dirs, files in walk:
            print 'dir count = %s' % dcount
            print root
            for name in files:
                print 'file count = %s' % fcount
                # print name
                try:
                    f = codecs.open(os.path.join(root, name), 'r', encoding='gbk')
                    raw = f.read()
                except Exception, e:
                    print 'error file name = %s' % name
                    continue
                word_list = []
                words = pseg.cut(raw)
                for item in words:
                    # if item.word not in stoplist and item.flag in [u'v', u'vn', u'n', u'ns']:
                    #     word_list.append(item.word)
                    # if item.flag in [u'v', u'vn', u'n', u'ns']:
                    #     word_list.append(item.word)
                    word_list.append(item.word)
                # word_list = list(jieba.cut(raw, cut_all=False))
                train_set.append(word_list)
                fcount += 1
            dcount += 1
        dic = corpora.Dictionary(train_set)
        dic.save('lda_dic')
        corpus = [dic.doc2bow(text) for text in train_set]
        tfidf = models.TfidfModel(corpus, id2word=dic)
        tfidf.save('tfidf.models')
        corpus_tfidf = tfidf[corpus]
        return tfidf

    def get_class_top_tfidf(self, class_path):
        stoplist = []
        for line in open('../data/WordFilter.dic', 'r'):
            stoplist.append(line.strip())
        walk = os.walk(class_path)
        dcount = 0
        fcount = 0
        word_list = []
        # dic = corpora.Dictionary.load('lda_dic')
        # tfidf = models.TfidfModel.load('tfidf.models')
        for root, dirs, files in walk:
            print 'dir count = %s' % dcount
            # print root
            for name in files:
                print 'file count = %s' % fcount
                # print name
                try:
                    f = codecs.open(os.path.join(root, name), 'r', encoding='gbk')
                    raw = f.read()
                    # class_text += raw + '\n'
                except Exception, e:
                    print 'error file name = %s' % name
                    continue

                words = pseg.cut(raw)
                for item in words:
                    # if item.word not in stoplist and item.flag in [u'v', u'vn', u'n', u'ns'] and len(item.word) > 1:
                    #     word_list.append(item.word)
                    if item.flag in [u'v', u'vn', u'n', u'ns'] and len(item.word) > 1:
                        word_list.append(item.word)
                        # if item.flag in [u'v', u'vn', u'n', u'ns']:
                        #     word_list.append(item.word)
                        # word_list.append(item.word)
                # word_list = list(jieba.cut(raw, cut_all=False))
                # train_set.append(word_list)
                fcount += 1
            dcount += 1

        vec_bow = self.dic.doc2bow(word_list)  # 把商品描述转为词包
        vec_tfidf = self.tfidf_model[vec_bow]
        result_list = []
        for i in vec_tfidf:
            result_list.append((self.tfidf_model.id2word[i[0]], i[1]))
            # print 'word=%s\ttfidf=%0.8f' % (tfidf.id2word[i[0]], i[1])
            # print vec_tfidf
        result_list.sort(lambda x, y: -cmp(x[1], y[1]))
        for i in xrange(500):
            try:
                word = result_list[i][0]
                tfidf_value = result_list[i][1]
                print 'rank=%s\tword=%s\ttfidf=%0.12f' % (i, word, tfidf_value)
            except Exception, e:
                # print e
                continue
        return result_list

    def build_single_vec(self, text):
        from copy import deepcopy

        temp_vec = deepcopy(self.base_vec)
        vec_bow = self.dic.doc2bow(jieba.cut(text))  # 把商品描述转为词包
        vec_tfidf = self.tfidf_model[vec_bow]
        count = 0
        for tfidf_item in vec_tfidf:
            word = self.tfidf_model.id2word[tfidf_item[0]]
            if temp_vec.has_key(word):
                temp_vec[word] = tfidf_item[1]
                count += 1
        result_vec = []
        for key in temp_vec:
            result_vec.append(temp_vec[key])
        print 'has value:%s' % count
        return result_vec

    def build_base_vec(self, root_path, fout_path):
        result_list = []
        fout = open(fout_path, 'w')
        for i in xrange(1, 11):
            result = self.get_class_top_tfidf(r'D:\CS\TrainSet\SogouC_Reduced\%s' % i)
            result_list.extend(result)
            for i in xrange(500):
                try:
                    word = result[i][0]
                    tfidf_value = result[i][1]
                    print 'rank=%s\tword=%s\ttfidf=%0.12f' % (i, word, tfidf_value)
                    fout.write('rank=%s\tword=%s\ttfidf=%0.12f' % (i, word, tfidf_value))
                except Exception, e:
                    # print e
                    continue

        return result_list


        ####################### old version #####################
        # walk = os.walk(root_path)
        # fout = open(fout_path, 'w')
        # vb = VectorBuilder()
        # for root, dirs, files in walk:
        #     for name in files:
        #         print name
        #         try:
        #             f = codecs.open(os.path.join(root, name), 'r', encoding='gbk')
        #             raw = f.read()
        #             # x_vec = vb.build_single_vec(raw)
        #             vec_bow = self.dic.doc2bow(jieba.cut(raw))  # 把商品描述转为词包
        #             vec_tfidf = self.tfidf_model[vec_bow]
        #             vec_tfidf = vec_tfidf.sort(lambda x, y: cmp(x[1], y[1]))
        #             result_list = []
        #             index = 0
        #             for i in vec_tfidf:
        #                 word = self.tfidf_model.id2word[i[0]]
        #                 tfidf = i[1]
        #                 result_list.append((word, tfidf))
        #                 fout.write('%s\tword=%s\ttfidf=%s\n' % (index, word, tfidf))
        #                 index += 1
        #                 if index > 500:
        #                     break
        #         except Exception, e:
        #             print 'error file name = %s' % name
        #             continue
        # print 'done'


def generate_trainset(raw_train_text_root, label_index):
    vb = VectorBuilder()
    # print vb.build_single_vec('腾讯喜欢投资球队')
    x_result = []
    y_result = []
    walk = os.walk(raw_train_text_root)
    for root, dirs, files in walk:
        for name in files:
            print name
            try:
                f = codecs.open(os.path.join(root, name), 'r', encoding='gbk')
                raw = f.read()
                x_vec = vb.build_single_vec(raw)
                y_label = label_index
                x_result.append(x_vec)
                y_result.append(y_label)
                # class_text += raw + '\n'
            except Exception, e:
                print 'error file name = %s' % name
                continue
                # print root, dirs, files
    return (x_result, y_result)


def generate_all_trainset(rootpath='/Users/jayvee/Desktop/data'):
    all_x = []
    all_y = []
    for i in xrange(1, 11):
        print 'label = %s' % i
        i_result_tuple = generate_trainset('%s/%s/' % (rootpath,i), i)
        all_x.extend(i_result_tuple[0])
        all_y.extend(i_result_tuple[1])
    return all_x, all_y


def generate_class_ave_vec(class_root_path):
    """
    为文章分类百分比服务，计算每一类的中心向量
    :param class_root_path:
    :return:
    """
    walk = os.walk(class_root_path)
    vecbuilder = VectorBuilder()
    class_vec = vecbuilder.build_single_vec('')
    filecount = 0
    for root, dirs, files in walk:
        for name in files:
            print name
            try:
                f = codecs.open(os.path.join(root, name), 'r', encoding='gbk')
                raw = f.read()
                x_vec = vecbuilder.build_single_vec(raw)
                for i_coord in xrange(len(class_vec)):
                    class_vec[i_coord] += x_vec[i_coord]
                filecount += 1
            except Exception, e:
                print 'error file name = %s' % name
                continue
    # average
    for vec_coord in class_vec:
        vec_coord /= filecount
    return class_vec


def generate_all_class_ave_vec(root_path):
    flist = os.listdir(root_path)
    for dir_path in flist:
        if os.path.isdir(root_path + dir_path):
            print dir_path
            class_vec = generate_class_ave_vec(root_path + dir_path + '/')
            fout = open('../data/ave_vec_%s.txt' % dir_path, 'w')
            for i in class_vec:
                fout.write('%f\t' % i)
    print 'done'



if __name__ == '__main__':
    # get class ave center point

    # cv = generate_class_ave_vec('/Users/jayvee/Downloads/SogouC.reduced/Reduced/C000008/')
    # fout = open('../data/ave_vec_8.txt', 'w')
    # for i in cv:
    #     fout.write('%f\t' % i)
    #
    # print 'done'

    generate_all_class_ave_vec('/Users/jayvee/Downloads/SogouC.reduced/Reduced/')

    # vb = VectorBuilder()
    # print vb.build_single_vec('腾讯喜欢投资球队')

    # result_tuple = generate_trainset(r'D:\CS\TrainSet\SogouC_Reduced\2', 2)

    # result = generate_all_trainset()

    # vb.build_base_vec(r'D:\CS\TrainSet\SogouC_Reduced', '../data/all_vec_500.txt')

    # for x in result_tuple[0]:
    #     for i in x:
    #         if i != 0:
    #             print i
    # print result_tuple
    pass
    # build_base_tfidf_vec('D:\CS\Java\SogouC.reduced.20061127\SogouC.reduced\Reduced')
    # dic = corpora.Dictionary.load_from_text('D:\CS\Git\Jobs\senz.analyzer.texttag\gensim_utils\lda_dic')
    # corpus = corpora
    # print dic.num_docs
    # dic.doc2bow()
    # test = ''
    # dic = corpora.Dictionary.load('lda_dic')
    # tfidf = models.TfidfModel.load('tfidf.models')
    # vec_bow = dic.doc2bow(jieba.cut(test))  # 把商品描述转为词包
    # vec_tfidf = tfidf[vec_bow]
    # # vec_tfidf = vec_tfidf.sort(lambda x, y: cmp(x[1], y[1]))
    # result_list = []
    # for i in vec_tfidf:
    #     result_list.append((tfidf.id2word[i[0]], i[1]))
    #     # print 'word=%s\ttfidf=%0.8f' % (tfidf.id2word[i[0]], i[1])
    #     # print vec_tfidf
    #     # tfidf = models.TfidfModel(id2word=dic, dictionary=dic)
    # result_list.sort(lambda x, y: -cmp(x[1], y[1]))
    # for j in result_list:
    #     print 'word=%s\ttfidf=%0.12f' % (j[0], j[1])
    # allresult = set()
    # for i in range(1, 11):
    #     class_result = VectorBuilder.get_class_top_tfidf(r'D:\CS\TrainSet\SogouC_Reduced\%s' % i)
    #     for item in class_result:
    #         allresult.add(item[0])
    # fout = open('allvec1.out', 'w')
    # for line in list(allresult):
    #     fout.write(line + '\n')
    # fout.write(json.dumps(list(allresult), ensure_ascii=False))
    # get_class_top_tfidf(r'D:\CS\TrainSet\SogouC_Reduced\2')
