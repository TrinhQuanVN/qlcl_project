import PySimpleGUI as sg
import sqlite3
import pandas as pd

conn = sqlite3.connect('test_search_text.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS work (
                            name text,
                            start datetime,
                            end datetime
                        )""")

layout = [
    [sg.Input(k='search input'), sg.Button('Search',k='search button'),],
    [sg.Table([],['name','start','end'],k='table',col_widths=[70,15,15],expand_x=True, expand_y=True,auto_size_columns=False)],
    [sg.Push(), sg.FileBrowse(k='browse button'), sg.Button('Load')]
]
window = sg.Window('SEARCH TEXT', layout, finalize=True,resizable=True)
window['search input'].bind('<Return>', ' enter')

table = window['table']

def get_work_from_db(text:str=None):
    if not text:
        cur.execute('select * from work')
        return cur.fetchall()
    cur.execute('select * from work where lower(name) like ?', ('%'+ text.lower()+'%',))
    return cur.fetchall()

def show(fetchall):
    table.update(fetchall)
    
def import_to_db(path):
    df = pd.read_excel(path,sheet_name='Sheet1',header=0,index_col=0)
    print(df)
    df.to_sql(name='work',con=conn,if_exists='replace')

def main():
    while True:
        event, values = window.read()
        print(event,'\n',values)
        if event in [sg.WIN_CLOSED]:
            break
        if event == 'Load':
            path = values['browse button']
            if path:
                print('haha')
                import_to_db(path)
                show(get_work_from_db())
        if event in ['search button', 'search input enter']:
            text = values['search input']
            show(get_work_from_db(text))
            
        
    conn.close()

if __name__ == "__main__":
    main()