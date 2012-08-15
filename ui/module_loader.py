import imp
import os
import inspect
import sys

#Handles loading of the dynamic modules
class module_loader(object):
    def __init__(self):

        self.modules = {}

    def load(self,path,imported_files):

        files = os.listdir(path)	
        for f in files:
            name,ext = os.path.splitext(os.path.split(f)[-1])

            if ext.lower() == '.py':
                py_mod = imp.load_source(name,os.path.join(path,name+ext))
            #elif ext.lower() == '.pyc':
                #py_mod = imp.load_compiled(name,os.path.join(path,name+ext))

                #for the moment, assume ONE class per file
                for name,obj in inspect.getmembers(py_mod,inspect.isclass):
                    if 'mod_' in name:
                        #instaniate this 
                        mod = eval('py_mod.'+name+'(imported_files)')
                        self.modules[mod.name] = mod

        return self.modules 	