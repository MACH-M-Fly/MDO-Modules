from lib_spline import getPoints, getThickness ,getThickness_cs, getArea
import numpy as np



def getY(shape_vars):
	Y = np.concatenate((np.array([TE_gap/2.0]),shape_vars[:(numDV/2+1)] , np.array([0.0]),\
	 -1*shape_vars[numDV/2:(numDV/2+1)], shape_vars[(numDV/2+1):]  , np.array([-1*TE_gap/2.0 ]))) 
	Y = np.array([Y])

	return Y

# ======================================================================
#         Setup 
# ======================================================================



# Constants 
TE_gap = 0.005
Cl_star = 0.824


# Declare X position of control points 
X = np.concatenate( ( np.linspace(1.0, 0.0, 11), np.array([0.0]), np.linspace(0.0, 1.0, 11) ) ) 
# Create array of an array so X.T works 
X = np.array([X])


# Declare X positions to measure thickness
thick_points = [0.001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]


# calculate the number of varibles used to control the shape of the airfoil
numDV = len(X[0]) - 4


# ------------------ Calculate initial thickness -------------------------
   							 

shape_vars_start = np.array([  0.02 ,    0.035,    0.0475 ,  0.0575, 0.0625,   0.0625 ,  0.05875,  0.0525 ,  0.04 ,    0.015, \
  							  -0.04 ,   -0.0525,  -0.05875  ,-0.06 ,-0.05125 ,-0.03875, -0.02375, -0.01,     0.0025 ]) 


Y = getY(shape_vars_start)
cv = np.concatenate((X.T, Y.T), axis = 1)


    
points_initial = getPoints(P=cv, n=3, V_type="clamped")
thickness_initial = getThickness(thick_points, points_initial)
area_initial = getArea(points_initial)
