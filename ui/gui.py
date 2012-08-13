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


from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *


from mainwindow import *

#import matplotlib

### Added for PySide
#matplotlib.use('Qt4Agg')
#matplotlib.rcParams['backend.qt4']='PySide'

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from matplotlib.figure import Figure
#from mpl_toolkits.axes_grid1 import make_axes_locatable

import mpl_view 
import crhmtools as ct
from module_loader import *

class BoldDelegate(QtGui.QStyledItemDelegate):

    def paint(self, painter, option, index):
        if index.data(QtCore.Qt.UserRole) == 1:
            option.font.setWeight(QtGui.QFont.Bold)
            
        QtGui.QStyledItemDelegate.paint(self, painter, option, index)    
        
class MainWindow(QMainWindow,Ui_MainWindow):

    def __init__(self):

        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("CRHM Tools - 0.0.2a")

        #holds the loaded & imported files
        self.import_files = {}                
        #load the dynamic modules
        loader = module_loader()

        self.modules = loader.load(os.path.join(os.getcwd(),'modules'),self.import_files)              
        self.current_fig = '' #name of what we are plotting 
        self.current_fig_item = None #reference to the QItem for the current figure (saves us having to look it up each time)
        #counter to guarantee a unique landclass name
        self.lc_count = 0
        
        #need to do the mpl init here otherwise it doesn't take up the full central widget
        self._init_mpl_view()

        self._init_lc_treeview_view()
        self._init_menus()


        self._set_layout()
        self.showMaximized()

        #initialize the member variables
        self.basin = ct.terrain.basin()


        self.statusBar.showMessage('Ready')

    #handle the click and double click events on the module tree       
    def _handle_modtree_click_tip(self, item):
        try:
            self.statusBar.showMessage(self.modules[self.mod_model.itemFromIndex(item).text()].description)
        except KeyError: #we need to handle the case where the user clicks the main parent item, which isn't a module
            self.statusBar.showMessage(self.mod_model.itemFromIndex(item).text() + ' toolbox')

    def _handle_modtree_dblclick_tip(self, item):
        try:
            lc = self.modules[self.mod_model.itemFromIndex(item).text()].run()
            if lc != None:
                self.basin.add_landclass(lc)
                parent = self.lc_model.findItems('Primary land classes').pop()
                item  = QStandardItem(lc._name)
                item.setDragEnabled(False)
                parent.appendRow(item)                        
        except KeyError: #we need to handle the case where the user clicks the main parent item, which isn't a module
            #unclear why this doesn't actually expand it.
            expand = not(self.treeView.isExpanded(self.treeView.currentIndex()))
            self.treeView.setExpanded(item,expand)

    #setup the tree view with the initial items
    def _init_lc_treeview_view(self):

        #initialize the landclass treeview
        #self.lc_model = QtGui.QStandardItemModel()
        self.lc_model = LCTreeViewModel()
        self.lc_treeview.setModel(self.lc_model)
        self.lc_treeview.setItemDelegate(BoldDelegate(self))

        parent = self.lc_model.invisibleRootItem()
        parent.setDropEnabled(False)

        primary_land = QStandardItem('Imported files')
        primary_land.setDragEnabled(False)
        self.lc_model.appendRow(primary_land)                

        primary_land = QStandardItem('Primary land classes')
        primary_land.setDragEnabled(False)
        primary_land.setDropEnabled(False)
        self.lc_model.appendRow(primary_land)

        primary_land = QStandardItem('Secondary land classes')
        primary_land.setDragEnabled(False)
        self.lc_model.appendRow(primary_land)                

        primary_land = QStandardItem('Generated HRUs')
        primary_land.setDragEnabled(False)
        primary_land.setDropEnabled(False)
        self.lc_model.appendRow(primary_land)               

    #initialize the module treeivew
        self.mod_model = QtGui.QStandardItemModel()
        self.treeView.setModel( self.mod_model)
        parent =  self.mod_model.invisibleRootItem()

        #loop through all the modules and add them to the tree
        for m,obj in self.modules.items():
            #try to find the category in the tree
            index = self.mod_model.findItems(obj.category)

            if index == []: #missing, so add it
                parent = self.mod_model.invisibleRootItem()
                item = QStandardItem(obj.category)
                parent.appendRow(item)
                parent = item #make the parent the new category
            else:
                parent = index.pop() #because this returns a list, we need the only item in this list. Multiple finds shouldn't happen (famous last words)
            #add the tool to the view        
            parent.appendRow(QStandardItem(obj.name))


        #connect the double click event to the .run() of the module
        self.treeView.doubleClicked.connect(self._handle_modtree_dblclick_tip)
        #connect single click event to the .description of the module and show it
        self.treeView.clicked.connect(self._handle_modtree_click_tip)


    #set up the matplotlib view
    def _init_mpl_view(self):
        self.plot_widget = QWidget()
        self.mpl_widget = mpl_view.mpl_widget(self.plot_widget )

    def _init_menus(self):

        #top menus
        self.actionImport_file.triggered.connect(self._import_file)

        self.actionGenerate_HRUs.triggered.connect(self._gen_hrus)


        #tree right-click context menu
        self.lc_treeview.customContextMenuRequested.connect(self._context_menu)


    def _set_layout(self):
        hbox = QHBoxLayout()
        hbox.addWidget(self.mpl_widget.canvas)

        self.plot_widget.setLayout(hbox)                
        self.setCentralWidget(self.plot_widget)       
        self.lc_treeview.resizeColumnToContents(0)
        self.lc_treeview.resizeColumnToContents(1)


    def _gen_hrus(self):
        self.statusBar.showMessage('Creating HRUs...')

        if self.basin.get_num_landclass() == 0:
            self.statusBar.showMessage('No landclasses')
            return
        
        slc = self.lc_model.findItems('Secondary land classes').pop() #comes back as a list, but we know there is only 1
        
        secondary_lc=[]
        for i in range(0,slc.rowCount()):
            secondary_lc.append(slc.child(i).text())
        
        
        self._hrus = self.basin.create_hrus()

        parent = self.lc_model.findItems('Generated HRUs').pop()
        parent.appendRow(QStandardItem('HRU'))


        #self.lc_treeview.expand(parent.index())

        self._plot_hru()
        self.statusBar.showMessage('Done')


    def _import_file(self):
        #the file to open
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file')    
        #bail on cancel
        if fname == '':
            return                
        self.statusBar.showMessage('Loading '+fname)
        name,ext = os.path.splitext(os.path.split(fname)[-1])

        self.import_files[name] = ct.terrain.raster()
        self.import_files[name].open(fname)

        self.statusBar.showMessage('Done')

        parent = self.lc_model.findItems('Imported files').pop()
        it = parent.appendRow(QStandardItem(name))
        self.lc_treeview.expand(parent.index())           
        


    def _context_menu(self,position):
        menu = QMenu()
        indexes = self.lc_treeview.selectedIndexes()
        #get what we clicked
        item=self.lc_model.itemFromIndex(self.lc_treeview.currentIndex())

        if len(indexes) > 0:           

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1                
        if level == 0 and item.text() == 'Generated HRUs':
            menu.addAction('Generate HRUs from primary')
        elif level == 0 and item.text() == 'Imported files':
            menu.addAction('Import file')
        elif level == 1:
            if index.data() == 'Generated HRUs':
                menu.addAction("Show HRU")
            elif index.data() == 'Imported files':
                menu.addAction('Show')
            elif index.data() == 'Primary land classes':
                menu.addAction("Show classified")
                menu.addAction("Show non-classified")
                menu.addAction("Remove landclass")


        #show menu at the point we clicked
        a=menu.exec_(self.lc_treeview.viewport().mapToGlobal(position))

        #no click
        if not a:
            return

        #do the action
        if a.text() == 'Import file':
            self._import_file()
        elif a.text() == 'Show':
            self._plot_imported(item.text())
        elif a.text() == 'Show HRU':
            self._plot_hru()
        elif a.text() == 'Show classified':
            self._plot_landclass(item.text(),True)
        elif a.text() == 'Show non-classified':
            self._plot_landclass(item.text(),False)
        elif a.text() == 'Remove landclass':

            #remove plot if we are currently showing it
            if self.current_fig == item.text():
                self.mpl_widget.clear()
                self.current_fig_item = None

            self.lc_model.removeRow(item.row(),parent=item.parent().index())   
         
            self.basin.remove_landclass(item.text())
        elif a.text() == 'Generate HRUs from primary':
            self._gen_hrus()
        
        #set the current figure to be the bolded text
        if 'Show' in a.text():
            if  self.current_fig_item:
                self.current_fig_item.setData(0,QtCore.Qt.UserRole) #unbold 
                
            item.setData(1,QtCore.Qt.UserRole)
            self.current_fig_item = item


    def plot(self,name,raster):
        self.statusBar.showMessage('Plotting...')
        
        self.current_fig = name
        self.mpl_widget.plot(raster)
        self.statusBar.showMessage('Done')     

    def _plot_hru(self):
        self.plot('hrus',self._hrus)
        
    
    def _plot_imported(self, name):

        r=self.import_files[name].get_raster()
        self.plot('imported_'+name,r)

    def _plot_landclass(self,name,classified=True):

        if classified:
            r = self.basin(name).get_classraster()

        else:
            r = self.basin(name).get_raster()

        self.plot(name,r)

        if classified:
            self.mpl_widget.set_cb_ticks( list(range(1,self.basin(name).get_nclasses()+1)))
            self.mpl_widget.set_cb_ticklabels(self.basin(name).get_classes_str())                



