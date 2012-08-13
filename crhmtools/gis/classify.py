import crhmtools as ct
import numpy as np


def classify(file, nclass=2, name='landclass'):
    lc = ct.terrain.landclass()
    lc.open(file)

    #create the bins 
    hist, edges = np.histogram(lc._raster, bins=nclass)
    classes= np.zeros([nclass,2])
    output = np.zeros([lc.ysize(),lc.xsize()])

    #create a 2*n matrix to hold the edges for use in np
    for i in range(0,nclass):
        classes[i,:] = [edges[i],edges[i+1]]    

        c_value = np.ones([lc.ysize(),lc.xsize()]) * (i+1)
        c_start = edges[i]
        c_end   = edges[i+1]
        src = lc._raster
        mask = np.bitwise_and(
            np.greater_equal(src,c_start),
            np.less_equal(src,c_end))

        output = np.choose( mask, (output, c_value) )               


    lc._classified = output
    lc._classes = classes
    lc._nclass = nclass
    lc._name = name
    return lc