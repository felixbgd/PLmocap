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

def data_viz3D(subj1, frameStop=None, spec_pt=-1, viz="PL", view=[25,125],liaisons=None, center_sens=0, numsubj=1, subj2=None) : 
    ##########################################################################
    ##### Animated visualization of mocap data in the 3D space
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 3
    ##### Reads until the end, or 'frameStop', can highlight 'spec_pt' sensor
    ##### "PL" (point-light) or "joints" display (then specify 'liaisons')
    ##### Beware of adjusting the Kx, Ky, Kz scale factors in the code
    ##########################################################################
    
    joints_to_draw = np.arange(np.shape(subj1)[0])
    
    # Center the image
    Ncenter = center_sens     # e.g. pelvis marker
    Ox = subj1[Ncenter,0,0];   Oy = subj1[Ncenter,1,0];   Oz = subj1[Ncenter,2,0]
    maxX = np.abs(subj1[:,0]-Ox).max(); maxY = np.abs(subj1[:,1]-Oy).max(); maxZ = np.abs(subj1[:,2]-Oz).max()
    # if numsubj > 1:
    #     maxX2 = np.abs(subj2[:,0]-Ox).max(); maxY2 = np.abs(subj2[:,1]-Oy).max(); maxZ2 = np.abs(subj2[:,2]-Oz).max()
    #     maxX = max(maxX,maxX2); maxY = max(maxY,maxY2); maxZ = max(maxZ,maxZ2);
    maxY = 2500
    
    # Adjust your scale along the 3 axis 
    Kx = 2.5; Ky = 1; Kz = 1.25;
    
    fig = plt.figure(figsize=(8,8))
    ax = fig.gca(projection='3d') 
    ax.view_init(view[0],view[1]);    ax.grid(None)
    plt.ion()
    
    numFrame = len(subj1[0,0,:])     
    if frameStop == None:
        frameStop = numFrame
    
    for i in range(0,frameStop) :
        ax.clear()
        ax.grid(None)
        
        for subj in range(numsubj) :
            print(subj)
            if subj == 0: data = subj1
            if subj == 1: data = subj2
    
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
        plt.pause(0.05)
        
            
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
    maxX = np.abs(data[:,0,:]-Ox).max(); maxZ = np.abs(data[:,1,:]-Oz).max();
    
    # Adjust your scale along the 3 axis 
    Kx = 1.25; Kz = 1.25;

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
                ax.plot([data[c1,0,i], data[c2,0,i]], [data[c1,1,i], data[c2,1,i]], 'k-', lw=1, c='black')
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
    if center_sens!=None:
        Ncenter = center_sens     # e.g. pelvis marker
        Ox = data[Ncenter,0];   Oy = data[Ncenter,1];   Oz = data[Ncenter,2]
    else: Ox = 0;   Oy = 0;   Oz = 0
    maxX = np.abs(data[:,0]-Ox).max(); maxY = np.abs(data[:,1]-Oy).max(); maxZ = np.abs(data[:,2]-Oz).max()
    
    # Adjust your scale along the 3 axis 
    Kx = 2; Ky = 2; Kz = 1.5; 
    
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
                       alpha=0.6, c=cmarker, marker='o',s=65)
            ax.set_xlabel('X (m)'); ax.set_ylabel('Y (m)'); ax.set_zlabel('Z (m)');
            ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.set_zlim(Oz-Kz*maxZ,Oz+Kz*maxZ)
            ax.invert_xaxis()
        if viz == "3Djoints":
            assert(liaisons!=None)
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # -1 pour indice python
                ax.plot([data[c1,0], data[c2,0]], [data[c1,1], data[c2,1]], [data[c1,2], data[c2,2]], 'k-', lw=1.2, c='black')
                ax.set_axis_off()
        
    elif viz[:2] == "PL" :
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(1, 1, 1) 
        ax.set_aspect('equal')
        # ax.get_xaxis().set_visible(False)  
        # ax.get_yaxis().set_visible(False)
        
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
            if j == spec_pt : ax.scatter(data[j,0], data[j,1],  c='r', marker='o',alpha=0.6)
            else: ax.scatter(data[j,0], data[j,1],  c=cmarker, marker='o',alpha=0.6)
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
    maxX = np.abs(data1[:,0]-Ox1).max(); maxZ = np.abs(data1[:,1]-Oz1).max()
    
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
        
        
def compare_Nframes(data, labels, markers, colors=None, save_dir=None, mean=None, liaisons=None, spec_pt=-1, center_sens=0) :
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
    maxX = np.abs(data[0,:,0]-Ox[0]).max(); maxZ = np.abs(data[0,:,1]-Oz[0]).max();
    
    # Adjust your scale along the 3 axis 
    Kx = 1.25; Kz = 1.25;
    
    joints_to_draw = np.arange(np.shape(data)[1])
    sizeMarker=60
    
    for n in range(0,len(labels)) :
        for j in joints_to_draw :
            if colors==None:
                if n==0 :cmarker = 'black'
                else: cmarker = 'gray'
            else:
                cmarker=colors[n]
            if j == spec_pt :
                cmarker = 'black'
            if j == joints_to_draw[0]:
                ax.scatter(data[n,j,0], data[n,j,1],  c=cmarker, marker=markers[n], alpha = 0.8, label=labels[n], s=sizeMarker)
            ax.scatter(data[n,j,0], data[n,j,1],  c=cmarker, marker=markers[n], alpha = 0.7, s=sizeMarker)
            ax.set_xlim(Ox[n]-Kx*1.1*maxX,Ox[n]+Kx*0.9*maxX); ax.set_ylim(Oz[n]-Kz*0.1*maxZ,Oz[n]+Kz*maxZ); 
            ax.set_xlim(-1,1); ax.set_ylim(-0.75,1.25); ax.invert_xaxis()
            ax.set_xlabel('X (m)',fontsize=20); ax.set_ylabel('Z (m)',fontsize=20); ax.tick_params(labelsize=15)
            plt.tight_layout(); plt.draw()
    
        if liaisons!=None:
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # get the two joints
                ax.plot([data[n,c1,0], data[n,c2,0]], [data[n,c1,1], data[n,c2,1]], 'k-', lw=1.25, c=cmarker,alpha=0.8)
#    ax.set_axis_off()
            
    if mean is not None :
        if mean.shape[2] == 3 : mean=mean[:,:,[0,2]]
        OxM = mean[:,Ncenter,0];   OzM = mean[:,Ncenter,1]
        cmarker = 'black'
        for j in joints_to_draw :
            if j == joints_to_draw[0]:
                ax.scatter(mean[0,j,0], mean[0,j,1],  facecolors='none', edgecolors=cmarker, marker='*', label='mean', s=sizeMarker)
            ax.scatter(mean[0,j,0], mean[0,j,1],  facecolors='none', edgecolors=cmarker, marker='*', s=sizeMarker)
            ax.set_xlim(OxM-Kx*maxX,OxM+Kx*maxX); ax.set_ylim(OzM-Kz*0.1*maxZ,OzM+Kz*maxZ); ax.invert_xaxis()
            plt.tight_layout(); plt.draw()
    ax.legend(fontsize=12);
            
    if save_dir is not None :
        fig.savefig(save_dir, dpi=300, bbox_inches='tight')
        
        
def video_PL(data, save_dir, plan="XZ", spec_pt=-1, viz="PL", fps=25, center_sens=None, minDim=None, maxDim=None, dpi=200, title=''):
    ##########################################################################
    ##### Exports a mocap video as point lights in the 2D frontal plane
    ##### It uses ffmpeg so it requires its installation
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 2 or 3
    ##### Display is black point lights, in the specified 'plan'
    ##### Beware of adjusting the Kx, Ky & Kz scale factors in the code
    ##########################################################################
    
    # Center the image
    # Center the image on the pelvis (0)
    if center_sens!=None:
        Ncenter = center_sens     # e.g. pelvis marker
        Ox = data[Ncenter,0];   Oy = data[Ncenter,1];   Oz = data[Ncenter,2]
    else: Ox = 0;   Oy = 0;   Oz = 0
    if type(minDim) == type(None) : 
        minDim = np.zeros((3))
        minDim[0] =  (data[:,0,:]-Ox).min();
        minDim[1] =  (data[:,1,:]-Oy).min();
        minDim[2] =  (data[:,2,:]-Oz).min();
    if type(maxDim) == type(None) : 
        maxDim = np.zeros((3))
        maxDim[0] =  (data[:,0,:]-Ox).max();
        maxDim[1] =  (data[:,1,:]-Oy).max();
        maxDim[2] =  (data[:,2,:]-Oz).max(); 
    
    # Keep only one plan (2D)
    dataXZ=data[:,[0,2],:]
    dataYZ=data[:,[1,2],:]
    
    # Adjust your scale along the 3 axis 
    Kx = (maxDim[0] - minDim[0])*0.2; Ky = (maxDim[1] - minDim[1])*0.8; Kz = (maxDim[2] - minDim[2])*0.1;
    
    joints_to_draw = np.arange(np.shape(data)[0])
    numFrame = len(data[0,0,:])     
    
    fig = plt.figure(figsize=(8,8))
    
    # Make sure that both subplots (frontal and sagittal) have same height, despite different width
    from matplotlib import gridspec
    width_x = maxDim[0]-minDim[0]+2*Kx; width_y = maxDim[1]-minDim[1]+2*Ky;
    gs = gridspec.GridSpec(1, 2, width_ratios=[width_x/width_y, 1]) 
    
    fig.patch.set_facecolor('black')
    def update_img(i):
        if i in idx_steps:
            print(str(ratios[np.where(idx_steps==i)[0][0]]) + "%   ",end='')
        if i == numFrame-1:
            print("100%")
        for p in range(2):
            ax = fig.add_subplot(gs[p])
            ax.set_aspect('equal')
            # ax.get_xaxis().set_visible(False)
            # ax.get_yaxis().set_visible(False)
            plt.ion()

            cmarker_ref = 'b'
            if viz == "PL" :
                cmarker_ref = 'w'
                ax.set_facecolor('black')
                
                
            ax.clear()

            for j in joints_to_draw :
                    if j == spec_pt: cmarker = 'r'
                    else: cmarker = cmarker_ref
                    if p == 0:
                        ax.scatter(dataXZ[j,0,i], dataXZ[j,1,i],  c=cmarker, marker='o')
                        # ax.set_xlim(Ox+Kx*minDim[0],Ox+Kx*maxDim[0]); ax.set_ylim(Oz+Kz*minDim[2],Oz+Kz*maxDim[2]); ax.invert_xaxis()
                    if p ==1:
                        ax.scatter(dataYZ[j,0,i], dataYZ[j,1,i],  c=cmarker, marker='o')
                        # ax.set_xlim(Oy+Ky*minDim[1],Oy+Ky*maxDim[1]); ax.set_ylim(Oz+Kz*minDim[2],Oz+Kz*maxDim[2]); 
            if p == 0: 
                ax.set_xlim(Ox+minDim[0]-Kx,Ox+maxDim[0]+Kx); ax.set_ylim(Oz+minDim[2]-Kz,Oz+maxDim[2]+Kz); ax.invert_xaxis()
                ax.set_title('Frontal plane',color=cmarker_ref)
            if p ==1: 
                ax.set_xlim(Oy+minDim[1]-Ky,Oy+maxDim[1]+Ky); ax.set_ylim(Oz+minDim[2]-Kz,Oz+maxDim[2]+Kz); 
                ax.set_title('Sagittal plane',color=cmarker_ref)
            ax.set_xticks([]); ax.set_yticks([])
        if i==0: fig.tight_layout()
        

        fig.suptitle(title,color=cmarker_ref)
        return ax
    numFrame=len(data[0,0,:])
    idx_steps = np.arange(0,numFrame,numFrame/10)[1:].astype(int)
    ratios = np.arange(0,100,10)[1:]
    
    ani = animation.FuncAnimation(fig,update_img,numFrame,interval=40)
    writer = animation.writers['ffmpeg'](fps=fps)
    writer = animation.FFMpegFileWriter(fps=fps)

    
    print('exporting PL video ... ' )
    ani.save(save_dir, writer=writer, dpi=dpi)
    plt.close()
    
def video_PL_dual(data1, data2, save_dir, plan="XZ", spec_pt=-1, viz="PL", fps=25, center_sens=None, minDim=None, maxDim=None, dpi=200, title=''):
    ##########################################################################
    ##### Exports a mocap video as point lights in the 2D frontal plane
    ##### It uses ffmpeg so it requires its installation
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 2 or 3
    ##### Display is black point lights, in the specified 'plan'
    ##### Beware of adjusting the Kx, Ky & Kz scale factors in the code
    ##########################################################################
    
    # Center the image
    # Center the image on the pelvis (0)
    if center_sens!=None:
        Ncenter = center_sens     # e.g. pelvis marker
        Ox = data1[Ncenter,0];   Oy = data1[Ncenter,1];   Oz = data1[Ncenter,2]
    else: Ox = 0;   Oy = 0;   Oz = 0
    if type(minDim) == type(None) : 
        minDim = np.zeros((3))
        minDim[0] =  (data1[:,0,:]-Ox).min();
        minDim[1] =  (data1[:,1,:]-Oy).min();
        minDim[2] =  (data1[:,2,:]-Oz).min();
    if type(maxDim) == type(None) : 
        maxDim = np.zeros((3))
        maxDim[0] =  (data1[:,0,:]-Ox).max();
        maxDim[1] =  (data1[:,1,:]-Oy).max();
        maxDim[2] =  (data1[:,2,:]-Oz).max(); 
    
    # Keep only one plan (2D)
    data1=data1[:,[0,2],:]
    data2=data2[:,[0,2],:]
    
    # Adjust your scale along the 3 axis 
    Kx = (maxDim[0] - minDim[0])*0.2; Ky = (maxDim[1] - minDim[1])*0.8; Kz = (maxDim[2] - minDim[2])*0.1;
    
    joints_to_draw = np.arange(np.shape(data1)[0])
    numFrame = len(data1[0,0,:])     
    
    fig = plt.figure(figsize=(8,8))
    
    # Make sure that both subplots (frontal and sagittal) have same height, despite different width
    from matplotlib import gridspec
    width_x = maxDim[0]-minDim[0]+2*Kx; width_y = maxDim[1]-minDim[1]+2*Ky;
    gs = gridspec.GridSpec(1, 2, width_ratios=[width_x/width_y, 1]) 
    
    fig.patch.set_facecolor('black')
    def update_img(i):
        if i in idx_steps:
            print(str(ratios[np.where(idx_steps==i)[0][0]]) + "%   ",end='')
        if i == numFrame-1:
            print("100%")
        for p in range(2):
            ax = fig.add_subplot(gs[p])
            ax.set_aspect('equal')
            # ax.get_xaxis().set_visible(False)
            # ax.get_yaxis().set_visible(False)
            plt.ion()

            cmarker_ref = 'b'
            if viz == "PL" :
                cmarker_ref = 'w'
                ax.set_facecolor('black')
                
                
            ax.clear()

            for j in joints_to_draw :
                    if j == spec_pt: cmarker = 'r'
                    else: cmarker = cmarker_ref
                    if p == 0:
                        ax.scatter(data1[j,0,i], data1[j,1,i],  c=cmarker, marker='o')
                        # ax.set_xlim(Ox+Kx*minDim[0],Ox+Kx*maxDim[0]); ax.set_ylim(Oz+Kz*minDim[2],Oz+Kz*maxDim[2]); ax.invert_xaxis()
                    if p ==1:
                        ax.scatter(data2[j,0,i], data2[j,1,i],  c=cmarker, marker='o')
                        # ax.set_xlim(Oy+Ky*minDim[1],Oy+Ky*maxDim[1]); ax.set_ylim(Oz+Kz*minDim[2],Oz+Kz*maxDim[2]); 
            if p == 0: 
                ax.set_xlim(Ox+minDim[0]-Kx,Ox+maxDim[0]+Kx); ax.set_ylim(Oz+minDim[2]-Kz,Oz+maxDim[2]+Kz); ax.invert_xaxis()
                ax.set_title('Frontal plane 1',color=cmarker_ref)
            if p ==1: 
                ax.set_xlim(Ox+minDim[0]-Kx,Ox+maxDim[0]+Kx); ax.set_ylim(Oz+minDim[2]-Kz,Oz+maxDim[2]+Kz); ax.invert_xaxis()
                ax.set_title('Frontal plane 2',color=cmarker_ref)
            ax.set_xticks([]); ax.set_yticks([])
        if i==0: fig.tight_layout()
        

        fig.suptitle(title,color=cmarker_ref)
        return ax
    numFrame=len(data1[0,0,:])
    idx_steps = np.arange(0,numFrame,numFrame/10)[1:].astype(int)
    ratios = np.arange(0,100,10)[1:]
    
    ani = animation.FuncAnimation(fig,update_img,numFrame,interval=40)
    writer = animation.writers['ffmpeg'](fps=fps)
    writer = animation.FFMpegFileWriter(fps=fps)

    
    print('exporting PL video ... ' )
    ani.save(save_dir, writer=writer, dpi=dpi)
    plt.close()
    
def plot_3frames(data, frames, plan="XZ", liaisons=None, save_dir=None, center_sens=0, cmarker='black',fig=None,label=None) :
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
    Kx = 1.5; Ky = 5; Kz = 0.6;
    
    # Keep only one plan (2D)
    if plan=="XZ" : data=data[:,[0,2],:]
    if plan=="XY" : data=data[:,[0,1],:]
    if plan=="YZ" : data=data[:,[1,2],:]
    
    if fig==None:
        fig = plt.figure(figsize=(16,8))
    for f in range(len(frames)) :
        print(frames[f])
        ax = fig.add_subplot(1, 3, f+1) 
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)  
        ax.get_yaxis().set_visible(False)
        
        if liaisons!=None:
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # get the two joints
                ax.plot([data[c1,0,frames[f]], data[c2,0,frames[f]]], [data[c1,1,frames[f]], data[c2,1,frames[f]]], 'k-', lw=1.5, c='black',zorder=1)

        for j in joints_to_draw :
            if plan == "XZ" :
                if j==0 : ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]], marker='o',edgecolor='black',facecolor=cmarker, s=55, alpha=0.8,zorder=2,label=label)  #label on scatter
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]], marker='o',edgecolor='black',facecolor=cmarker,alpha=0.8,zorder=2)
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oz-Kz*maxZ,Oz+2.1*Kz*maxZ); ax.invert_xaxis()
            if plan == "XY" :
                if j==0:ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]], marker='o',edgecolor='black',facecolor=cmarker, s=55,alpha=0.8,zorder=2,label=label)
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]], marker='o',edgecolor='black',facecolor=cmarker,alpha=0.8,zorder=2)
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.invert_xaxis()
            if plan == "YZ" :
                if j==0:ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]], marker='o',edgecolor='black',facecolor=cmarker, s=55,alpha=0.8,zorder=2,label=label)
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]], marker='o',edgecolor='black',facecolor=cmarker,alpha=0.8,zorder=2)
                ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.set_ylim(Oz-Kz*maxZ,Oz+2.1*Kz*maxZ); 
            plt.tight_layout(); plt.draw()
            
        ax.set_axis_off()
    
    if label!=None:
        ax.legend(fontsize=13,markerscale=1.2)
            
    if save_dir != None :
        fig.savefig(save_dir, bbox_inches='tight')
        
        
def plot_2frames(data, frames, plan="XZ", liaisons=None, save_dir=None, center_sens=0, ax=None) :
    ##########################################################################
    ##### Visualization of mocap data in 2D, min and max postures in 1 figure
    ##### 'data' array is (Nsensors, Ndim, Nframes) - Ndim should be 3
    ##### Display is black point lights, in the specified 'plan'
    ##### Beware of adjusting the Kx & Kz scale factors in the code
    ##########################################################################
    
    joints_to_draw = np.arange(np.shape(data)[0])
    
    # Center the image
    Ncenter = center_sens     # e.g. pelvis marker
    Ox = data[Ncenter,0,0];   Oy = data[Ncenter,1,0];   Oz = data[Ncenter,2,0]
    maxX = abs(data[:,0,:]-Ox).max(); maxY = abs(data[:,1,:]-Oy).max(); maxZ = abs(data[:,2,:]-Oz).max()
    
    # Adjust your scale along the 3 axis 
    Kx = 2; Ky = 2; Kz = 0.6; 
    
    # Keep only one plan (2D)
    if plan=="XZ" : data=data[:,[0,2],:]
    if plan=="XY" : data=data[:,[0,1],:]
    if plan=="YZ" : data=data[:,[1,2],:]
    
    if ax==None:
        fig = plt.figure(figsize=(10,10))
        ax = fig.gca()
    for f in range(len(frames)) :
        if f==0:cmarker = 'gray'
        if f==1:cmarker = 'black'
        ax.set_aspect('equal')
        ax.get_xaxis().set_visible(False)  
        ax.get_yaxis().set_visible(False)
        
        for j in joints_to_draw :
            if plan == "XZ" :
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]],  c=cmarker, marker='o', s=55, alpha=0.6)
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oz-2.1*Kz*maxZ,Oz+2.1*Kz*maxZ);  ax.invert_xaxis()
            if plan == "XY" :
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]],  c=cmarker, marker='o', s=55 ,alpha=0.6)
                ax.set_xlim(Ox-Kx*maxX,Ox+Kx*maxX); ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.invert_xaxis()
            if plan == "YZ" :
                ax.scatter(data[j,0,frames[f]], data[j,1,frames[f]],  c=cmarker, marker='o', s=55 ,alpha=0.6)
                ax.set_ylim(Oy-Ky*maxY,Oy+Ky*maxY); ax.set_ylim(Oz-2.1*Kz*maxZ,Oz+2.1*Kz*maxZ); 
            plt.tight_layout(); plt.draw()
            
        if liaisons!=None:
            for l in liaisons :
                c1 = l[0];   c2 = l[1]  # get the two joints
                ax.plot([data[c1,0,frames[f]], data[c2,0,frames[f]]], [data[c1,1,frames[f]], data[c2,1,frames[f]]], 'k-', lw=1.5, c=cmarker)
        ax.set_axis_off()
            
    if save_dir != None :
        fig.savefig(save_dir, bbox_inches='tight')
