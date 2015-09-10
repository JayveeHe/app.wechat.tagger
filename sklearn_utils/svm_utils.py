# coding=utf-8
from operator import itemgetter
from sklearn import cross_validation
from passage_classifier.vector_builder import generate_all_trainset, VectorBuilder

from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

__author__ = 'Jayvee'
from sklearn.svm import SVC
from sklearn.externals import joblib

import numpy as np
from sklearn.naive_bayes import MultinomialNB

svclf = SVC(kernel='rbf', probability=True)  # default with 'rbf'
nbclf = MultinomialNB()
testtext = open(r'../data/passages/test').read()
#
result = generate_all_trainset()

svclf.fit(np.array(result[0]), np.array(result[1]))
nbclf.fit(np.array(result[0]), np.array(result[1]))



vb = VectorBuilder()

# svclf = joblib.load('svclf.model')
# nbclf = joblib.load('nbclf.model')
pred_svm = svclf.predict(np.array(vb.build_single_vec(testtext)))
pred_nb = nbclf.predict(np.array(vb.build_single_vec(testtext)))
print pred_svm
print pred_nb
# print 'score=%s' % cross_validation.cross_val_score(nbclf, np.array(result[0]), np.array(result[1]))

print svclf.predict_proba(np.array(vb.build_single_vec(testtext)))

# lr是一个LogisticRegression模型
joblib.dump(svclf, '../data/models/svc/svclf.models')
joblib.dump(nbclf, '../data/models/nb/nbclf.models')


# svclf1 = joblib.load('svclf.models')
#
# pred1 = svclf1.predict(vb.build_single_vec(testtext))
# print pred
# #
#
# def generate_trainset():

# def train_svclf():

def grid_search_params(clf, train_x, train_y,param_grid):
    gs = GridSearchCV(clf, param_grid)
    gs.fit(train_x, train_y)
    report(gs.grid_scores_)

# Utility function to report best scores
def report(grid_scores, n_top=3):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
            score.mean_validation_score,
            np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")


param_grid = [
  {'C': [1, 10, 100, 1000], 'kernel': ['linear']},
  {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 ]
grid_search_params(svclf,np.array(result[0]), np.array(result[1]),param_grid)

joblib.dump(svclf, '../data/models/svc/svclf_grid.models')