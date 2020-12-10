#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  7 11:26:33 2018

@author: bigand
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np
import matplotlib.animation as animation

#####################################################################################
##### ALL THE FUNCTIONS CAN BE USED WITH MOTION MATRIX OF CARTESIAN COORD (XYZ) #####
#####################################################################################

def data_viz3D(data, frameStop=None, spec_pt=-1, viz="PL", view=[25,125],liaisons=None, center_sens=0) : 
    ##########################################################################
    ##### Animated visualization of mocap data in the 3D space
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 3
    ##### Reads until the end, or 'frameStop', can highlight 'spec_pt' sensor
    ##### "PL" (point-light) or "joints" display (then specify 'liaisons')
    ##### Beware of adjusting the Kx, Ky, Kz scale factors in the code
    ##########################################################################
    
    joints_to_draw = np.arange(np.shape(data)[0])
    
    # Center the image
    Ncenter = center_sens     # e.g. pelvis marker
    Ox = data[Ncenter,0,0];   Oy = data[Ncenter,1,0];   Oz = data[Ncenter,2,0]
    maxX = (data[:,0,:]-Ox).max(); maxY = (data[:,1,:]-Oy).max(); maxZ = (data[:,2,:]-Oz).max()
    
    # Adjust your scale along the 3 axis 
    Kx = 3; Ky = 5; Kz = 1.25;
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca(projection='3d') 
    ax.view_init(view[0],view[1]);    ax.grid(None)
    plt.ion()
    
    numFrame = len(data[0,0,:])     
    if frameStop == None:
        frameStop = numFrame
        
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
            ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.set_zlim(Oz-Kz*maxZ,Oz+Kz*maxZ)
        if viz == "joints":
            assert(liaisons!=None)
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  
                ax.plot([data[c1,0,i], data[c2,0,i]], [data[c1,1,i], data[c2,1,i]], [data[c1,2,i], data[c2,2,i]], 'k-', lw=1, c='black')
        ax.set_title('Frame %s' %i)
        plt.draw()
        plt.pause(0.04)
        
            
def data_viz2D(data, frameStop=None, spec_pt=-1, viz="PL",liaisons=None, center_sens=0) : 
    ##########################################################################
    ##### Animated visualization of mocap data in the 2D frontal plane
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 2 or 3
    ##### Reads until the end, or 'frameStop', can highlight 'spec_pt' sensor
    ##### "PL" (point-light) or "joints" display (then specify 'liaisons')
    ##### Beware of adjusting the Kx & Kz scale factors in the code
    ##########################################################################
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1) 
    plt.ion()
    
    # Keep only one plan (2D)
    if data.shape[1] == 3 :
        data=data[:,[0,2],:]    # frontal plane (X-Z)
    joints_to_draw = np.arange(np.shape(data)[0])
    
    # Center the image
    Ncenter = center_sens    # e.g. pelvis marker
    Ox = data[Ncenter,0,0];   Oz = data[Ncenter,1,0];
    maxX = (data[:,0,:]-Ox).max(); maxZ = (data[:,1,:]-Oz).max();
    
    # Adjust your scale along the 3 axis 
    Kx = 3; Kz = 1.25;

    numFrame = len(data[0,0,:])     
    if frameStop == None:
        frameStop = numFrame
           
    for i in range(0,frameStop) :
        ax.clear()
    
        for j in joints_to_draw :
            cmarker = 'b' 
            if j == spec_pt :
                cmarker = 'r'
            ax.scatter(data[j,0,i], data[j,1,i],  c=cmarker, marker='o')
            ax.set_xlabel('X (m)'); ax.set_ylabel('Z (m)');
            ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oz-Kz*maxZ,Oz+Kz*maxZ); ax.invert_xaxis()
        if viz == "joints":
            assert(liaisons!=None)
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  
                ax.plot([data[c1,0,i], data[c2,0,i]], [data[c1,1,i], data[c2,1,i]], [data[c1,2,i], data[c2,2,i]], 'k-', lw=1, c='black')
        ax.set_title('Frame %s' %i)
        plt.draw()
        plt.pause(0.1)
        
            
def plot_frame(data, spec_pt=-1,viz="3DPL",liaisons=None,save_dir=None, center_sens=0) : 
    ##########################################################################
    ##### Visualization of 1 frame of mocap data in 2D or 3D
    ##### 'data' array is (Nsensors, Ndim) - Ndim should be 2 or 3
    ##### viz : "3DPL" (3D point-lights), "3Djoints" (then specify 'liaisons'),
    ##### "PL" (white 2D point-lights), "PLb" (black 2D point-lights)
    ##### Beware of adjusting the Kx, Ky, Kz scale factors in the code
    ##########################################################################
       
    joints_to_draw = np.arange(np.shape(data)[0])
    
    # Center the image on the pelvis (0)
    Ncenter = center_sens     # e.g. pelvis marker
    Ox = data[Ncenter,0];   Oy = data[Ncenter,1];   Oz = data[Ncenter,2]
    maxX = (data[:,0]-Ox).max(); maxY = (data[:,1]-Oy).max(); maxZ = (data[:,2]-Oz).max()
    
    # Adjust your scale along the 3 axis 
    Kx = 3; Ky = 5; Kz = 1.25;
    
    if viz[:2]=='3D' : 
        fig = plt.figure(figsize=(8,8))
        ax = fig.gca(projection='3d') 
        ax.view_init(25,125)
        ax.grid(False)
        
        for j in joints_to_draw :
            cmarker = 'b'
            if j == spec_pt :
                cmarker = 'r'
            line=ax.scatter(xs=data[j,0], 
                       ys=data[j,1],  
                       zs=data[j,2],  
                       alpha=0.6, c=cmarker, marker='o')
            ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)'); ax.set_zlabel('Z (m)');
            ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.set_zlim(Oz-Kz*maxZ,Oz+Kz*maxZ)
        if viz == "3Djoints":
            assert(liaisons!=None)
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # -1 pour indice python
                ax.plot([data[c1,0], data[c2,0]], [data[c1,1], data[c2,1]], [data[c1,2], data[c2,2]], 'k-', lw=1, c='black')

        
    elif viz[:2] == "PL" :
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(1, 1, 1) 
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)  
        ax.get_yaxis().set_visible(False)
        
        # Keep only one plan (2D)
        if data.shape[1] == 3 :
            data=data[:,[0,2]]
        
        if viz=="PLb" :
            cmarker = 'black'
        else :
            cmarker = 'w'
            fig.patch.set_facecolor('black')
            ax.set_facecolor('black')
        
        for j in joints_to_draw :
            ax.scatter(data[j,0], data[j,1],  c=cmarker, marker='o',alpha=0.6)
            ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oz-Kz*maxZ,Oz+Kz*maxZ); ax.invert_xaxis()
            plt.tight_layout(); plt.draw()
            
    if save_dir != None :
        fig.savefig(save_dir, bbox_inches='tight')
        
        
def compare_2frames(data1, data2, label1="data1", label2="data2", save_dir=None, center_sens=0) :
    ##########################################################################
    ##### Comparison of 2 postures of mocap data in the 2D frontal plane
    ##### 'dataX' array are (Nsensors, Ndim) - Ndim should be 2 or 3
    ##### 'labelX' are specified as legend of the plot
    ##### Beware of adjusting the Kx & Kz scale factors in the code
    ##########################################################################
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_aspect('equal')
    
    # Keep only one plan (2D)
    if data1.shape[1] == 3 : data1=data1[:,[0,2]]
    if data2.shape[1] == 3 : data2=data2[:,[0,2]]
    
    # Center the image
    Ncenter = center_sens     # e.g. pelvis marker
    Ox1 = data1[Ncenter,0];   Oz1 = data1[Ncenter,1]
    Ox2 = data2[Ncenter,0];   Oz2 = data2[Ncenter,1]
    maxX = (data1[:,0]-Ox1).max(); maxZ = (data1[:,1]-Oz1).max()
    
    # Adjust your scale along the 3 axis 
    Kx = 3; Kz = 1.25;
    
    joints_to_draw = np.arange(np.shape(data1)[0])
    # data1
    cmarker = 'b'

    for j in joints_to_draw :
        if j == joints_to_draw[0]:
            ax.scatter(data1[j,0], data1[j,1],  c=cmarker, marker='o', alpha = 0.7, label=label1)
        ax.scatter(data1[j,0], data1[j,1],  c=cmarker, marker='o', alpha = 0.7)
        ax.set_xlim(Ox1-Kx*maxX,Ox1+Kx*maxX); ax.set_ylim(Oz1-Kz*maxZ,Oz1+Kz*maxZ); ax.invert_xaxis()
        plt.tight_layout(); plt.draw()
    
    # data2
    cmarker = 'r'

    for j in joints_to_draw :
        if j == joints_to_draw[0]:
            ax.scatter(data2[j,0], data2[j,1],  c=cmarker, marker='o', alpha = 0.7, label=label2)
        ax.scatter(data2[j,0], data2[j,1],  c=cmarker, marker='o', alpha = 0.7)
        ax.set_xlabel('X (m)'); ax.set_ylabel('Z (m)');
        ax.set_xlim(Ox1-Kx*maxX,Ox1+Kx*maxX); ax.set_ylim(Oz1-Kz*maxZ,Oz1+Kz*maxZ); ax.invert_xaxis()
        plt.tight_layout(); plt.draw()
    ax.legend()
            
    if save_dir != None :
        fig.savefig(save_dir, bbox_inches='tight')
        
        
def compare_Nframes(data, labels, colors, markers, save_dir=None, mean=None, spec_pt=-1, center_sens=0) :
    ##########################################################################
    ##### Comparison of N postures of mocap data in the 2D frontal plane
    ##### 'data' array is (Npos, Nsensors, Ndim) - Ndim should be 2 or 3
    ##### 'labels' list has Npos length, colors/markers must be specified
    ##### 'mean' of the N postures is plotted if not None
    ##### Beware of adjusting the Kx & Kz scale factors in the code
    ##########################################################################
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_aspect('equal')
    
    # Keep only one plan (2D)
    if data.shape[2] == 3 : data=data[:,:,[0,2]]
    
    # Center the image
    Ncenter = center_sens   # e.g. pelvis marker
    Ox = data[:,Ncenter,0];   Oz = data[:,Ncenter,1]
    maxX = (data[0,:,0]-Ox[0]).max(); maxZ = (data[0,:,1]-Oz[0]).max();
    
    # Adjust your scale along the 3 axis 
    Kx = 3; Kz = 1.25;
    
    joints_to_draw = np.arange(np.shape(data)[1])
    sizeMarker=50
    
    for n in range(0,len(labels)) :
        for j in joints_to_draw :
            cmarker = colors[n]
            if j == spec_pt :
                cmarker = 'black'
            if j == joints_to_draw[0]:
                ax.scatter(data[n,j,0], data[n,j,1],  c=cmarker, marker=markers[n], alpha = 0.7, label=labels[n], s=sizeMarker)
            ax.scatter(data[n,j,0], data[n,j,1],  c=cmarker, marker=markers[n], alpha = 0.7, s=sizeMarker)
            ax.set_xlim(Ox[n]-Kx*maxX,Ox[n]+Kx*maxX); ax.set_ylim(Oz[n]-Kz*maxZ,Oz[n]+Kz*maxZ); ax.invert_xaxis()
            ax.set_xlabel('X (m)',fontsize=20); ax.set_ylabel('Z (m)',fontsize=20); ax.tick_params(labelsize=15)
            plt.tight_layout(); plt.draw()
            
    if mean is not None :
        if mean.shape[2] == 3 : mean=mean[:,:,[0,2]]
        OxM = mean[:,Ncenter,0];   OzM = mean[:,Ncenter,1]
        cmarker = 'black'
        for j in joints_to_draw :
            if j == joints_to_draw[0]:
                ax.scatter(mean[0,j,0], mean[0,j,1],  facecolors='none', edgecolors=cmarker, marker='*', label='mean', s=sizeMarker)
            ax.scatter(mean[0,j,0], mean[0,j,1],  facecolors='none', edgecolors=cmarker, marker='*', s=sizeMarker)
            ax.set_xlim(OxM-Kx*maxX,OxM+Kx*maxX); ax.set_ylim(OzM-Kz*maxZ,OzM+Kz*maxZ); ax.invert_xaxis()
            plt.tight_layout(); plt.draw()
    ax.legend(fontsize=12);
            
    if save_dir is not None :
        fig.savefig(save_dir, bbox_inches='tight')
        
        
def video_PL(data, save_dir, spec_pt=-1, viz="PL", fps=25, center_sens=0):
    ##########################################################################
    ##### Exports a mocap video as point lights in the 2D frontal plane
    ##### It uses ffmpeg so it requires its installation
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 2 or 3
    ##### Display is black point lights, in the specified 'plan'
    ##### Beware of adjusting the Kx & Kz scale factors in the code
    ##########################################################################
    
    fig = plt.figure(figsize=(8,8))
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(1, 1, 1) 
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)  
    ax.get_yaxis().set_visible(False)
    
    plt.ion()
    
    
    
    # Keep only one plan (2D)
    if data.shape[1] == 3 : data=data[:,[0,2],:]
    
    # Center the image
    Ncenter = center_sens    # e.g. pelvis marker
    Ox = data[Ncenter,0,0];   Oz = data[Ncenter,1,0];
    maxX = (data[:,0,:]-Ox).max(); maxZ = (data[:,1,:]-Oz).max();
    
    # Adjust your scale along the 3 axis 
    Kx = 3; Kz = 1.25;
    
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
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oz-Kz*maxZ,Oz+Kz*maxZ); ax.invert_xaxis()
        plt.tight_layout(); plt.draw()
        return ax
    numFrame=len(data[0,0,:])
        
    ani = animation.FuncAnimation(fig,update_img,numFrame,interval=40)
    writer = animation.writers['ffmpeg'](fps=fps)
    writer = animation.FFMpegFileWriter(fps=fps)

    
    dpi=200
    print('exporting PL video ... ' )
    ani.save(save_dir, writer=writer, dpi=dpi)
    plt.close()
    
    
def plot_3frames(data, frames, plan="XZ", save_dir=None, center_sens=0) :
    ##########################################################################
    ##### 3-frame visualization of mocap data in 2D, to describe motion
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 3
    ##### Display is black point lights, in the specified 'plan'
    ##### Beware of adjusting the Kx & Kz scale factors in the code
    ##########################################################################
    
    joints_to_draw = np.arange(np.shape(data)[0])
    
    # Center the image
    Ncenter = center_sens     # e.g. pelvis marker
    Ox = data[Ncenter,0,0];   Oy = data[Ncenter,1,0];   Oz = data[Ncenter,2,0]
    maxX = (data[:,0,:]-Ox).max(); maxY = (data[:,1,:]-Oy).max(); maxZ = (data[:,2,:]-Oz).max()
    
    # Adjust your scale along the 3 axis 
    Kx = 1.5; Ky = 2; Kz = 0.6;
    
    # Keep only one plan (2D)
    if plan=="XZ" : data=data[:,[0,2],:]
    if plan=="XY" : data=data[:,[0,1],:]
    if plan=="YZ" : data=data[:,[1,2],:]
    cmarker = 'black'
    
    fig = plt.figure(figsize=(16,8))
    for f in range(len(frames)) :
        ax = fig.add_subplot(1, 3, f+1) 
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)  
        ax.get_yaxis().set_visible(False)
        
        for j in joints_to_draw :
            if plan == "XZ" :
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]],  c=cmarker, marker='o',alpha=0.6)
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oz-Kz*maxZ,Oz+2.1*Kz*maxZ); ax.invert_xaxis()
#                ax.set_xlim(Ox-0.5,Ox+0.5); ax.set_ylim(Oz-0.5,Oz+1); ax.invert_xaxis()
            if plan == "XY" :
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]],  c=cmarker, marker='o',alpha=0.6)
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY);
            if plan == "YZ" :
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]],  c=cmarker, marker='o',alpha=0.6)
                ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.set_ylim(Oz-Kz*maxZ,Oz+Kz*maxZ); ax.invert_xaxis()
            plt.tight_layout(); plt.draw()
            
    if save_dir != None :
        fig.savefig(save_dir, bbox_inches='tight')
