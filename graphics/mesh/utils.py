import numpy as np

'''
convert a reference configuration in the ALE method into an current configuration, in any dimension

Input values:
    - 'x_ref': a list which stores the coordinates in the reference configuration
    - 'u': a list storing the components of the vector field, each component of the list is a function u_i(x)

Return values:
    - 'x_cur': a list which stores the coordinates in the current configuration
'''


def reference_to_current(x_ref, u):

    x_ref_transformed = np.array(x_ref)[None, :]

    x_cur = np.add(x_ref, [u[i](x_ref_transformed)[0] for i in range(len(u))])

    return list(x_cur)
