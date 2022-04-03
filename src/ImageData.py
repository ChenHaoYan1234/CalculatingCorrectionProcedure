import sqlite3
import json


class ImageData():
    def __init__(self, db_path: str) -> None:
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()
        self.initDB()

    def initDB(self) -> None:
        self.cursor.execute(
            "SELECT name FROM sqlite_master where type='table' order by name")
        table = self.cursor.fetchall()
        table = [line[0] for line in table]
        if not ("IMAGE" in table):
            self.cursor.execute(
                '''
            CREATE TABLE IMAGE
            (
            IMAGE          BLOB  PRIMARY KEY  NOT NULL,
            RESULT         TEXT               NOT NULL
            );
            '''
            )
            self.connect.commit()

    def getResultFromImage(self, img: bytes) -> dict:
        data = self.cursor.execute(
            "SELECT image, result  from IMAGE")
        for image, result in data:
            if image == img:
                return json.loads(result)
        return None

    def newResult(self, img: bytes, result: dict) -> None:
        result_ = json.dumps(result)
        self.cursor.execute(
            "INSERT INTO IMAGE (IMAGE,RESULT) VALUES (?, '"+result_+"')", (img,))
        self.connect.commit()

    def close(self) -> None:
        self.connect.close()
