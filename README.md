# PLmocap

A Python library for machine learning, motion analysis and visualization of motion capture data. 

Pre-processing:

- Normalizations of the structural features of the body of the moving person. Mocap data can be normalized with respect to size or shape of the body. 
- Transformation of the mocap data from global reference system to local reference system. + inverse function from local to global.

Visualization:

- data_viz_3d: Animated real-time visualization of mocap data in the 3D space, shown as Point- Light Display or stick figure. One specific body marker can be highlighted.

- data_viz_2d: Animated real-time visualization of mocap data in the 2D frontal plane, shown as Point-Light Display or stick figure. One specific body marker can be highlighted.

- plot_frame: Visualization of 1 given frame of mocap data in 2D or 3D, shown as Point-Light Display or stick figure.

- compare_Nframes: Comparison of N postures of mocap data in the 2D frontal plane.

- video_PL: Generation of a mocap video as Point- Light Display in 2D in either the frontal, sagittal or transverse plane, exported in MPEG-4 format (using ffmpeg).

- plot_2frames: Visualization of mocap data in 2D at 2 given frames, in either the frontal, sagittal or transverse plane. The 2 postures are shown as overlapped gray and black stick figures.

- plot_3frames: Visualization of mocap data in 2D at 3 given frames, in either the frontal, sagittal or transverse plane. The 3 postures are shown side-by-side. Overlapping stick figures of two different individuals

Classification:

- Classification of mocap data using Multinomial Logistic Regression.
- Classification of mocap data using Support Vector Machine (without a kernel, or with RBF kernel).
