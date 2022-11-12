import time
import sqlite3
from sqlite3 import Error
import Extension as ex
import pandas as pd
import itertools

class data_access:
    def __init__(self,norm_path=None,work_path=None) -> None:
        self.norm_path = norm_path
        self.work_path = work_path
        self.connect_norm_db()
        
    def connect_norm_db(self):
        try:
            self.conn = sqlite3.connect(self.norm_path)
            self.cur = self.conn.cursor()
            self.create_norm_db()
        except Error:
            print(f'Error on {self.__class__.__name__}.connect_norm_db: ',Error)
            return 0
    
    def close_norm_db(self):
        try:
            self.conn.close()
            return 1
        except Error:
            print(f'Erroron {self.__class__.__name__}.close_norm_db: ',Error)
            return 0
        
    def execute(self,sql, parameter=None):
        try:
            self.cur.execute(sql) if not parameter else self.cur.execute(sql, parameter)
            self.conn.commit()
            return 1
        except Error:
            print(f'Erroron {self.__class__.__name__}.execute: ',Error)
            return 0
        
    def fetchall(self, sql, parameter=None):
        try:
            self.cur.execute(sql) if not parameter else self.cur.execute(sql, parameter)
            return self.cur.fetchall()
        except Error:
            print(f'Erroron {self.__class__.__name__}.execute: ',Error)
            return 0
        
    def create_norm_db(self):
        try:
            self.execute("""CREATE TABLE IF NOT EXISTS norm (
                            id text PRIMARY KEY,
                            name text,
                            unit text
                        )""")
            self.execute("""CREATE TABLE IF NOT EXISTS worker (
                        id text PRIMARY KEY,
                        name text,
                        unit text
                        )""")
            self.execute("""CREATE TABLE IF NOT EXISTS machine (
                            id text PRIMARY KEY,
                            name text,
                            unit text
                        )""")
            self.execute("""CREATE TABLE IF NOT EXISTS material (
                            id text PRIMARY KEY,
                            name text,
                            unit text
                        )""")
            self.execute("""CREATE TABLE IF NOT EXISTS worker_norm (
                            norm_id text,
                            id text,
                            amount real,
                            UNIQUE(norm_id, id),
                            FOREIGN KEY (id) REFERENCES worker (id),
                            FOREIGN KEY (norm_id) REFERENCES norm (id)                       
                        )""")
            self.execute("""CREATE TABLE IF NOT EXISTS machine_norm (
                            norm_id text,
                            id text,
                            amount real,
                            UNIQUE(norm_id, id),
                            FOREIGN KEY (id) REFERENCES machine (id),
                            FOREIGN KEY (norm_id) REFERENCES norm (id)                        
                        )""")
            self.execute("""CREATE TABLE IF NOT EXISTS material_norm (
                            norm_id text,
                            id text,
                            amount real,
                            UNIQUE(norm_id, id),
                            FOREIGN KEY (id) REFERENCES material (id),
                            FOREIGN KEY (norm_id) REFERENCES norm (id) 
                        )""")
            return 1
        except Error:
            print(f'Erroron {self.__class__.__name__}.create_norm_db: ',Error)
            return 0                    
    
    
def main():
    db = data_access('norm.db')
    db.connect_norm_db()
    
    db.close_norm_db()
    

if __name__ == "__main__":
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')
    