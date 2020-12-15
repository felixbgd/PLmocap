# PLmocap

A Python library for machine learning, feature analysis, and visualization based on motion capture data. 

Preprocessing : 
- size_norm : Size normalization of the skeletons in a mocap dataset with multiple persons.
- shape_norm : Shape normalization of the skeletons in a mocap dataset with multiple persons.
- local_pos and local_pos_inv : Conversion from global to local coordinates, and its inverse function. 

Viz : 
- data_viz_3d : Animated visualization of mocap data in the 3D space
- data_viz_2d : Animated visualization of mocap data in the 2D frontal plane
- plot_frame : Visualization of 1 frame of mocap data in 2D or 3D
- compare_2frames : Comparison of 2 postures of mocap data in the 2D frontal plane
- compare_Nframes : Comparison of N postures of mocap data in the 2D frontal plane
- video_PL : Exports a mocap video as point lights in the 2D frontal plane (using ffmpeg)
- plot_3frames : 3-frame visualization of mocap data in 2D, to describe motion

Classif : 
- class_logReg : Multinomial logistic regression with leave-one-observation-out validation 

Stats.py coming soon, with a set of functions to compute differential features of motion (velocities, accelerations...) and apply stats on it...
