#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 15:44:10 2020

@author: felixbigand
"""

from funcs_c3d import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
import numpy as np
import os

def size_norm(data,ref_posture=None,persons=np.arange(4),output_dir=os.getcwd(),colors=None,viz=True,dim=3) :
    
    ## The input (xyz) data 'data' must be in the format Npersons x (Nsensorsxdim) x Nframes
    ## 'ref_posture' (Npersons x Nsensors) is the average of postures across frames, if None
    ## 'persons' is the list of the labels given to the different persons in the mocap dataset
    ## Figures are saved on 'output_dir', if 'viz'!=None
    
    if ref_posture is None :
        ref_posture=np.mean(data,2)
    global_ref_posture = np.mean(ref_posture,0)
    Nsensors = np.int( data.shape[1] / dim )
    
    # Regression bt each average posture and global average posture
    reg_slope = []
    reg_offset = []
    for i in range(0,len(persons)):
        reg = LinearRegression(False).fit(np.reshape(global_ref_posture,(-1,1)),np.reshape(ref_posture[i,:],(-1,1)))
        reg_slope.append(reg.coef_)
        reg_offset.append(reg.intercept_)
    
    # Compute relative sizes of each person    
    relative_size=np.round( np.reshape(np.asarray(reg_slope),(len(persons),1)) , 3)
    offset= np.reshape(np.asarray(reg_offset),(len(persons),1))
    
    # Plots (optimized for 4 persons)
    if viz != False : 
        # Scatterplots of the sensors of each person in the reference posture, 
        # as a function of the global reference posture (fig)
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
    # regression bt each average posture and global average posture
    reg_slope_SI = []
    reg_offset_SI = []
    for i in range(0,len(persons)):
        reg_SI = LinearRegression(False).fit(np.reshape(global_ref_posture_SI,(-1,1)), np.reshape(ref_posture_SI[i,:],(-1,1)))
        reg_slope_SI.append(reg_SI.coef_)
        reg_offset_SI.append(reg_SI.intercept_)
     
    # Compute new relative sizes    
    relative_size_SI= np.round( np.reshape(np.asarray(reg_slope_SI),(len(persons),1)) , 3)
    offset_SI= np.reshape(np.asarray(reg_offset_SI),(len(persons),1))
    
    # Plots
    if viz != False : 
        # Scatterplots of the sensors of each person in the new reference posture, 
        # as a function of the global reference posture
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
    
        # Comparison of the sensors positions in the reference posture, between 
        # size_norm and after, for each person
        for i in range(0,len(persons)):
            compare_frame(np.reshape(ref_posture[i,:],(1,Nsensors,dim)), \
                          np.reshape(ref_posture_SI[i,:],(1,Nsensors,dim)), \
                       "ORI","SI", save=output_dir + '/COMPAR_SI_person' + str(i+1) + '.pdf')
            plt.close()
        # Comparison of the Npers refererence postures after size_norm
        compare_allrefs(np.reshape(ref_posture_SI,(len(persons),Nsensors,dim)), persons, colors, save=output_dir + '/COMPAR_allrefs_SI.pdf')
        plt.close()
        # Comparison of the Npers refererence postures after size_norm + the new global reference posture
        compare_allrefs(np.reshape(ref_posture_SI,(len(persons),Nsensors,dim)), persons, colors, save=output_dir + '/COMPAR_allrefs_SI_mean.pdf',  \
                        mean=np.reshape(global_ref_posture_SI,(1,Nsensors,dim)))
        plt.close()
        
    return data_SI, ref_posture_SI

def shape_norm(data,ref_posture=None,persons=np.arange(4),output_dir=os.getcwd(),colors=None,viz=True,dim=3) :
    
    ## The input (xyz) data 'data' must be in the format Npersons x (Nsensorsxdim) x Nframes
    ## 'ref_posture' (Npersons x Nsensors) is the average of postures across frames, if None
    ## 'persons' is the list of the labels given to the different persons in the mocap dataset
    ## Figures are saved on 'output_dir', if 'viz'!=None
    ## USE SHAPE_NORM ON SIZE_NORM DATA IF YOU WANT A COMPLETE MORPHOLOGICAL NORM
    
    if ref_posture is None :
        ref_posture=np.mean(data,2)
    global_ref_posture = np.mean(ref_posture,0)
    Nsensors = np.int( data.shape[1] / dim )
    
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
        # Comparison of the sensors positions in the reference posture, between 
        # shape_norm and after, for each person                          
        for i in range(0,len(persons)):
            compare_frame(np.reshape(ref_posture[i,:],(1,Nsensors,dim)), \
                          np.reshape(ref_posture_SH[i,:],(1,Nsensors,dim)), \
                       "SI","SH", save=output_dir + '/COMPAR_SH_person' + str(i+1) + '.pdf')
            plt.close()
        # Comparison of the Npers refererence postures after shape_norm
        compare_allrefs(np.reshape(ref_posture_SH,(len(persons),Nsensors,dim)), persons, colors, save=output_dir + '/COMPAR_allrefs_SH.pdf')
        plt.close()
        # Comparison of the Npers refererence postures after shape_norm + the new global reference posture
        compare_allrefs(np.reshape(ref_posture_SH,(len(persons),Nsensors,dim)), persons, colors, save=output_dir + '/COMPAR_allrefs_SH_mean.pdf',  \
                        mean=np.reshape(global_ref_posture,(1,Nsensors,dim)))
        plt.close()
        
    return data_SH, ref_posture_SH
        