import time
import sqlite3
from sqlite3 import Error
import Extension as ex
import pandas as pd
import itertools

class data_access:
    work = ()
    def __init__(self,norm_path=None,qlcl_path=None) -> None:
        self.norm_path = norm_path
        self.qlcl_path = qlcl_path
        self.connect_norm_db()

    def connect_qlcl_db(self):
        try:
            self.qlcl_conn = sqlite3.connect(self.qlcl_path if self.qlcl_path else 'qlcl.db')
            self.cur = self.qlcl_conn.cursor()
            self.create_qlcl_db()
        except Error:
            print(f'Error on {self.__class__.__name__}.connect_qlcl_db: ',Error)
            return 0
    
    def disconect(self):
        try:
            self.qlcl_conn.close()
            self.norm_conn.close()
            
            return 1
        except Error:
            print(f'Erroron {self.__class__.__name__}.disconect: ',Error)
            return 0           

    def close_qlcl_db(self):
        try:
            self.qlcl_conn.close()
            return 1
        except Error:
            print(f'Erroron {self.__class__.__name__}.close_qlcl_db: ',Error)
            return 0

        
    def connect_norm_db(self):
        try:
            self.norm_conn = sqlite3.connect(self.norm_path)
            self.cur = self.norm_conn.cursor()
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

    def create_qlcl_db(self):
        try:
            self.execute("""CREATE TABLE IF NOT EXISTS work (
                            id text PRIMARY KEY,
                            norm_id text,
                            name text,
                            unit text,
                            amount real,
                            start text,
                            end text,
                            FOREIGN KEY (norm_id) REFERENCES norm (id)
                        )""")

            return 1
        except Error:
            print(f'Error {self.__class__.__name__}.create_norm_db: ',Error)
            return 0     
    
def main():
    db = data_access('norm.db')
    db.connect_norm_db()
    
    db.close_norm_db()
    

if __name__ == "__main__":
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')
    