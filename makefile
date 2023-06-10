include config.txt

build:
	pyinstaller ./src/Main.py -F -w -p ./src/MainWindow.py -p ./src/Values.py -p ./src/Tools.py -p ./src/ImageData.py --distpath ./dist --upx-dir ${UPX}
	pyinstaller ./src/Updater.py -F -w --uac-admin -p ./src/Values.py --distpath ./dist --upx-dir ${UPX}

clean:
	${DEL} Main.spec
	${DEL} dist\Main.exe
	${DEL} Updater.spec
	${DEL} dist\Updater.exe
	${DEL} build\Main\*.*
	${DEL} build\Main\localpycs\*.*
	${RMDIR} build\Main\localpycs
	${RMDIR} build\Main
	${DEL} build\Updater\*.*
	${DEL} build\Updater\localpycs\*.*
	${RMDIR} build\Updater\localpycs
	${RMDIR} build\Updater
	${RMDIR} build

rebuild:
	make -r clean
	make -r build