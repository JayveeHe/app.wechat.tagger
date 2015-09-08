from gensim import corpora, models
import jieba
import jieba.posseg as pseg

__author__ = 'jayvee'


def get_topics(text, topic_num=10):
    word_list = []
    words = pseg.cut(text)
    for item in words:
        if item.flag in [u'n', u'ns']:
            word_list.append(item.word)
    train_set = [word_list]
    dic = corpora.Dictionary(train_set)
    # dic.save_as_text('lda_dic')
    corpus = [dic.doc2bow(text) for text in train_set]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus, id2word=dic, num_topics=topic_num, iterations=100)
    # lda.save('sogou_reduced_lda.models')
    return lda.print_topics(topic_num, num_words=30)


def get_topic_by_model(text):
    lda = models.LdaModel.load('/Users/jayvee/github_project/jobs/senz.analyzer.texttag/data/lda_models/reduced.model')
    word_list = []
    words = pseg.cut(text)
    for item in words:
        if item.flag in [u'n', u'ns']:
            word_list.append(item.word)
    train_set = [word_list]
    dic = corpora.Dictionary(train_set)
    corpus = [dic.doc2bow(text) for text in train_set]
    doc_lda = lda.get_document_topics(corpus)
    count = 0
    for j in lda.print_topics(20):
        print count, j
        count += 1
    print doc_lda
    for i in lda[corpus]:
        for k in i:
            print lda.print_topic(k[0]),k[1]


if __name__ == '__main__':
    tt = open('../data/sample.txt', 'r')
    get_topic_by_model(tt.read())
