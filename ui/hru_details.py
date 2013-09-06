from PySide import QtGui, QtCore,QtUiTools 
import crhmtools as ct
import numpy as np

class HRUDetails(QtGui.QMainWindow):
    def __init__(self, parent, basin, secondary_lc, imported_files,generated_files):
        super(HRUDetails,self).__init__(parent=parent)

        #load the UI file
        file = QtCore.QFile('./ui/hru_details.ui')
        file.open(QtCore.QFile.ReadOnly)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load(file,self)
        file.close() 

        self.basin = basin
        self.slc = secondary_lc
        self.imported_files = imported_files
        self.generated_files = generated_files
        
        self.window.setWindowTitle('HRU details - CRHM Tools')
        #setup menubar
        self.window.actionClose.triggered.connect(self.window.close)
        
    def show(self):
        #setup the grid
        nhru = self.basin.get_num_hrus()
        self.window.tableWidget.setColumnCount(nhru)
        self.window.tableWidget.setRowCount(len(self.slc)+1) #+1 to account for the extra line for the area
        
        for i in range(0,nhru):
            header = QtGui.QTableWidgetItem('HRU ' + str(i+1))
            self.window.tableWidget.setHorizontalHeaderItem(i,header)

        
        for i in range(0,len(self.slc)):
            header = QtGui.QTableWidgetItem('Mean of ' + self.slc[i])
            self.window.tableWidget.setVerticalHeaderItem(i,header)   
        
        header = QtGui.QTableWidgetItem('Area (km^2)')
        self.window.tableWidget.setVerticalHeaderItem(len(self.slc),header)   
        
        #calculate the mean for each HRU
        for i in range(0,nhru):
            for j in range(0,len(self.slc)):
                try:
                    mean = np.mean(self.imported_files[self.slc[j]].get_raster()[self.basin._hrus._raster  == i+1])
                except:
                    mean = np.mean(self.generated_files[self.slc[j]].get_raster()[self.basin._hrus._raster  == i+1])
                    
                item = QtGui.QTableWidgetItem('{0:.2f}'.format(mean))
                self.window.tableWidget.setItem(j,i,item) #intentional i,j flip here
        
        #calculate the area of each HRU
        for i in range(0,nhru):
            total = (self.basin._hrus._raster  == i+1).sum()
            total = total * abs(self.basin._hrus.get_resolution()[0]*self.basin._hrus.get_resolution()[1]) / 10**6 # to km^2
                
            item = QtGui.QTableWidgetItem('{0:.2f}'.format(total))
            self.window.tableWidget.setItem(len(self.slc),i,item) #intentional i,j flip here        

        self.window.show()
        
