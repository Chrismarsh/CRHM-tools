import crhmtools as ct
import numpy as np


def classify(landclass=None, nclass=2, edges=[], name='landclass'):

    classes= np.zeros([nclass,2])
    output = np.zeros([landclass.ysize(),landclass.xsize()])

    #create a 2*n matrix to hold the edges for use in np
    for i in range(0,nclass):
        classes[i,:] = [edges[i],edges[i+1]]    

        c_value = np.ones([landclass.ysize(),landclass.xsize()]) * (i+1)
        c_start = edges[i]
        c_end   = edges[i+1]
        src = landclass._raster
        mask = np.bitwise_and(
            np.greater_equal(src,c_start),
            np.less_equal(src,c_end))

        output = np.choose( mask, (output, c_value) )               

    
    landclass._classified = output
    landclass._classes = classes
    landclass._nclass = nclass
    landclass._name = name

    return landclass