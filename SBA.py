"""
# Sparse-Bundle-Adjustments-with-GCPs
This python implementation of Sparse bundle adjustment based on the sparse Levenberg-Marquardt algorithm with Ground Control Points (GCPs).
A bundle adjusmtent problem arises in 3-D reconstruction and it can be formulated as follows (taken from https://en.wikipedia.org/wiki/Bundle_adjustment):
To derive accurate 3D geospatial information from imagery, it is necessary to establish the exterior orientation parameters.
EOPs, which define the position and orientation of the camera at the point of exposure in a mapping frame, can be established using either Ground Control Points (GCPs) through a Aerial triangulation (AT) process.
AT is one of the most critical steps in aerial photogrammetry to estimate the Tie points Object coordinates (OC) and EOPs which is performed with the bundle Adjustment (BA).
The basic photogrammetric principal geometry consists of three geometric entities: object space points (3D points),
corresponding image points (2D points), and perspective centers. Such a geometry can be formulized with collinearity equations.
 R_{ij} (i = 1,2,3,... , j = 1,2,3,...) stands for the nine elements of the rotation matrix , which can be modeled by three rotation Euler angles omega,
 phi and kappa.

R = r_{11} & r_{12} & r_{13}
    r_{21} & r_{22} & r_{23}
    r_{31} & r_{32} & r_{33}
    [P]        [X - X0]
    [S]  = R . [Y - Y0]
    [Q]        [Z - Z0]

X_0,Y_0 and Z_0 are the translation parameters for the camera station. 
Meanwhile, X,Y and Z are the object point coordinates usually given in meters in the mapping reference system (i.e., Earth-fixed coordinate system, in the case UTM)

"""







import os
import numpy as np
import Func as Fun

# 0 ---------------------------------User Inputs Dataset Address---------------------------------
dir_files = os.getcwd() + '/Dataset-2'

sigma_img = 0.6             # Image Accuracy
sigma_obj = 0.15            # Object Accuracy
Max_iter = 100              # Maximum iteration
th = 1e-8                   # Converge criteria

# 1 -------------------- Import Data --------------------
EOP_ref, EOP_init, IOP, TieXYZ, TieObs = Fun.Import_Data(dir_files)

# 2 -------------------- Preprocess --------------------
Observation_Tie, TieXYZ, camera_params = Fun.preprocess(TieXYZ, TieObs, EOP_init)
GCP, Observation_gcp = Fun.Control_from_xml(dir_files, Control_start_id=TieXYZ[-1, 0] + 1)
Info = Fun.Bundle_information(dir_files, GCP, TieXYZ, Observation_Tie, Observation_gcp, camera_params, IOP)

# 3 -------------------- Weight Matrix --------------------
Weight = Fun.Weight(Info.Tie_indices, Info.Gcp_indices, sigma_img, sigma_obj)

# 4 -------------------- Approximate Value --------------------
x0 = np.hstack((camera_params.ravel(), Info.points_3d.ravel()))

# 5 -------------------- Sparse Bundle Adjustment --------------------
BA = Fun.SBA(x0, Weight, Info, Max_iter, th, 1, Show=True)
