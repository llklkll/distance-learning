import sqlite3


class UsersModel:
    def __init__(self, connection):
        self.connection = connection
        
    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS userss 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name VARCHAR(60),
                          groupe VARCHAR(2),
                          user_name VARCHAR(50),
                          password_hash VARCHAR(128),
                          teacher VARCHAR(60),
                          role VARCHAR(7),
                          im VARCHAR(30)
                          )''')
        cursor.close()
        self.connection.commit()
    
    def insert(self, name, groupe, user_name, password_hash, teacher, role, im):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO userss 
                          (name, groupe, user_name, password_hash, teacher, role, im) 
                          VALUES (?,?,?,?,?,?,?)''', (name, groupe, user_name, password_hash, teacher, role, im))
        cursor.close()
        self.connection.commit() 
        
    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM userss WHERE user_name = ?", (user_name,))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)   
    
        
    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM userss WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row
    
    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM userss")
        rows = cursor.fetchall()
        return rows
    
    def delete(self, pupil_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM userss WHERE id = ?''', (str(pupil_id),))
        cursor.close()
        self.connection.commit()
