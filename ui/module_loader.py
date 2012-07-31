import imp
import os
import inspect
import sys

class module_loader():
    def __init__(self):
        
	self.modules = {}
    def load(self,path):

	files = os.listdir(path)	
	for f in files:
		    name,ext = os.path.splitext(os.path.split(f)[-1])
		    
		    if ext.lower() == '.py':
			py_mod = imp.load_source(name,os.path.join(path,name+ext))
		    elif ext.lower() == '.pyc':
			py_mod = imp.load_compiled(name,os.path.join(path,name+ext))
		    
		    #for the moment, assume ONE class per file
		    for name,obj in inspect.getmembers(py_mod,inspect.isclass):
			#instaniate this 
			self.modules[name] = eval('py_mod.'+name+'()')
		    
	return self.modules 	