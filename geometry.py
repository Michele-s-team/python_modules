import numpy as np

#euclidean  norm of vector x
def eucl_norm(x):
    return (np.sqrt( np.dot( x, x ) ))

#the vectors tangent to the curvilinear coordinates on the manifold : e(z)[i] = e_i_{al-izzi2020shear}
def e(omega):
    return [[1, 0, omega[0]], [0, 1, omega[1]]]

#MAKE SURE THAT THIS NORMAL IS DIRECTED OUTWARDS
#normal(z) = \hat{n}_{al-izzi2020shear}
def normal(omega):
    return np.cross(e(omega)[0], e(omega)[1]) /  eucl_norm(np.cross(e(omega)[0], e(omega)[1]))
#MAKE SURE THAT THIS NORMAL IS DIRECTED OUTWARDS