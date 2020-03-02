#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 17:12:23 2019

@author: felixbigand
"""

from funcs_test_c3d import *
import c3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np
import os

# tests librairies pour export vidéo des PL.
import matplotlib.animation as animation
import numpy as np
import scipy.signal
from pylab import *

#test git
#signers = ['l1-dom','l2-ma.th','l3-cyr','l4-pas','l6-viv','l8-lau']
signers = ['l2-ma.th','l4-pas','l6-viv','l8-lau']
#signers = ['l3-cyr']


sign=0
for s in signers :
    folder = os.getcwd() + '/Tache1/' + s + '/mocap/c3d'
    files=os.listdir(folder);      files=[x for i,x in enumerate(files) if (x.endswith(".c3d"))]
    files=sorted(files)
    
    for im in files :
        
        output_dir = os.getcwd() + '/Tache1/' + s + '/mocap/features2'
        if not (os.path.exists(output_dir)) :
            os.mkdir(output_dir)

        data = np.load(os.getcwd() + '/Tache1/' + s + '/mocap/npy/' + im[0:-4] +'_data.npy')
        labels = np.load(os.getcwd() + '/Tache1/' + s + '/mocap/npy/' + im[0:-4] +'_labels.npy')
        
        if len(labels) >= 23 :

            # Downsample data for visualisation
            data = data[:,:,::10]
            fps = 25
                            
            # Recentrer certains capteurs
            # Coudes (garder uniquement 1 des deux capteurs coudes
            coudeG = data[11,:,:];  coudeD = data[18,:,:]
            data[11,:,:] = coudeG;  data[18,:,:] = coudeD
            labels[11] = 'coudeG';  labels[18] = 'coudeD'
            
            # Poignet (2 pts -> 1 moyen)
    #        wristG = ( data[25,:,:] + data[26,:,:] ) / 2
    #        wristD = ( data[33,:,:] + data[34,:,:] ) / 2
    #        data[25,:,:] = wristG;  data[26,:,:] = wristD
    #        labels[25] = 'wristG';  labels[26] = 'wristD'
            
            # Buste (2x 2 pts -> 1 pt moyen)
            if s=='l3-cyr' :    #bug capteur col cyril
                bustH = ( data[10,:,:] + data[17,:,:] ) / 2
            else :
                bustH = data[2,:,:]
            bustL = data[3,:,:]
            data[1,:,:] = bustH;  data[3,:,:] = bustL
            labels[1] = 'bustH';  labels[3] = 'bustL'
            
            # Bassin (3 pts -> 1 pt moyen)
    #        pelv = ( data[0,:,:] + data[3,:,:] + data[4,:,:] ) / 3
            pelv = data[0,:,:]
            data[0,:,:] = pelv;    labels[0] = 'pelv'
            
            # Supprimer les capteurs qui ont servi à moyenner
#            if s=='l3-cyr' :    #bug capteur col cyril
#                data=np.delete(data,[2,4,9,16],0);   labels=np.delete(labels,[2,4,9,16],0) 
#            else :
            data=np.delete(data,[2,4,9,16],0);   labels=np.delete(labels,[2,4,9,16],0) 
    
            # Cut norm. motion start/end
#            tCut = int(6*fps)
            t = data[0,0,:];     xyz = data[:,1:4,:]
            joints = [i for i,x in enumerate(labels) if x.find("Face")==-1]
            numFrame = len(data[0,0,:])
            
            # Filter the mocap data to avoid noisy markers
            for capt in range(0,len(xyz[:,0,0])) :
                xyz[capt,0,:] = scipy.signal.savgol_filter(xyz[capt,0,:],5,3)
                xyz[capt,1,:] = scipy.signal.savgol_filter(xyz[capt,1,:],5,3)
                xyz[capt,2,:] = scipy.signal.savgol_filter(xyz[capt,2,:],5,3)
#                xyz[capt,0,:] = scipy.signal.medfilt(xyz[capt,0,:], kernel_size=7)
#                xyz[capt,1,:] = scipy.signal.medfilt(xyz[capt,1,:], kernel_size=7)
#                xyz[capt,2,:] = scipy.signal.medfilt(xyz[capt,2,:], kernel_size=7)
            
            data=xyz
            joints_to_draw = joints
            spec_pt=-1
            viz="PL"
            fig = plt.figure(figsize=(8,8))
            fig.patch.set_facecolor('black')
            ax = fig.add_subplot(1, 1, 1) 
            ax.set_aspect('equal')
            ax.get_xaxis().set_visible(False)  
            ax.get_yaxis().set_visible(False)
            
            plt.ion()
            
            # Keep only one plan (2D)
            data=data[:,[0,2],:]
            
            # Center the image on the pelvis (2)
            Ox = data[2,0,0];   Oy = data[2,1,0]
            
            numFrame = len(data[0,0,:])     
            
            cmarker = 'b'
            if viz == "PL" :
                cmarker = 'w'
                ax.set_facecolor('black')
            
            def update_img(i):
                ax.clear()
            
                cmarker = 'w'
                ax.set_facecolor('black')
                for j in joints_to_draw :
                        if j == spec_pt :
                            cmarker = 'r'
                        ax.scatter(data[j,0,i], data[j,1,i],  c=cmarker, marker='o')
                        ax.set_xlim(Ox-1,Ox+1); ax.set_ylim(Oy-1,Oy+1); ax.invert_xaxis()
                plt.tight_layout(); plt.draw()
                return ax
            
            #legend(loc=0)
#            numFrame=min(len(data[0,0,:]),500)
            numFrame=len(data[0,0,:])
                
            ani = animation.FuncAnimation(fig,update_img,numFrame,interval=40)
            writer = animation.writers['ffmpeg'](fps=25)
            writer = animation.FFMpegFileWriter(fps=25)
    
            
            dpi=200
            print('exporting ...  ' + s + '_' + im[0:-4] + '.mp4')
            ani.save('/people/bigand/Bureau/PL_stimuli/distracteurs/' + s + '_' + im[0:-4] + '.mp4',writer=writer,dpi=dpi)
#            ani.save('/Users/felixbigand/Desktop/PL_stimuli/' + s + '_' + im[0:-4] + '.mp4',writer=writer,dpi=dpi)
#            ani.save('/Users/felixbigand/Desktop/PL_stimuli/' + s + '_' + im[0:-4] + '_testScolio.mp4',writer=writer,dpi=dpi)            
#            ani.save('/people/bigand/Bureau/PL_stimuli/' + s + '_' + im[0:-4] + '_testScolio.mp4',writer=writer,dpi=dpi)
            plt.close()
