# -*- coding: utf-8 -*-
import json
import sqlite3
from typing import Literal

from Values import STATUS


class ImageData():
    def __init__(self, db_path: str) -> None:
        self.connect = sqlite3.connect(db_path)
        self.cursor = self.connect.cursor()
        self.initDB()
        return

    def initDB(self) -> None:
        self.cursor.execute(
            "SELECT name FROM sqlite_master where type='table' order by name")
        table = self.cursor.fetchall()
        table = [line[0] for line in table]
        if not ("IMAGE" in table):
            self.cursor.execute(
                """
            CREATE TABLE IMAGE
            (
            IMAGE          BLOB  PRIMARY KEY  NOT NULL,
            RESULT         TEXT               NOT NULL
            );
            """
            )
            self.connect.commit()
            return

    def getResultFromImage(self, img: bytes) -> dict | Literal[STATUS.NOTFOUND]:
        data = self.cursor.execute(
            "SELECT image, result  from IMAGE")
        for image, result in data:
            if image == img:

                return json.loads(result)
        return STATUS.NOTFOUND

    def newResult(self, img: bytes, result: dict) -> None:
        result_ = json.dumps(result)
        self.cursor.execute(
            "INSERT INTO IMAGE (IMAGE,RESULT) VALUES (?, '"+result_+"')", (img,))
        self.connect.commit()
        return

    def close(self) -> None:
        self.connect.close()
        return
