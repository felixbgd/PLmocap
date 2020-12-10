#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:44:10 2020

@author: felixbigand
"""

import matplotlib.pyplot as plt
from PLmocap.viz import *
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import numpy as np
import os

#####################################################################################
##### ALL THE FUNCTIONS CAN BE USED WITH MOTION MATRIX OF CARTESIAN COORD (XYZ) #####
##### BE CAREFUL THAT PLOTS AREN'T ALL WORKING IF MORE THAN 4 PERSONS FOR NOW   #####
#####################################################################################

markers = ['o','s','+','*','.','x']

def size_norm(data,ref_posture=None,persons=np.arange(4),output_dir=os.getcwd(),colors=None,viz=False,dim=3) :
    ##########################################################################
    ##### Size normalization of the mocap dataset of multiple persons
    ##### 'data' : the whole motion data (Npersons, NsensorsxNdim, Nframes) 
    ##### 'ref_posture' : the reference postures (Npersons, NsensorsxNdim) 
    ##### 'persons' : labels of the persons
    ##### OUTPUTS : size-normalized dataset + new ref_postures
    ##### Inspired by Trojet et al. (2005)  
    ##########################################################################
    
    # Set reference postures to the mean posture over frames, if None
    if ref_posture is None : ref_posture=np.mean(data,2)
    global_ref_posture = np.mean(ref_posture,0)     # Average posture over the persons
    Nsensors = np.int( data.shape[1] / dim )
    
    # Regression between each average posture and the global average posture
    reg_slope = []
    reg_offset = []
    for i in range(0,len(persons)):
        reg = LinearRegression(False).fit(np.reshape(global_ref_posture,(-1,1)),np.reshape(ref_posture[i,:],(-1,1)))
        reg_slope.append(reg.coef_)
        reg_offset.append(reg.intercept_)
    
    # Compute relative sizes of each person    
    relative_size=np.round( np.reshape(np.asarray(reg_slope),(len(persons),1)) , 3)
    offset= np.reshape(np.asarray(reg_offset),(len(persons),1))
    
    # Descriptive plots for regression (optimized for 4 persons)
    if viz != False : 
        # Scatterplots of ref_posture, as a function of the global_ref_posture 
        # fig2 allows for specifying the 3D axis of each sensor (x,y,z) 
        fig = plt.figure(figsize=(8,8))
        fig2 = plt.figure(figsize=(8,8))   
        for i in range(0,len(persons)):
            min_plot=-1; max_plot=1
            ax = fig.add_subplot(2, 2, i+1)
            ax2 = fig2.add_subplot(2, 2, i+1)
            ax.scatter(global_ref_posture, ref_posture[i,:])
            ax2.scatter([e for i, e in enumerate(global_ref_posture) if  i%3==0], [e for i, e in enumerate(ref_posture[i,:]) if  i%3==0],c='r')
            ax2.scatter([e for i, e in enumerate(global_ref_posture) if  i%3==2], [e for i, e in enumerate(ref_posture[i,:]) if  i%3==2],c='b')
            ax2.scatter([e for i, e in enumerate(global_ref_posture) if  i%3==1], [e for i, e in enumerate(ref_posture[i,:]) if  i%3==1],c='g')
            ax.plot([min_plot,max_plot],[min_plot,max_plot],'--')
            ax.plot([min_plot,max_plot],[min_plot*relative_size[i]+offset[i],max_plot*relative_size[i]+offset[i]],'r-')
            ax2.plot([min_plot,max_plot],[min_plot,max_plot],'--')
            ax2.plot([min_plot,max_plot],[min_plot*relative_size[i]+offset[i],max_plot*relative_size[i]+offset[i]],'r-')
            if i+1>2 : ax.set_xlabel('Global average posture (m)');   ax2.set_xlabel('Global average posture (m)')
            if (i+1)%2!=0 : ax.set_ylabel('Individual average posture (m)');  ax2.set_ylabel('Individual average posture (m)')
            ax.set_xlim(min_plot,max_plot); ax.set_ylim(min_plot,max_plot)
            ax2.set_xlim(min_plot,max_plot); ax2.set_ylim(min_plot,max_plot)
            r = round(np.corrcoef(ref_posture[i,:],global_ref_posture)[0,1],2)
            ax.set_title("ORI S%s" %(i+1) + ": s = %s " %relative_size[i] + "r = %s" %r)
            ax2.set_title("ORI S%s" %(i+1) + ": s = %s " %relative_size[i] + "r = %s" %r)
        fig.savefig(output_dir + '/scatter_ORI.pdf', bbox_inches='tight')
        fig2.savefig(output_dir + '/scatter_ORI_3D.pdf', bbox_inches='tight')
        plt.close();    plt.close()
    
    # Compute the size-normalize motion
    ref_posture_SI = np.zeros(ref_posture.shape)
    data_SI = np.zeros(data.shape)
    for i in range(0,len(persons)):
        data_SI[i,:,:] = data[i,:,:] / relative_size[i]
        ref_posture_SI[i,:] = ref_posture[i,:] / relative_size[i]
    global_ref_posture_SI = np.mean(ref_posture_SI,0)
    
    # Compute and plot reference posture after normalization
    if colors is None : 
        colors = []
        for i in range(0,len(persons)) :
            colors.append(np.random.rand(3,))
    
    # Descriptive plots of the normalization effect 
    if viz != False : 
        # Scatterplots of the sensors of each person in the new reference posture, 
        # as a function of the global reference posture (optimized for 4 persons)
        fig = plt.figure(figsize=(8,8))
        for i in range(0,len(persons)):
            ax = fig.add_subplot(2, 2, i+1) 
            ax.scatter(global_ref_posture_SI, ref_posture_SI[i,:])
            ax.plot([min_plot,max_plot],[min_plot,max_plot],'--')
            ax.plot([min_plot,max_plot],[min_plot*relative_size_SI[i]+offset_SI[i],max_plot*relative_size_SI[i]+offset_SI[i]],'r-')
            if i+1>2 : ax.set_xlabel('Global average posture (m)')
            if (i+1)%2!=0 : ax.set_ylabel('Individual average posture (m)')
            ax.set_xlim(min_plot,max_plot); ax.set_ylim(min_plot,max_plot)
            r_SI = round(np.corrcoef(ref_posture_SI[i,:],global_ref_posture_SI)[0,1],2)
            ax.set_title("SI S%s" %(i+1) + ": s = %s " %relative_size_SI[i] + "r = %s" %r_SI)
        fig.savefig(output_dir + '/scatter_SI.pdf', bbox_inches='tight')
        plt.close()
    
        # Comparison of the ref posture, before norm. vs. after, for each person
        for i in range(0,len(persons)):
            compare_2frames(np.reshape(ref_posture[i,:],(Nsensors,dim)), \
                          np.reshape(ref_posture_SI[i,:],(Nsensors,dim)), \
                       "ORI","SI", save_dir=output_dir + '/COMPAR_SI_person' + str(i+1) + '.pdf')
            plt.close()
            
        # Comparison of the Npers refererence postures after size_norm
        compare_Nframes(np.reshape(ref_posture_SI,(len(persons),Nsensors,dim)), persons, colors, markers, save_dir=output_dir + '/COMPAR_allrefs_SI.pdf')
        plt.close()
        # Same plot + the new global reference posture
        compare_Nframes(np.reshape(ref_posture_SI,(len(persons),Nsensors,dim)), persons, colors, markers, save_dir=output_dir + '/COMPAR_allrefs_SI_mean.pdf',  \
                        mean=np.reshape(global_ref_posture_SI,(1,Nsensors,dim)))
        plt.close()
        
    return data_SI, ref_posture_SI


def shape_norm(data,ref_posture=None,persons=np.arange(4),output_dir=os.getcwd(),colors=None,viz=False,dim=3) :
    ##########################################################################
    ##### Shape normalization of the mocap dataset of multiple persons
    ##### 'data' : the whole motion data (Npersons, NsensorsxNdim, Nframes) 
    ##### 'ref_posture' : the reference postures (Npersons, NsensorsxNdim) 
    ##### 'persons' : labels of the persons
    ##### OUTPUTS : shape-normalized dataset + new ref_postures
    ##### Inspired by Trojet et al. (2005)  
    ##########################################################################
    
    # Set reference postures to the mean posture over frames, if None
    if ref_posture is None :
        ref_posture=np.mean(data,2)
    global_ref_posture = np.mean(ref_posture,0)
    Nsensors = np.int( data.shape[1] / dim )
    
    # At each frame, substract the ref_posture of the person, add the global_ref_posture
    data_SH = np.zeros(data.shape)
    ref_posture_SH = np.zeros(ref_posture.shape)
    for i in range(0,len(persons)):
        data_SH[i,:,:] = data[i,:,:] - np.reshape(ref_posture[i,:],(-1,1)) \
                                    + np.reshape(global_ref_posture,(-1,1))
        ref_posture_SH[i,:] = ref_posture[i,:] - ref_posture[i,:] + global_ref_posture
        
    if viz != False :  
        if colors is None : 
            colors = []
            for i in range(0,len(persons)) :
                colors.append(np.random.rand(3,))
                
        # Comparison of the ref posture, before norm. vs. after, for each person                         
        for i in range(0,len(persons)):
            compare_2frames(np.reshape(ref_posture[i,:],(Nsensors,dim)), \
                          np.reshape(ref_posture_SH[i,:],(Nsensors,dim)), \
                       "SI","SH", save_dir=output_dir + '/COMPAR_SH_person' + str(i+1) + '.pdf')
            plt.close()
            
        # Comparison of the Npers refererence postures after shape_norm
        compare_Nframes(np.reshape(ref_posture_SH,(len(persons),Nsensors,dim)), persons, colors, markers, save_dir=output_dir + '/COMPAR_allrefs_SH.pdf')
        plt.close()
        # Same plot + the new global reference posture
        compare_Nframes(np.reshape(ref_posture_SH,(len(persons),Nsensors,dim)), persons, colors, markers, save_dir=output_dir + '/COMPAR_allrefs_SH_mean.pdf',  \
                        mean=np.reshape(global_ref_posture,(1,Nsensors,dim)))
        plt.close()
        
    return data_SH, ref_posture_SH


def local_pos(global_pos, parent_joints, dim=3):
    ##########################################################################
    ##### Convert a global coord. matrix to local coord. matrix
    ##### 'global_pos' : global motion data (Npersons, NsensorsxNdim, Nframes) 
    ##### 'parent_joints' : i each sensor, list[i] the child sensor  
    ##### OUTPUTS : local coord. matrix
    ##########################################################################
    
    Nlabels =  global_pos.shape[0]; Nsensors = int (global_pos.shape[1] / dim ); Nframes = global_pos.shape[2]
    assert(len(parent_joints)==Nsensors-1)
    
    local_pos = np.zeros( global_pos.shape )
    for c in range(Nlabels):
        for i in range(Nframes) :
            local_pos[c,0:3,i] = global_pos[c,0:3,i]
            for j in range (1,Nsensors) :
                idx_p = parent_joints[j-1]
                local_pos[c,j*3:(j+1)*3,i] = global_pos[c,j*3:(j+1)*3,i] - global_pos[c,idx_p*3:(idx_p+1)*3,i]
            
    return local_pos


def local_to_global(local_pos, joint, parent_joints):
    ##########################################################################
    ##### Convert global to local coord of one sensor, at one frame
    ##### by searching the global coord of the parent joint, recursively
    ##### 'local_pos' : local motion data (NsensorsxNdim) - 'joint' : scalar
    ##### 'parent_joints' : i each sensor, list[i] the child sensor  
    ##### OUTPUTS : global coord. matrix
    ##########################################################################
    
    if joint==0:
        res = local_pos[joint*3:(joint+1)*3]
    else :
        res = local_pos[joint*3:(joint+1)*3] + local_to_global(local_pos, parent_joints[joint-1], parent_joints)
    return res


def local_pos_inv(local_pos, parent_joints, dim=3):
    ##########################################################################
    ##### Convert a local coord. matrix to global coord. matrix
    ##### 'local_pos' : local motion data (Npersons, NsensorsxNdim, Nframes) 
    ##### 'parent_joints' : i each sensor, list[i] the child sensor  
    ##### OUTPUTS : global coord. matrix
    ##########################################################################
    
    Npersons =  local_pos.shape[0]; Nsensors = int (local_pos.shape[1] / dim ); Nframes = local_pos.shape[2]
    assert(len(parent_joints)==Nsensors-1)
    
    global_pos = np.zeros( local_pos.shape )
    for c in range(Npersons):
        for i in range(Nframes) :
            global_pos[c,0:3,i] = local_pos[c,0:3,i]
            for j in range(1,Nsensors):
                global_pos[c,j*3:(j+1)*3,i] = local_to_global( local_pos[c,:,i], j, parent_joints)
                
    return global_pos
           
