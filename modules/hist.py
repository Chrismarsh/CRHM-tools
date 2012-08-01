import numpy as np
import crhmtools as ct

from PySide import QtGui 

    
class mod_hist():
    def __init__(self):
        self.name = 'Histogram partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the histogram in to n partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'
        
    def run(self):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Hello world from mod_hist()")
        msgBox.exec_()        