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


'''
check if a point lies within a triangle
Input values: 
    - 'p1', 'p2', 'p3': the two-dimensional coordinates of the vertices of the triangle
    - 'q': the point
    
Return values: 
    - True if q is in the triangle, False otherwise

'''
def point_in_triangle(p1, p2, p3, q):

    # vectors joining the vertices
    vector_12 = np.subtract(p1, p2)
    vector_23 = np.subtract(p2, p3)
    vector_31 = np.subtract(p3, p1)
    
    # midpoints between vertices
    midpoint_12 = np.add(p1, p2)/2
    midpoint_23 = np.add(p2, p3)/2
    midpoint_31 = np.add(p3, p1)/2
    
    # normals to vectors joining the vertices
    normal_12 = [-vector_12[1], vector_12[0]]
    normal_23 = [-vector_23[1], vector_23[0]]
    normal_31 = [-vector_31[1], vector_31[0]]
    
    # check if q is on the same side as p3 with respect to normal_12, and similarly for other edges
    check_12 = (np.dot(np.subtract(q, midpoint_12), normal_12) * np.dot(np.subtract(p3, midpoint_12), normal_12) > 0 )
    check_23 = (np.dot(np.subtract(q, midpoint_23), normal_23) * np.dot(np.subtract(p1, midpoint_23), normal_23) > 0 )
    check_31 = (np.dot(np.subtract(q, midpoint_31), normal_31) * np.dot(np.subtract(p2, midpoint_31), normal_31) > 0)
    
    # the point is in the triangle if all checks evaluate to True
    return check_12 and check_23 and check_31
   