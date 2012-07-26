from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *

from mainwindow import *

import matplotlib

## Added for PySide
matplotlib.use('Qt4Agg')
matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable

import crhmtools as ct


class MainWindow(QMainWindow,Ui_MainWindow):
        def __init__(self):
                
                super(MainWindow,self).__init__()
                self.setupUi(self)
                self.setWindowTitle("CRHM Tools")
              
              #need to do the mpl init here otherwise it doesn't take up the full central widget
                self._init_mpl_view()
                
                self._init_lc_tree_view()
                self._init_menus()
                
                self.statusBar.showMessage('Ready')
                
                self._set_layout()
                self.showMaximized()
                #initialize the member variables
                self.basin = ct.terrain.basin()
                self.curr_cb = None
                self.current_fig = ''
                
                #counter to guarantee a unique landclass name
                self.lc_count = 0
                
        #setup the tree view with the initial items
        def _init_lc_tree_view(self):
                primary_land = QTreeWidgetItem(self.lc_tree)
                primary_land.setText(0,"Primary land classes")
                
                secondary_land = QTreeWidgetItem(self.lc_tree)
                secondary_land.setText(0,"Secondary land classes")
                
               
                
        #set up the matplotlib view
        def _init_mpl_view(self):
                self.mpl_view = QWidget()
                self.fig = Figure() #(6.0, 4.0)
                
                
                self.axes = self.fig.add_subplot(111)     
                
                self.canvas = FigureCanvas(self.fig)
                self.canvas.setParent(self.mpl_view)
        
        def _init_menus(self):
                
                #top menus
                self.actionPrimary.triggered.connect(self._open_landclass)
                self.actionSecondary.triggered.connect(self._open_landclass)
                self.actionGenerate_HRUs.triggered.connect(self._gen_hrus)
                
                
                #tree right-click context menu
                self.lc_tree.customContextMenuRequested.connect(self._context_menu)
                
        def _set_layout(self):
                hbox = QHBoxLayout()
                hbox.addWidget(self.canvas)
                                
                self.mpl_view.setLayout(hbox)                
                self.setCentralWidget(self.mpl_view)       
                self.lc_tree.resizeColumnToContents(0)
                self.lc_tree.resizeColumnToContents(1)
        def _gen_hrus(self):
                self.statusBar.showMessage('Creating HRUs...')
                self._hrus = self.basin.create_hrus()
                tw = QTreeWidgetItem()
                tw.setText(0,"HRUs")
                
                self.lc_tree.insertTopLevelItem(2,tw)
                
                self._add_to_primary_tree("HRUs",'Generated HRUs',self.basin.get_num_hrus(),'')
                
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
                                self._clear_plot()
                            
                        self.basin.remove_landclass(item.text(0))
                        
                        self.lc_tree.clear()
                        
                        tw = QTreeWidgetItem()
                        tw.setText(0,"Primary land classes")
                        self.lc_tree.insertTopLevelItem(0,tw)
                        
                        tw = QTreeWidgetItem()
                        tw.setText(0,"Secondary land classes")
                        self.lc_tree.insertTopLevelItem(1,tw)                        
                        
                        
                        for i in self.basin._landclass.values():
                                self._add_to_primary_tree("Primary land classes",i.name(),i.get_nclasses(),i.get_file_name())
                        
                        
                        
                
        def _plot_hru(self):
                self.statusBar.showMessage('Plotting...')
                self.current_fig = 'hrus'
                self._clear_plot()
                h=self.axes.imshow(self._hrus)
                
                divider = make_axes_locatable(self.axes)
                cax = divider.append_axes("right", size="5%", pad=0.05)
                
                self.curr_cb=self.fig.colorbar(h,cax=cax) 
                
                
                self.canvas.draw()
                self.statusBar.showMessage('Done')       
                
        def _plot_landclass(self,name,classified=True):
                
                self.statusBar.showMessage('Plotting...')
                if classified:
                        r = self.basin(name).get_classraster()
                       
                else:
                        r = self.basin(name).get_raster()
                
                self.current_fig = name
                
                self._clear_plot()

                h=self.axes.imshow(r)
                divider = make_axes_locatable(self.axes)
                cax = divider.append_axes("right", size="5%", pad=0.05)
                
                self.curr_cb=self.fig.colorbar(h,cax=cax)
                
                if classified:
                        self.curr_cb.set_ticks( list(range(1,self.basin(name).get_nclasses()+1)))
                        self.curr_cb.set_ticklabels(self.basin(name).get_classes_str())
                
                self.canvas.draw()
                self.statusBar.showMessage('Done')

        def _clear_plot(self):
                self.axes.clear()  
                
                
                
                #remove the old colorbar
                if self.curr_cb:
                        self.fig.delaxes(self.fig.axes[1])
                        self.fig.subplots_adjust(right=0.90) 
                        self.curr_cb=None
                self.canvas.draw()        
                

