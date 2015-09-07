# coding=utf-8
from sklearn import cross_validation
from passage_classifier.vector_builder import generate_all_trainset, VectorBuilder

__author__ = 'Jayvee'
from sklearn.svm import SVC
from sklearn.externals import joblib

import numpy as np
from sklearn.naive_bayes import MultinomialNB

# svclf = SVC(kernel='rbf')  # default with 'rbf'
# nbclf = MultinomialNB()
testtext = open(r'../data/passages/test').read()
#
result = generate_all_trainset()
#
# svclf.fit(np.array(result[0]), np.array(result[1]))
# nbclf.fit(np.array(result[0]), np.array(result[1]))

vb = VectorBuilder()

svclf = joblib.load('svclf.model')
nbclf = joblib.load('nbclf.model')
pred_svm = svclf.predict(np.array(vb.build_single_vec(testtext)))
pred_nb = nbclf.predict(np.array(vb.build_single_vec(testtext)))
print pred_svm
print pred_nb
print 'score=%s' % cross_validation.cross_val_score(nbclf, np.array(result[0]), np.array(result[1]))


# lr是一个LogisticRegression模型
# joblib.dump(svclf, 'svclf.models')
# joblib.dump(nbclf, 'nbclf.models')
# svclf1 = joblib.load('svclf.models')
#
# pred1 = svclf1.predict(vb.build_single_vec(testtext))
# print pred
# #
#
# def generate_trainset():
