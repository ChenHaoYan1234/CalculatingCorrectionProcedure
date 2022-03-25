del .\\Main.spec
pyinstaller .\\src\\Main.py -F -w -p .\\src\\MainWindow.py -p .\\src\\MainWindow_rc.py -p .\\src\\Tools.py -p .\\src\\ImageData.py --distpath .\\dist