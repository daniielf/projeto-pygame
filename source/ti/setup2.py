import sys
from cx_Freeze import setup,Executable

includefiles = ["media"]

#includes = ["game.py","avalgame.py","constants.py","gameSettings.py","log.py","objects.py","text_input.py"]
packages = ["pygame","pygaze","numpy"]
excludes = []
includes = []

base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(name="KidConsumer",
         version='1.0.0',
         description="test",
         options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
         executables=[Executable("menu.py", base=base)])