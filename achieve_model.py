import sqlite3
import datetime


class AchieveModel:
    
    def __init__(self, connection):
        self.connection = connection
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS achieve 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER,
                             time VARCHAR(10),
                             im VARCHAR(30)
                             )''')
        cursor.close()
        self.connection.commit()
        
    def insert(self, title, content, user_id, im):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO achieve 
                          (title, content, user_id, time, im) 
                          VALUES (?,?,?,?,?)''', (title, content, str(user_id), str(datetime.date.today()), im))
        cursor.close()
        self.connection.commit()
    
    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM achieve WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row
    
    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM achieve WHERE user_id = ?", (str(user_id),))
        else:
            cursor.execute("SELECT * FROM achieve")
        rows = cursor.fetchall()
        return rows 
        
    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM achieve WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()    