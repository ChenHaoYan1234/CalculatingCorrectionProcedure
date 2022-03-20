import sqlite3

class ImageData():
    def __init__(self,db_path:str) -> None:
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()

    def getResultFromImage(self,img:bytes) -> dict:
        pass

    def newResult(self,img:bytes,result:dict) -> None:
        pass

    def close(self) -> None:
        self.connect.close()