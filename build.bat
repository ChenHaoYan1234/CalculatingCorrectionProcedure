@echo off
pyinstaller .\\src\\Main.py -F -w -p .\\src\\MainWindow.py -p .\\src\\Values.py -p .\\src\\Tools.py -p .\\src\\ImageData.py --upx-dir .\\tools\\upx --distpath .\\dist
del .\\Main.spec
pyinstaller .\\src\\Upgrader.py -F -w --uac-admin -p .\\src\\Values.py --upx-dir .\\tools\\upx --distpath .\\dist
del .\\Upgrader.spec