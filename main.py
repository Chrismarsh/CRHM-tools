#Copyright (C) 2012  Chris Marsh

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


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