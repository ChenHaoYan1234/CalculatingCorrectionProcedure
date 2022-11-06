all:
	pyinstaller ./src/Main.py -F -w -p ./src/MainWindow.py -p ./src/Values.py -p ./src/Tools.py -p ./src/ImageData.py --distpath ./dist --upx-dir ./tools/upx
	pyinstaller ./src/Updater.py -F -w --uac-admin -p ./src/Values.py --distpath ./dist --upx-dir ./tools/upx