import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["pygame", "random", "tkinter"],
                     "excludes": ["numpy", "pytz", "asyncio", "concurrent", "ctypes", "distutils", "email", "html",
                                  "http", "json", "logging", "multiprocessing", "neat", "pkg_resources", "pydoc_data",
                                  "test", "unittest", "urllib", "xmlrpc"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Snake",
    options={"build_exe": build_exe_options},
    version="4.0",
    description='my first game -- 4.0',
    executables=[Executable("Snake.py", base=base, icon='data/snake.ico')]
)




