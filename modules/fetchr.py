import numpy as np
import crhmtools as ct
from ui.module_base import  *
from PySide import QtGui, QtCore,QtUiTools 
from scipy import weave
#Base oned code from FetchR:
#! Original program written March 1990; current version written June 1992.
#! Resurrected July 2008

#! Programmers:
#!     Lawrence W. Martz and David R. Lapen

class mod_fetchR(module_base):
    def __init__(self,imported_files):
        
        #load the ui file
        super(mod_fetchR,self).__init__(imported_files,'./modules/fetchr_ui.ui')

        self.name = 'FetchR'
        self.version = '1.0'
        self.description = 'Creates a raster of Fetches.'
        self.author = 'Chris Marsh'
        self.category = 'Process'

        #set a validator to the linedit so it only accepts integers
        v=QtGui.QIntValidator(1,999,self.window.lineEdit)
        self.window.lineEdit.setValidator(v)    
        
    def init_run(self):
    
        try:
           #height of obstructing terrain
            height=int(self.window.lineEdit.text())
            #get the name from the edit widget
            name = self.window.edit_name.text()
            if name == '':
                raise ValueError()
            direction = self.window.cb_direction.currentText()
            
            kwargs={}
            kwargs['file']=self.selected_file
            kwargs['height']=height
            kwargs['name']=name
            kwargs['wind_dir']=direction
            #call our main handler
            return kwargs
        except ValueError:
            self.mbox_error('Invalid field. Perhaps a field is empty?')
        
            return None
    
    #This is what can be called from the command line if wanted
    #@profile
    def exec_module(self,**kwargs):
        #create a new landclass
        r = ct.terrain.landclass()
        r.set_creator(self.name)
        r._name = kwargs['name']
        #open the file
        r.open(kwargs['file'])
        fetch = np.zeros(r.xsize()*r.ysize()).reshape(r.ysize(),r.xsize())
        #hard-coded direction, fixup later
        direction = kwargs['wind_dir']
        elev = kwargs['height']
        
        
        #self.window.progressBar.setRange(0,r.ysize())
        #self.window.progressBar.setTextVisible(True)
        
        #default views
        r_view = r._raster
        f_view = fetch        
        for i in range(0,r.ysize()):
            for j in range(0,r.xsize()):
                
                
                if direction == 'N': #for NORTH
                    s=r._raster[:i,j][::-1] #[::-1] is because we are looking north, so need to flip the results, same for West

                elif direction == 'S': #SOUTH
                    s = r._raster[i:,j]  
  
                elif direction == 'E':#east
                    s = r._raster[i,j:] 

                elif direction == 'W':#west
                    s = r._raster[i,:j] [::-1] 

                elif direction == 'NE': # we end up traversing the flipped array, so need to be using [::-1] everywhere otherwise in correct indexing is used because a[i,j]!=a[::-1][i,j]
                    s = r._raster[::-1].diagonal(j-i)[i:]
                    
                    #use the flipped view
                    r_view = r._raster[::-1]
                    f_view = fetch[::-1]

                elif direction == 'SE':
                    s = r._raster.diagonal(j-i)[i:]
                
                elif direction == 'SW':
                    s = np.fliplr(r._raster).diagonal(j-i)[i:]
                    
                elif direction == 'NW':
                    s = r._raster.diagonal(j-i)[:i]
                
                idx = np.where( (s < r_view[i,j]+elev)==False)[0]
                if idx.size == 0: #no false found, so all true
                    f_view[i,j] = s.size * r.get_resolution()[0]   
                else:
                    f_view[i,j] = idx[0] * r.get_resolution()[0]   
           # self.window.progressBar.setValue(i)
            
        r._raster = fetch

        return r

    
    


 
 