#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 16:51:22 2019

@author: bigand
"""

import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#####################################################################################
##### ALL THE FUNCTIONS CAN BE USED WITH MOTION MATRIX OF CARTESIAN COORD (XYZ) #####
#####################################################################################

def class_logReg(features, labels, NB_OBS, label_names, C=1, output_dir=None, multiclass='multinomial') :
    ##########################################################################
    ##### Multinomial regression with leave-one-observation-out validation 
    ##### 'features' : feature matrix (Nexamples x Nfeatures)
    ##### 'labels' : label of each example (Nexamples) 
    ##### 'NB_OBS' : number of observations per subject
    ##### 'label_names' : labels names (Nlabel)
    ##### OUTPUTS : confusion and proba matrix + the sklearn regression model
    ##########################################################################
    
    NB_LABEL = len(np.unique(labels)); NB_SUBJ = int( features.shape[0] / NB_OBS )
    conf = np.zeros((NB_OBS,NB_LABEL,NB_LABEL));  proba = np.zeros((NB_OBS,NB_SUBJ,NB_LABEL))
    weights = np.zeros((NB_OBS,NB_LABEL,features.shape[1])); intercept = np.zeros((NB_OBS,NB_LABEL))
    train_score = np.zeros((NB_OBS));   test_score = np.zeros((NB_OBS))
    for j in range(0,NB_OBS) :
        testFold = j
        # Determine indexes for LOOO
        indTest=[]; 
        for subj in range(NB_SUBJ) : indTest.append(subj*NB_OBS+j)
        indTrain = [e for i, e in enumerate(range(len(labels))) if  not (i in (indTest))]
        test_x = np.array([e for i, e in enumerate(features) if  i in (indTest)])
        test_y = [e for i, e in enumerate(labels) if  i in (indTest)]
        train_x = np.array([e for i, e in enumerate(features) if  i in (indTrain)])
        train_y = [e for i, e in enumerate(labels) if  i in (indTrain)]
        
        if multiclass=='multinomial': mul_lr = linear_model.LogisticRegression(multi_class=multiclass,solver='newton-cg',C=C).fit(train_x, train_y)
        if multiclass=='ovr': mul_lr = linear_model.LogisticRegression(multi_class=multiclass,C=C).fit(train_x, train_y)
        
        weights[j,:,:] = mul_lr.coef_
        intercept[j,:] = mul_lr.intercept_
        proba[j,:,:] = mul_lr.predict_proba(test_x)
        conf[j,:,:] = metrics.confusion_matrix(test_y, mul_lr.predict(test_x))
        conf[j,:,:] /= np.sum(conf[j,:,:],axis=1)[:,None]
        test_score[j] = np.average(np.diag(conf[j,:,:]))
        train_score[j] = metrics.accuracy_score(train_y, mul_lr.predict(train_x))
     
    weights_mean = np.average(weights,0)
    intercept_mean = np.average(intercept,0)
    proba_mean = np.average(proba,0)
    conf_mean = np.average(conf,0)
    conf_sdv = np.std(conf,0)
    
    if output_dir != None:
        np.save(output_dir + '/conf_MLR_m',conf_mean)
        np.save(output_dir + '/proba_MLR_m',proba_mean)
        
        fig_proba = plt.figure(figsize=(8,8))
        ax = fig_proba.gca()
        im = ax.imshow(proba_mean , clim=(0.0, 1.0))
        fig_proba.colorbar(im, shrink=0.83, orientation='vertical')
        ax.set_xticks(np.arange(NB_LABEL)); ax.set_xticklabels(label_names); ax.set_yticks(np.arange(NB_LABEL)); ax.set_yticklabels(label_names)
        fig_proba.savefig(output_dir + '/proba_MLR_m.pdf', bbox_inches='tight')
        plt.close()
        
        fig_conf = plt.figure(figsize=(8,8))
        ax = fig_conf.gca()
        im = ax.imshow(conf_mean , clim=(0.0, 1.0))
        fig_conf.colorbar(im, shrink=0.83, orientation='vertical')
        ax.set_xticks(np.arange(NB_LABEL)); ax.set_xticklabels(label_names); ax.set_yticks(np.arange(NB_LABEL)); ax.set_yticklabels(label_names)
        fig_conf.savefig(output_dir + '/conf_MLR_m.pdf', bbox_inches='tight')
    
    return weights_mean, intercept_mean, conf_mean, proba_mean, test_score, mul_lr


# def crossval_logReg(features, labels, NB_OBS, label_names, c_values=np.hstack((0,10**np.arange(-4.0,5.0))), output_dir=None, multiclass='multinomial') :
#     ##########################################################################
#     ##### Multinomial regression with leave-one-observation-out validation 
#     ##### 'features' : feature matrix (Nexamples x Nfeatures)
#     ##### 'labels' : label of each example (Nexamples) 
#     ##### 'NB_OBS' : number of observations per subject
#     ##### 'label_names' : labels names (Nlabel)
#     ##### OUTPUTS : confusion and proba matrix + the sklearn regression model
#     ##########################################################################
    
#     print("Performing LOOO Cross-validation LogReg...")
#     NB_C = len(c_values)
#     NB_LABEL = len(np.unique(labels)); NB_SUBJ = int( features.shape[0] / NB_OBS )
#     conf = np.zeros((NB_OBS,NB_C,NB_LABEL,NB_LABEL));  # proba = np.zeros((NB_OBS,NB_SUBJ,NB_LABEL))
#     # weights = np.zeros((NB_OBS,NB_LABEL,features.shape[1])); intercept = np.zeros((NB_OBS,NB_LABEL))
#     cv_score = np.zeros((NB_OBS,NB_C))
#     for j in range(0,NB_OBS) :
#         print('LOOO fold ' + str(j+1))
#         testFold = j
#         # Determine indexes for LOOO
#         indTest=[]; 
#         for subj in range(NB_SUBJ) : indTest.append(subj*NB_OBS+j)
#         indTrain = [e for i, e in enumerate(range(len(labels))) if  not (i in (indTest))]
#         test_x = np.array([e for i, e in enumerate(features) if  i in (indTest)])
#         test_y = [e for i, e in enumerate(labels) if  i in (indTest)]
#         train_x = np.array([e for i, e in enumerate(features) if  i in (indTrain)])
#         train_y = [e for i, e in enumerate(labels) if  i in (indTrain)]
        
#         for i in range(NB_C):
#             mul_lr = linear_model.LogisticRegression(multi_class=multiclass, solver='newton-cg',C=c_values[i]).fit(train_x, train_y)
        
#             conf[j,i,:,:] = metrics.confusion_matrix(test_y, mul_lr.predict(test_x))
#             conf[j,i,:,:] /= np.sum(conf[j,i,:,:],axis=1)[:,None]
#             cv_score[j,i] = metrics.accuracy_score(test_y, mul_lr.predict(test_x))
     
#     # conf_mean = np.average(conf,0)
#     # conf_sdv = np.std(conf,0)
    
#     return cv_score


def class_SVM(features, labels, label_names, output_dir, kernel = 'linear') :

    NB_LABEL = len(np.unique(labels)); NB_IM = int( features.shape[0] / NB_LABEL )
    conf = np.zeros((NB_IM,NB_LABEL,NB_LABEL)); 
    train_score = np.zeros((NB_IM,NB_LABEL));   test_score = np.zeros((NB_IM,NB_LABEL))
    for j in range(0,NB_IM) :
        testFold = j
        # Determine indexes for LOOO
        indTest=[]; 
        for lab in range(NB_LABEL) : indTest.append(lab*NB_IM+j)
        indTrain = [e for i, e in enumerate(range(len(labels))) if  not (i in (indTest))]
        test_x = np.array([e for i, e in enumerate(features) if  i in (indTest)])
        test_y = [e for i, e in enumerate(labels) if  i in (indTest)]
        train_x = np.array([e for i, e in enumerate(features) if  i in (indTrain)])
        train_y = [e for i, e in enumerate(labels) if  i in (indTrain)]
                
        svm_model = SVC(kernel = kernel, C = 1).fit(train_x, train_y) 
        conf[j,:] = metrics.confusion_matrix(test_y, svm_model.predict(test_x))
    
        train_score[j,:] = metrics.accuracy_score(train_y, svm_model.predict(train_x))
        test_score[j,:] = metrics.accuracy_score(test_y, svm_model.predict(test_x))
        
    conf_mean = np.average(conf,0)
    conf_sdv = np.std(conf,0)
    
    np.save(output_dir + '/conf_SVM_m',conf_mean)

    fig_conf = plt.figure(figsize=(8,8))
    ax = fig_conf.gca()
    im = ax.imshow(conf_mean , clim=(0.0, 1.0))
    fig_conf.colorbar(im, shrink=0.83, orientation='vertical')
    ax.set_xticks(np.arange(NB_LABEL)); ax.set_xticklabels(label_names); ax.set_yticks(np.arange(NB_LABEL)); ax.set_yticklabels(label_names)
    fig_conf.savefig(output_dir + '/conf_SVM_m.pdf', bbox_inches='tight')
    
    return conf_mean, svm_model
    

# CLUSTERING K-MEANS (in progress)
#def cluster_kmeans(features, labels, colors, output_dir) : 
#    
#    conf = np.zeros((NB_IM,4,4));  proba = np.zeros((NB_IM,4,4))
#    train_score = np.zeros((NB_IM,4));   test_score = np.zeros((NB_IM,4))
#    for j in range(0,NB_IM) :
#        testFold = j
#        # Determine indexes for LOOO
#        indTest = [j, 24+j, 48+j, 72+j]
#        indTrain = [e for i, e in enumerate(range(len(labels))) if  not (i in (indTest))]
#        test_x = np.array([e for i, e in enumerate(features) if  i in (indTest)])
#        test_y = [e for i, e in enumerate(labels) if  i in (indTest)]
#        train_x = np.array([e for i, e in enumerate(features) if  i in (indTrain)])
#        train_y = [e for i, e in enumerate(labels) if  i in (indTrain)]
#        
#        mul_lr = linear_model.LogisticRegression(multi_class='multinomial', solver='newton-cg').fit(train_x, train_y)
#        kmeans = KMeans(n_clusters=4, random_state=0).fit(train_x)
#        clusters=kmeans.labels_
#        kmeans.cluster_centers_        
#        
#        pred = kmeans.predict(test_x)
#        conf[j,:] = metrics.confusion_matrix(test_y, pred)
#        train_score[j,:] = metrics.accuracy_score(train_y, kmeans.predict(train_x))
#        test_score[j,:] = metrics.accuracy_score(test_y, pred)
#    
#    fig_kmeans = plt.figure(figsize=(8,8))
#    ax = fig_kmeans.gca()
#    for i in range(4):
#        points = np.array([PC_scores[j,:2] for j in range(len(PC_scores)) if clusters[j] == i])
#        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
        
    