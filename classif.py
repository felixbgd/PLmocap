#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:51:22 2019

@author: bigand
"""

import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# MULTINOMIAL REGRESSION
def class_logReg(features, labels, label_names, output_dir) :
    
    conf = np.zeros((24,4,4));  proba = np.zeros((24,4,4))
    train_score = np.zeros((24,4));   test_score = np.zeros((24,4))
    for j in range(0,24) :
        testFold = j
        # Determine indexes for LOOO
        indTest = [j, 24+j, 48+j, 72+j]
        indTrain = [e for i, e in enumerate(range(len(labels))) if  not (i in (indTest))]
        test_x = np.array([e for i, e in enumerate(features) if  i in (indTest)])
        test_y = [e for i, e in enumerate(labels) if  i in (indTest)]
        train_x = np.array([e for i, e in enumerate(features) if  i in (indTrain)])
        train_y = [e for i, e in enumerate(labels) if  i in (indTrain)]
        
        mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(train_x, train_y)
        
        proba[j,:] = mul_lr.predict_proba(test_x)
        conf[j,:] = metrics.confusion_matrix(test_y, mul_lr.predict(test_x))
        train_score[j,:] = metrics.accuracy_score(train_y, mul_lr.predict(train_x))
        test_score[j,:] = metrics.accuracy_score(test_y, mul_lr.predict(test_x))
    
    proba_mean = np.average(proba,0)
    conf_mean = np.average(conf,0)
    conf_sdv = np.std(conf,0)
    print("Standard deviations of conf :" + str(np.diag(conf_sdv)))
    
    np.save(output_dir + '/proba_mean',proba_mean)
    
    fig_proba = plt.figure(figsize=(8,8))
    ax = fig_proba.gca()
    im = ax.imshow(proba_mean , clim=(0.0, 1.0))
    fig_proba.colorbar(im, shrink=0.83, orientation='vertical')
    ax.set_xticks(np.arange(4)); ax.set_xticklabels(label_names); ax.set_yticks(np.arange(4)); ax.set_yticklabels(label_names)
    fig_proba.savefig(output_dir + '/proba_matrix.pdf', bbox_inches='tight')
    plt.close()
    
    fig_conf = plt.figure(figsize=(8,8))
    ax = fig_conf.gca()
    im = ax.imshow(conf_mean , clim=(0.0, 1.0))
    fig_conf.colorbar(im, shrink=0.83, orientation='vertical')
    ax.set_xticks(np.arange(4)); ax.set_xticklabels(label_names); ax.set_yticks(np.arange(4)); ax.set_yticklabels(label_names)
    fig_conf.savefig(output_dir + '/conf_matrix.pdf', bbox_inches='tight')
    
    return conf_mean, proba_mean 

# CLUSTERING K-MEANS (in progress)
def cluster_kmeans(features, labels, colors, output_dir) : 
    
    conf = np.zeros((24,4,4));  proba = np.zeros((24,4,4))
    train_score = np.zeros((24,4));   test_score = np.zeros((24,4))
    for j in range(0,24) :
        testFold = j
        # Determine indexes for LOOO
        indTest = [j, 24+j, 48+j, 72+j]
        indTrain = [e for i, e in enumerate(range(len(labels))) if  not (i in (indTest))]
        test_x = np.array([e for i, e in enumerate(features) if  i in (indTest)])
        test_y = [e for i, e in enumerate(labels) if  i in (indTest)]
        train_x = np.array([e for i, e in enumerate(features) if  i in (indTrain)])
        train_y = [e for i, e in enumerate(labels) if  i in (indTrain)]
        
        mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(train_x, train_y)
        kmeans = KMeans(n_clusters=4, random_state=0).fit(train_x)
        clusters=kmeans.labels_
        kmeans.cluster_centers_        
        
        pred = kmeans.predict(test_x)
        conf[j,:] = metrics.confusion_matrix(test_y, pred)
        train_score[j,:] = metrics.accuracy_score(train_y, kmeans.predict(train_x))
        test_score[j,:] = metrics.accuracy_score(test_y, pred)
    
    fig_kmeans = plt.figure(figsize=(8,8))
    ax = fig_kmeans.gca()
    for i in range(4):
        points = np.array([PC_scores[j,:2] for j in range(len(PC_scores)) if clusters[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
        
    