import time
from data_access import data_access
from sqlite3 import Error

class repository:
    def __init__(self, data_base: data_access) -> None:
        self.db = data_base
        self.db.connect_norm_db()
        
    def insert_norm(self, norm):
        try:
            self.db.execute('INSERT OR IGNORE INTO norm VALUES(?,?,?)',norm)
        except:
            print(f'Error on {self.__class__.__name__}.insert_norm: ',Error)
            return 0
        



def main():
    db = data_access('norm.db')
    repo = repository(db)
    repo.insert_norm(('QQ.11111','Trịnh Tiến Quân','GOD'))
    
    db.close_norm_db()
    
    

if __name__ == "__main__":
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')        