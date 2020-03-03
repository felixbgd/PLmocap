#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:26:33 2018

@author: bigand
"""

import c3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np
import matplotlib.animation as animation

liaisons = [(20,18),(20,19),(18,17),(17,19),(30,1),(30,2),(22,1),(22,2),(1,6),(6,5),(2,5), \
            (4,3),(3,0),(0,4),(30,31),(31,29),(31,32),(32,29),(32,34),(29,33),(34,33),(33,35), \
            (34,36),(36,35),(22,23),(24,21),(24,23),(23,21),(21,25),(24,26),(25,27),(26,28),(25,26),(27,28)]

liaisons = [(0,2),(1,2),(3,4),(4,6),(6,5),(5,3),(1,7),(7,8),(8,9),(8,10),(9,10),(9,11),(11,12),(12,10), \
            (1,13),(13,14),(14,15),(14,16),(15,16),(15,17),(16,18),(17,18)]

def data_viz3D(data, joints_to_draw=None, frameStop=None, spec_pt=-1, viz="joints", v=[25,125]) : 
    
    sz = data.shape
    if sz[1] == 4 :     # verify the shape of data (xyz, without time column)
        data=data[:,1:4,:]
    if joints_to_draw == None : 
        joints_to_draw = np.arange(np.shape(data)[0])
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca(projection='3d') 
    ax.view_init(v[0],v[1]);    ax.grid(None)
    plt.ion()
    
    numFrame = len(data[0,0,:])     
    if frameStop == None:
        frameStop = numFrame
    
    if viz == "PL" :
        cmarker = 'w'
        ax.set_facecolor('black');   
        
    for i in range(0,frameStop) :
        ax.clear()
        ax.grid(None)
    
        for j in joints_to_draw :
            cmarker = 'b'
            if j == spec_pt :
                cmarker = 'r'
            line=ax.scatter(xs=data[j,0,i], 
                       ys=data[j,1,i],  
                       zs=data[j,2,i],  
                       alpha=0.6, c=cmarker, marker='o')
            ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)'); ax.set_zlabel('Z (m)');
            ax.set_xlim(0,2); ax.set_ylim(-0.5,1.5); ax.set_zlim(0,2)
        if viz == "joints":
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # -1 pour indice python
                ax.plot([data[c1,0,i], data[c2,0,i]], [data[c1,1,i], data[c2,1,i]], [data[c1,2,i], data[c2,2,i]], 'k-', lw=1, c='black')
        ax.set_title('Frame %s' %i)
        plt.draw()
        plt.pause(0.04)
            
def data_viz2D(data, joints_to_draw, frameStop=None, spec_pt=-1, viz="joints") : 
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1) 
    plt.ion()
    
    # Keep only one plan (2D)
    data=data[:,[0,2],:]
    
    numFrame = len(data[0,0,:])     
    if frameStop == None:
        frameStop = numFrame
    
    cmarker = 'b'
    if viz == "PL" :
        cmarker = 'w'
        ax.set_facecolor('black');   
        
    for i in range(0,frameStop) :
        if i % 10 == 0 :    #pour permettre visuo rapide
            ax.clear()
        
            for j in joints_to_draw :
                    if j == spec_pt :
                        cmarker = 'r'
                    ax.scatter(data[j,0,i], data[j,1,i],  c=cmarker, marker='o')
                    ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)');
                    ax.set_xlim(0,2); ax.set_ylim(0,2);
            if viz == "joints":
                for l in liaisons :
                    c1 = l[0];   c2 = l[1]  # -1 pour indice python
                    ax.plot([data[c1,0,i], data[c2,0,i]], [data[c1,1,i], data[c2,1,i]], [data[c1,2,i], data[c2,2,i]], 'k-', lw=1, c='black')
            ax.set_title('Frame %s' %i)
            plt.draw()
            plt.pause(0.1)
            
def plot_frame(data, frame, joints_to_draw = None, spec_pt=-1,viz="3Djoints",save=None) : 
    
    sz = data.shape
    if sz[1] == 4 :     # verify the shape of data (xyz, without time column)
        data=data[:,1:4,:]
        
    if joints_to_draw == None : 
        joints_to_draw = np.arange(np.shape(data)[0])
    
    if viz[:2]=='3D' : 
        fig = plt.figure(figsize=(8,8))
        ax = fig.gca(projection='3d') 
        ax.view_init(25,125)
        ax.grid(False)
        
        for j in joints_to_draw :
            cmarker = 'b'
            if j == spec_pt :
                cmarker = 'r'
            line=ax.scatter(xs=data[j,0,frame], 
                       ys=data[j,1,frame],  
                       zs=data[j,2,frame],  
                       alpha=0.6, c=cmarker, marker='o')
            ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)'); ax.set_zlabel('Z (m)');
            ax.set_xlim(0,2); ax.set_ylim(-0.5,1.5); ax.set_zlim(0,2)
        if viz == "3Djoints":
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # -1 pour indice python
                ax.plot([data[c1,0,frame], data[c2,0,frame]], [data[c1,1,frame], data[c2,1,frame]], [data[c1,2,frame], data[c2,2,frame]], 'k-', lw=1, c='black')
        ax.set_title('Frame %s' %frame)
        
    elif viz[:2] == "PL" :
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(1, 1, 1) 
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)  
        ax.get_yaxis().set_visible(False)
        
        # Keep only one plan (2D)
        data=data[:,[0,2],:]
        
        # Center the image on the pelvis (2)
        Ox = data[2,0,0];   Oy = data[2,1,0]
        
        numFrame = len(data[0,0,:])
        if viz=="PLw" :
            cmarker = 'b'
        else :
            cmarker = 'w'
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
        
        for j in joints_to_draw :
            ax.scatter(data[j,0,frame], data[j,1,frame],  c=cmarker, marker='o')
            ax.set_xlim(Ox-1,Ox+1); ax.set_ylim(Oy-1,Oy+1); ax.invert_xaxis()
            plt.tight_layout(); plt.draw()
            
    if save != None :
        fig.savefig(save, bbox_inches='tight')
        
def compare_frame(data1, data2, label1="data1", label2="data2", save=None) :
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_aspect('equal')
    
    # Keep only one plan (2D)
    data1=data1[:,:,[0,2]]
    data2=data2[:,:,[0,2]]
    
    # Center the image on the pelvis (0)
    Ox1 = data1[0,0,0];   Oy1 = data1[0,0,1]
    Ox2 = data2[0,0,0];   Oy2 = data2[0,0,1]
    
    joints_to_draw = np.arange(np.shape(data1)[1])
    # data1
    cmarker = 'b'

    for j in joints_to_draw :
        if j == joints_to_draw[0]:
            ax.scatter(data1[0,j,0], data1[0,j,1],  c=cmarker, marker='o', alpha = 0.7, label=label1)
        ax.scatter(data1[0,j,0], data1[0,j,1],  c=cmarker, marker='o', alpha = 0.7)
        ax.set_xlim(Ox1-1,Ox1+1); ax.set_ylim(Oy1-0.75,Oy1+1.25); ax.invert_xaxis()
        plt.tight_layout(); plt.draw()
    
    # data2
    cmarker = 'r'

    for j in joints_to_draw :
        if j == joints_to_draw[0]:
            ax.scatter(data2[0,j,0], data2[0,j,1],  c=cmarker, marker='o', alpha = 0.7, label=label2)
        ax.scatter(data2[0,j,0], data2[0,j,1],  c=cmarker, marker='o', alpha = 0.7)
        ax.set_xlim(Ox2-1,Ox2+1); ax.set_ylim(Oy2-0.75,Oy2+1.25); ax.invert_xaxis()
        plt.tight_layout(); plt.draw()
    ax.legend()
            
    if save != None :
        fig.savefig(save, bbox_inches='tight')
        
def compare_allrefs(data_ref, labels, colors, save=None, mean=None, spec_pt=-1) :
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_aspect('equal')
    
    marker = ['o','s','+','*']
            
    # Keep only one plan (2D)
    data_ref=data_ref[:,:,[0,2]]
    
    # Center the image on the pelvis (0)
    Ox = data_ref[:,0,0];   Oy = data_ref[:,0,1]
    
    joints_to_draw = np.arange(np.shape(data_ref)[1])
    sizeMarker=50
    
    for n in range(0,len(labels)) :
        for j in joints_to_draw :
            cmarker = colors[n]
            if j == spec_pt :
                cmarker = 'black'
            if j == joints_to_draw[0]:
                ax.scatter(data_ref[n,j,0], data_ref[n,j,1],  c=cmarker, marker=marker[n], alpha = 0.7, label=labels[n], s=sizeMarker)
            ax.scatter(data_ref[n,j,0], data_ref[n,j,1],  c=cmarker, marker=marker[n], alpha = 0.7, s=sizeMarker)
            ax.set_xlim(Ox[n]-1,Ox[n]+1); ax.set_ylim(Oy[n]-0.75,Oy[n]+1.25); ax.invert_xaxis()
            ax.set_xlabel('X (m)',fontsize=20); ax.set_ylabel('Z (m)',fontsize=20); ax.tick_params(labelsize=15)
            plt.tight_layout(); plt.draw()
            
    if mean is not None :
        mean=mean[:,:,[0,2]]
        OxM = mean[:,0,0];   OyM = mean[:,0,1]
        cmarker = 'black'
        for j in joints_to_draw :
            if j == joints_to_draw[0]:
                ax.scatter(mean[0,j,0], mean[0,j,1],  facecolors='none', edgecolors=cmarker, marker=marker[n], label='mean', s=sizeMarker)
            ax.scatter(mean[0,j,0], mean[0,j,1],  facecolors='none', edgecolors=cmarker, marker=marker[n], s=sizeMarker)
            ax.set_xlim(OxM-1,OxM+1); ax.set_ylim(OyM-0.75,OyM+1.25); ax.invert_xaxis()
            plt.tight_layout(); plt.draw()
    ax.legend(fontsize=12);
            
    if save is not None :
        fig.savefig(save, bbox_inches='tight')
        
def video_PL(data, save, spec_pt=-1, viz="PL"):
    fig = plt.figure(figsize=(8,8))
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)  
    ax.get_yaxis().set_visible(False)
    
    plt.ion()
    
    # Keep only one plan (2D)
    data=data[:,[0,2],:]
    
    # Center the image on the pelvis (0)
    Ox = data[0,0,0];   Oy = data[0,1,0]
    
    joints_to_draw = np.arange(np.shape(data)[0])
    numFrame = len(data[0,0,:])     
    
    cmarker = 'b'
    if viz == "PL" :
        cmarker = 'w'
        ax.set_facecolor('black')
    
    def update_img(i):
        ax.clear()
        
        if viz == "PL" :
            cmarker = 'w'
            ax.set_facecolor('black')
        for j in joints_to_draw :
                if j == spec_pt :
                    cmarker = 'r'
                ax.scatter(data[j,0,i], data[j,1,i],  c=cmarker, marker='o')
                ax.set_xlim(Ox-1,Ox+1); ax.set_ylim(Oy-0.75,Oy+1.25); ax.invert_xaxis()
        plt.tight_layout(); plt.draw()
        return ax
    
    #legend(loc=0)
#            numFrame=min(len(data[0,0,:]),500)
    numFrame=len(data[0,0,:])
        
    ani = animation.FuncAnimation(fig,update_img,numFrame,interval=40)
    writer = animation.writers['ffmpeg'](fps=25)
    writer = animation.FFMpegFileWriter(fps=25)

    
    dpi=200
    print('exporting PL video ... ' )
    ani.save(save, writer=writer, dpi=dpi)
    plt.close()
