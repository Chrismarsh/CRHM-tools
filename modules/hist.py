import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_hist(module_base):
    def __init__(self,imported_files):
        super(mod_hist,self).__init__(imported_files,'./modules/hist_ui.ui')
        
        
        self.name = 'Histogram partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the histogram in to n partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'

    def run(self):
        self.show_ui()
        
        if self.ok_exit == True:
            c=int(self.window.lineEdit.text())
            name = self.window.edit_name.text()

            if c  <= 0:
                mbox =QtGui.QMessageBox()
                mbox.setText("Cannot have <=0 bins.")
                mbox.exec_()
                return
            
            lc = self.classify( self.selected_file, c, name)
            return lc
        
        return None
        
    def classify(self, file , nclass=2, name='landclass'):
       #inspired by http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/classify.py
     
        lc = ct.terrain.landclass()
        lc.open(self.selected_file)
        
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


 
 