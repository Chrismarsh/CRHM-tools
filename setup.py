import matplotlib
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

sys.path.append(r"C:\Windows\winsxs\amd64_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_750b37ff97f4f68b")
sys.path.append("modules")

#mpl_files = matplotlib.get_py2exe_datafiles();
includefiles = [r'modules\aspect_ui.ui',
                r'modules\fetchr_ui.ui',
                r'modules\hist_ui.ui',
                r'modules\manual_class.ui',
                r'modules\slope_ui.ui']
includes = ['atexit',
            'PySide.QtXml',
	    'PySide.QtUiTools',
	    'matplotlib',
	    'matplotlib.backends.backend_tkagg',
	    'matplotlib.pyplot',
	    'scipy.sparse.csgraph._validation',
	    'modules.aspect',
	    'modules.fetchr',
	    'modules.hist',
	    'modules.manual_class',
	    'modules.slope']
excludes = []
packages = []

#path = sys.path + ["modules"]

setup(
    name = 'CRHM Tools',
    version = '0.0.3b"',
    description = 'CRHM Tools',
    author = 'Chris Marsh',
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}}, 
    executables = [Executable('main.py',base=base)]
)




#
#setup(
    #options = {
        #'py2exe': {
            #'includes':['PySide.QtXml',
            			#'PySide.QtUiTools',
            			#'matplotlib',
                		#'matplotlib.backends.backend_tkagg',
                		#'matplotlib.pyplot',
                		#'scipy.sparse.csgraph._validation',
                        #'modules'
                	#],
            #'dist_dir': 'dist',
        #}
    #},
    #data_files=matplotlib.get_py2exe_datafiles(),
    #windows=['main.py']
#)

