from distutils.core import setup
import py2exe
import sys
import matplotlib


sys.path.append(r"C:\Windows\winsxs\amd64_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_750b37ff97f4f68b")

setup(
    options = {
        'py2exe': {
            'includes': ['PySide.QtXml','PySide.QtUiTools'],
            'dist_dir': 'dist',
        }
    },
    data_files=matplotlib.get_py2exe_datafiles(),
    windows=['main.py']
)


