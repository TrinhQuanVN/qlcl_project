import time
import pandas as pd
from docxtpl import DocxTemplate
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

def get_templates(folder_template_path):
    result = {}
    docx_path = Path(folder_template_path) # Folder chứa docx: NKTC, NKEC
    for docx in docx_path.glob('*.docx'):
        if docx.is_file(): # kiểm tra nếu là file thì add vào docxs
            result.update({docx.stem:docx})
    return result

def render(path_template, context, output_path):
    # try:
        doc = DocxTemplate(path_template)
        doc.render(context)
        doc.save(output_path)
    # except:
    #     print('Error on render')

def rain(prpc:float):
    if  0 < prpc <6:
        return 'mưa nhỏ'
    if 6 <= prpc <= 15:
        return 'mưa'
    if 16 < prpc <= 50:
        return 'mưa vừa'
    if 50 < prpc <= 100:
        return 'mưa to' 
    if prpc > 100:
        return 'mưa rất to' 
    else:
        return 'không mưa'   
def get_data_weather(location:Point, tmin:datetime, tmax:datetime):
    data = Daily(location, tmin, tmax)
    return data.fetch()

def main():
    # df = pd.DataFrame([(1,2,3),(4,5,6)],columns=list('abc'))
    # items = df.to_dict(orient='records')
    # doc =DocxTemplate('test.docx')
    # doc.render({'items':items})
    # doc.save('rendered.docx')
    path = 'qlcl_imput_test.xlsx'
    dfs = pd.read_excel(path, sheet_name=['info','lmtn','ntcv','ntvl','nktc'], header=0)
    
    info = dfs['info'].set_index('key').to_dict()['value']
    # print(type(info))
    # # dfs['lmtn']['info'] = [info * ]
    # print(dfs['lmtn'].to_dict(orient='records'))
    # # print(info * 51)
    
    
    
    dict_template = get_templates(r'D:\Travail\QLCL\Template')
    # items = dfs['lmtn'].to_dict(orient='records')
    # for item in items:
    #     item.update({'info':info})
    
    # render(dict_template['lmtn'], {'items':items}, 'lmtn.docx')
    
    # items = dfs['ntvl'].to_dict(orient='records')
    # for item in items:
    #     item.update({'info':info})
    
    # render(dict_template['ntvl'], {'items':items}, 'ntvl.docx')

    # items = dfs['ntcv'].to_dict(orient='records')
    # for item in items:
    #     item.update({'info':info})
    
    # render(dict_template['ntcv'], {'items':items}, 'ntcv.docx')
    
    data = Daily(Point(21.025821, 105.856541, 70), min(dfs['nktc'].day), max(dfs['nktc'].day))
    weather = data.fetch()
    dfs['nktc'].set_index('day',inplace=True,drop=False)
    dfs['nktc'].fillna('',inplace=True)
    dfs['nktc']['weather'] = weather.tmax.map(lambda x: u'Nhiệt độ trung bình: {}\N{DEGREE SIGN}C, '.format(int(round(x,0)))) + weather.prcp.map(rain)
    items = dfs['nktc'].to_dict(orient='records')
    for item in items:
        item.update({'info':info})
        
    render(dict_template['nktc'], {'items':items}, 'nktc.docx')

if __name__ == '__main__':
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')