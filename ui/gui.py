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

class MainWindow(QMainWindow,Ui_MainWindow):

        def __init__(self):
                
                super(MainWindow,self).__init__()
                self.setupUi(self)
                self.setWindowTitle("CRHM Tools - 0.0.2a")
              
              #need to do the mpl init here otherwise it doesn't take up the full central widget
                self._init_mpl_view()
                
                self._init_lc_tree_view()
                self._init_menus()
                
                self.statusBar.showMessage('Ready')
                
                self._set_layout()
                self.showMaximized()
                
                #initialize the member variables
                self.basin = ct.terrain.basin()
                self.current_fig = '' #name of what we are plotting 
                
                loader = module_loader()
                self.modules = loader.load(	path = os.path.join(os.getcwd(),'modules'))
                
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

                #counter to guarantee a unique landclass name
                self.lc_count = 0
                
        #handle the click and double click events on the moule tree       
        def _handle_modtree_click_tip(self, item):
                try:
                        self.statusBar.showMessage(self.modules[self.mod_model.itemFromIndex(item).text()].description)
                except: #we need to handle the case where the user clicks the main parent item, which isn't a module
                        self.statusBar.showMessage(self.mod_model.itemFromIndex(item).text() + ' toolbox')
                        
        def _handle_modtree_dblclick_tip(self, item):
                try:
                        self.modules[self.mod_model.itemFromIndex(item).text()].run()
                except: #we need to handle the case where the user clicks the main parent item, which isn't a module
                        pass


        
        #setup the tree view with the initial items
        def _init_lc_tree_view(self):

                primary_land = QTreeWidgetItem(self.lc_tree)
                primary_land.setText(0,"Primary land classes")
                
                #secondary_land = QTreeWidgetItem(self.lc_tree)
                #secondary_land.setText(0,"Secondary land classes")
                
               
                
        #set up the matplotlib view
        def _init_mpl_view(self):
                self.plot_widget = QWidget()
                self.mpl_widget = mpl_view.mpl_widget(self.plot_widget )
        
        def _init_menus(self):
                
                #top menus
                self.actionPrimary.triggered.connect(self._open_landclass)
                self.actionSecondary.triggered.connect(self._open_landclass)
                self.actionGenerate_HRUs.triggered.connect(self._gen_hrus)
                
                
                #tree right-click context menu
                self.lc_tree.customContextMenuRequested.connect(self._context_menu)
                
        def _set_layout(self):
                hbox = QHBoxLayout()
                hbox.addWidget(self.mpl_widget.canvas)
                
                self.plot_widget.setLayout(hbox)                
                self.setCentralWidget(self.plot_widget)       
                self.lc_tree.resizeColumnToContents(0)
                self.lc_tree.resizeColumnToContents(1)
                
                
        def _gen_hrus(self):
                self.statusBar.showMessage('Creating HRUs...')
                self._hrus = self.basin.create_hrus()
                tw = QTreeWidgetItem()
                tw.setText(0,"HRUs")
                
                self.lc_tree.insertTopLevelItem(2,tw)
                
                self._add_to_primary_tree("HRUs",'Generated HRUs',self.basin.get_num_hrus(),'')
                self._plot_hru()
                self.statusBar.showMessage('Done')
                
                
        
        def _open_landclass(self):
                sender = self.sender()
                num_classes = 2 #default num of classes
                #the file to open
                fname, _ = QFileDialog.getOpenFileName(self, 'Open file')    
                #bail on cancle
                if fname == '':
                        return
                
                
                result = QInputDialog.getInt(self, "Number of classes", "Enter number of classes",value=2)
                
                #bail if we pressed cancel
                if not result[1]:
                        return
                
                num_classes = result[0]
                
               
                result = QInputDialog.getText(self,"Name of class","Enter name of the landclass",text='Landclass'+str(self.lc_count))
                self.lc_count+=1
                #bail if we cancel
                if not result[1]:
                        return
                name = result[0]
                
                self.statusBar.showMessage('Loading '+fname)
                
                
                self.basin.define_landclass(fname,name,num_classes)
                self.statusBar.showMessage('Done')

                
                self._add_to_primary_tree("Primary land classes",name, num_classes, fname)
                      
                       
                self._plot_landclass(name)  

        def _add_to_primary_tree(self, parent, name, num_classes, fname):
                it = self.lc_tree.findItems(parent,Qt.MatchFlag.MatchExactly)
                it=it[0] #returns a list, but we only need the first and only occurance
                
                #add the new dataset to the treeview
                child = QTreeWidgetItem(it)
                child.setText(0,name)
                child.setText(1,str(num_classes))
                child.setText(2,fname)
                it.setExpanded(True)
                
        def _context_menu(self,position):
                menu = QMenu()
                indexes = self.lc_tree.selectedIndexes()
                if len(indexes) > 0:           
                        
                        level = 0
                        index = indexes[0]
                        while index.parent().isValid():
                                index = index.parent()
                                level += 1                
                if level == 0:
                        menu.addAction("Load landclass")
                elif level == 1:
                        if index.data() == 'HRUs':
                                menu.addAction("Show")
                        else:
                                menu.addAction("Show classified")
                                menu.addAction("Show non-classified")
                                menu.addAction("Remove landclass")
                        
                #get what we clicked
                item=self.lc_tree.itemAt(position)
                #show menu
                a=menu.exec_(self.lc_tree.viewport().mapToGlobal(position))
                
                #no click
                if not a:
                        return
                
                #do the action
                if a.text() == "Load landclass":
                        self._open_landclass()
                elif a.text() == 'Show':
                        self._plot_hru()
                elif a.text() == 'Show classified':
                        self._plot_landclass(item.text(0),True)
                elif a.text() == 'Show non-classified':
                        self._plot_landclass(item.text(0),False)
                elif a.text() == 'Remove landclass':
                        
                        #remove plot if we are currently showing it
                        if self.current_fig == item.text(0):
                                self.mpl_widget.clear()
                            
                        self.basin.remove_landclass(item.text(0))
                        
                        self._rebuild_tree()

        def _rebuild_tree(self):
                self.lc_tree.clear()
                
                tw = QTreeWidgetItem()
                tw.setText(0,"Primary land classes")
                self.lc_tree.insertTopLevelItem(0,tw)
                
                #tw = QTreeWidgetItem()
                #tw.setText(0,"Secondary land classes")
                #self.lc_tree.insertTopLevelItem(1,tw)                        
                
                
                for i in self.basin._landclass.values():
                        self._add_to_primary_tree("Primary land classes",i.name(),i.get_nclasses(),i.get_file_name())
                        
                        
                        
                
        def _plot_hru(self):
                self.statusBar.showMessage('Plotting...')
                self.current_fig = 'hrus'
                
                self.mpl_widget.plot_hru(self._hrus)
                
                
                self.statusBar.showMessage('Done')       
                
        def _plot_landclass(self,name,classified=True):
                
                self.statusBar.showMessage('Plotting...')
                if classified:
                        r = self.basin(name).get_classraster()
                       
                else:
                        r = self.basin(name).get_raster()
                
                self.current_fig = name
                
                self.mpl_widget.plot_landclass(r)
                
                if classified:
                        self.mpl_widget.set_cb_ticks( list(range(1,self.basin(name).get_nclasses()+1)))
                        self.mpl_widget.set_cb_ticklabels(self.basin(name).get_classes_str())                
               
                self.statusBar.showMessage('Done')



