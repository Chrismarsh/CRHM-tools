import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 

    
class mod_manclass(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_manclass,self).__init__(imported_files,'./modules/manual_class.ui')

        self.name = 'Manual partioning'
        self.version = '1.0'
        self.description = 'Creates a landscape class by partitioning the domain in to n, user defined, partitions.'
        self.author = 'Chris Marsh'
        self.category = 'Statistics'
        
        self.nclasses = 0
        
        #connect the lineedit text changed signal 
        self.window.lineEdit.textChanged.connect(self.update_tableview)     
        #connect the cell changed signal to the validator function
        self.window.tableWidget.cellChanged.connect(self.validate_table)
        
        #give the line editor a validator so it only takes integers
        v=QtGui.QIntValidator(1,999,self.window.lineEdit)
        self.window.lineEdit.setValidator(v)
        
    #this is called when we change the number of
    def update_tableview(self,arg):
        try:
            self.nclasses = int(arg) #we know this to be valid because of our validator
        except ValueError:
            self.nclasses = 0
        self.window.tableWidget.setRowCount(self.nclasses)
        
    #this is called when a table cell is changed, so we can check if it has valid input   
    def validate_table(self,row,col):
        item = self.window.tableWidget.item(row,col) #get what was just changed
        v=QtGui.QDoubleValidator() #create a validator for doubles
        v.setRange(-99999,99999)
        if v.validate(item.text(),0)[0] == QtGui.QValidator.State.Invalid: #did our validator return an invalid vale?
            self.window.tableWidget.setItem(row,col,QtGui.QTableWidgetItem('0')) #just reset the cell to 0
            
    def init_run(self):
        
        try:
            #get the number of classes from the line edit widget
            nclasses=int(self.window.lineEdit.text())
            #get the name from the edit widget
            name = self.window.edit_name.text()
            if name == '':
                raise ValueError()
            
            edges = []
            for i in range(0,self.window.tableWidget.rowCount()):
                start = self.window.tableWidget.item(i,0)
                end = self.window.tableWidget.item(i,1)
                
                #empty list, so just insert
                if len(edges) == 0:
                    edges.append(int(start.text()))
                    edges.append(int(end.text()))
                else:
                #However!! if we have something like 0-90, 90-360, we don't want to add the 90 twice
                    prev = edges[-1]
                    cstart = int(start.text()) 
                    cend = int(end.text()) 
                    if prev != cstart:
                        edges.append(cstart)
                    edges.append(cend)            


            kwargs={}
            kwargs['nbin']=nclasses
            kwargs['name']=name
            kwargs['edges']=edges
            
            return kwargs          
        except ValueError:
            self.mbox_error('Invalid number of classes or blank name field')
        except:
            self.mbox_error('Invalid data in class table')

        return None
 
    #This is what can be called from the command line if wanted
    def exec_module(self,**kwargs):
        
        r = self.selected_file.copy()
        r._name = kwargs['name']
        r.set_creator(self.name)

        return ct.gis.classify(r,kwargs['nbin'],kwargs['edges'],kwargs['name'])
    
    


 
 