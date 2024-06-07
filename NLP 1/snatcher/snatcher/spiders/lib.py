import sqlite3
import os

#"Библиотека" для вынесения общих методов

class DB_link:
    
    def __init__(self, name) -> None:
        self.name = name

    def InitDir(self):
        if(not os.path.exists("db")):
            os.mkdir("db")

    def InitDB(self):
        connection = sqlite3.connect(f'db/{self.name}.db')
        cursor = connection.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.name} (
                            title TEXT, content TEXT, category TEXT, created_date TEXT
                            )''')
        connection.commit()
        cursor.close()

    def AddToDB(self, instanse):
        connection = sqlite3.connect(f'db/{self.name}.db')
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {self.name} VALUES (?,?,?,?)",
                        instanse)
        connection.commit()
        connection.close()