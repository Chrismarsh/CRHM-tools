from PySide import QtGui
from ui.gui import *
import sys

app = QtGui.QApplication(sys.argv)

window =  MainWindow()
window.show()
sys.exit(app.exec_())

"""
basin = ct.basin()
base='/Volumes/Local Disk/Users/Chris/Documents/Academic/2012 CRHM/crhmtools/'
print 'Loading dem...'
basin.define_landclass(base+'dem1m.asc', name='DEM', nclass=6)
print 'Loading slope...'
basin.define_landclass(base+'slope1m.asc', name='slope', nclass=2)
#print 'Loading aspect'
#basin.define_landclass(base+'aspect1m.asc', name='aspect', nclass=2)



#print 'Creating HRUs'
HRU = basin.create_hrus()

basin.show()


import matplotlib.pyplot as plt
plt.figure()
plt.imshow(HRU)
plt.show()
"""