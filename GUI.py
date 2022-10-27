import Elements
import PySimpleGUI as sg
from Elements import Text

def Combo(values=[],s=(20,1),k='',default_value=None,enable_event=True,font=('Any',11),expand_x=True):
    return sg.Combo(values=values,s=s,k=k,default_value=default_value,enable_events=enable_event,font=font,expand_x=expand_x)

def I(s=(10,1),k='',default_text='',readonly=False,text_color=None,justification='l',font=('Any',11)):
    return sg.Input(s=s,k=k,default_text=default_text,readonly=readonly,text_color=text_color,justification=justification,font=font)

def T(text='',k='',s=(5,1),justification='r',font=('Any',11)):
    return sg.Text(text=text,s=s, justification=justification, font=font)


right_click_menu_def = [[], ['Quan', 'Yeu', 'Hang','More Nothing','Exit']]
right_click_menu_tab_norm = [[], ['Create a copy', 'Edit', 'Delete', 'More']]
right_click_menu_tab_work = [[], ['Create a copy', 'Edit', 'Delete', 'Add LMTN', 'Add NTVL']]

GRAPH_SIZE = (640,480)
def menu_layout():
    menu_def = [['Công trình', ['Save','Open','Exit']],
                ['Định mức', ['Lưu định mức','Mở định mức','Thêm từ dự toán',]]]
    
    menu_layout =  [sg.MenubarCustom(menu_def, key='-MENU-', font='Courier 13')]
    return menu_layout

def tab_machine_layout():
    layout = [
        [Text('Find',(5,1)).GUI,sg.Input(s=(20,1),k='-MACHINE SEARCH INPUT-'),sg.Text(s=(5,1),k='-MACHINE COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-MACHINE FIND BUTTON-')],
        [sg.Table(values=[],headings=['id','name','unit','amount'],k='-TABLE MACHINE-',col_widths=[6,35,6],auto_size_columns=False,justification='l')],
        [sg.Push(),sg.Button('Add',s=(10,1),k='-ADD MACHINE-'),sg.Button('Edit',s=(10,1),k='-EDIT MACHINE-'),sg.Button('Delete',s=(10,1),k='-DELETE MACHINE-')]
    ]
    return layout

def tab_material_layout():
    layout = [
        [Text('Find',(5,1)).GUI,sg.Input(s=(20,1),k='-MATERIAL SEARCH INPUT-'),sg.Text(s=(5,1),k='-MATERIAL COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-MATERIAL FIND BUTTON-')],
        [sg.Table(values=[],headings=['id','name','unit','amount'],k='-TABLE MATERIAL-',col_widths=[6,35,6],auto_size_columns=False,justification='l')],
        [sg.Push(),sg.Button('Add',s=(10,1),k='-ADD MATERIAL-'),sg.Button('Edit',s=(10,1),k='-EDIT MATERIAL-'),sg.Button('Delete',s=(10,1),k='-DELETE MATERIAL-')]
    ]
    return layout

def tab_worker_layout():
    layout = [
        [Text('Find',(5,1)).GUI,sg.Input(s=(20,1),k='-WORKER SEARCH INPUT-'),sg.Text(s=(5,1),k='-WORKER COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-WORKER FIND BUTTON-')],
        [sg.Table(values=[],headings=['id','name','unit','amount'],k='-TABLE WORKER-',col_widths=[6,35,6],auto_size_columns=False,justification='l')],
        [sg.Push(),sg.Button('Add',s=(10,1),k='-ADD WORKER-'),sg.Button('Edit',s=(10,1),k='-EDIT WORKER-'),sg.Button('Delete',s=(10,1),k='-DELETE WORKER-')]
    ]
    return layout

def tab_norm_layout():
    layout = [
        [sg.Text('Find',s=(5,1)), 
        sg.Input(s=(20,1),k='-NORM SEARCH INPUT-'), 
        sg.Text(s=(5,1),k='-NORM COUNT TEXT-'), 
        sg.Button('Find',s=(10,1),k='-NORM FIND BUTTON-'), 
        sg.Input(k='-SELECTED NORM INPUT-',visible=False)],
        
        [sg.Tree(data=sg.TreeData(), 
                 headings=['ID','UNIT','amount'], 
                 k='-TREE NORM-',col0_heading='NORM',
                 col0_width=50,col_widths=[6,6,6],
                 auto_size_columns=False,
                 enable_events=True,
                 right_click_menu= right_click_menu_tab_norm,
                 select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        
        [sg.Push(), 
         sg.Button('Add work',s=(10,1),k='-ADD WORK WITH NORM ID-'),
         sg.Button('Add',s=(10,1),k='-ADD NORM-'),
         sg.Button('Edit',s=(10,1),k='-EDIT NORM-'),
         sg.Button('Create a copy',s=(15,1),k='-CREATE COPY NORM-'),
         sg.Button('Delete',s=(10,1),k='-DELETE NORM-')]
    ]
    return layout

def tab_work_layout():
    layout = [
        [sg.Text('Find',s=(5,1)),
         sg.Input(s=(20,1),k='-WORK SEARCH INPUT-'),
         sg.Text(s=(5,1),k='-WORK COUNT TEXT-'),
         sg.Button('Find',s=(10,1),k='-WORK FIND BUTTON-'),
         sg.Input(k='-SELECTED WORK INPUT-',visible=True)],
        
        [sg.Tree(data=sg.TreeData(),
                 headings=['ID','Unit','Amount','Days','Start','End'],
                 k='-TREE WORK-',
                 col0_heading='WORK',
                 col0_width=50,
                 col_widths=[6,6,6],
                 auto_size_columns=False,
                 right_click_menu= right_click_menu_tab_work,
                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                 enable_events=True)],
        
        [sg.Push(),
         sg.Button('Đồ thị',s=(10,1),k='-SHOW GRAPH-'),
         sg.Button('Add HM',s=(10,1),k='-ADD HM-'),
         sg.Button('Add',s=(10,1),k='-ADD WORK-'),
         sg.Button('Edit',s=(10,1),k='-EDIT WORK-'),
         sg.Button('Create a copy',s=(15,1),k='-CREATE COPY WORK-'),
         sg.Button('Delete',s=(10,1),k='-DELETE WORK-')]
    ]
    return layout

def tab_lmtn_layout():
    layout = [
        [sg.Text('Find',s=(5,1)),
         sg.Input(s=(20,1),k='-LMTN SEARCH INPUT-'),
         sg.Text(s=(5,1),k='-LMTN COUNT TEXT-'),
         sg.Button('Find',s=(10,1),k='-LMTN FIND BUTTON-')],
        
        [sg.Tree(data=sg.TreeData(),
                 headings=['DateNT','DateYC','Name','SLTM','SLM','KTM','YC'],
                 k='-TREE LMTN-',
                 col0_heading='ID',
                 col0_width=6,
                 col_widths=[6,6,30,6,6,6,6],
                 auto_size_columns=False,
                 enable_events=True)],
        
        [sg.Push(),
         
        #  sg.Button('Add HM',s=(10,1),k='-ADD HM-'),
         sg.Button('Add',s=(10,1),k='-ADD LMTN-'),
         sg.Button('Edit',s=(10,1),k='-EDIT LMTN-'),
         sg.Button('Create a copy',s=(15,1),k='-CREATE COPY LMTN-'),
         sg.Button('Delete',s=(10,1),k='-DELETE LMTN-')]
    ]
    return layout

def tab_ntvl_layout():
    layout = [
        [sg.Text('Find',s=(5,1)),
         sg.Input(s=(20,1),k='-NTVL SEARCH INPUT-'),
         sg.Text(s=(5,1),k='-NTVL COUNT TEXT-'),
         sg.Button('Find',s=(10,1),k='-NTVL FIND BUTTON-')],
        
        [sg.Tree(data=sg.TreeData(),
                 headings=['Date YC','NTVL'],
                 k='-TREE NTVL-',
                 col0_heading='Date NT',
                 col0_width=10,
                 col_widths=[10,20],
                 auto_size_columns=False,
                 enable_events=True)],
        
        [sg.Push(),
        #  sg.Button('Add HM',s=(10,1),k='-ADD HM-'),
         sg.Button('Add',s=(10,1),k='-ADD NTVL-'),
         sg.Button('Edit',s=(10,1),k='-EDIT NTVL-'),
         sg.Button('Create a copy',s=(15,1),k='-CREATE COPY NTVL-'),
         sg.Button('Delete',s=(10,1),k='-DELETE NTVL-')]
    ]
    return layout

def tab_ntcv_layout():
    layout = [
        [sg.Text('Find',s=(5,1)),
         sg.Input(s=(20,1),k='-NTCV SEARCH INPUT-'),
         sg.Text(s=(5,1),k='-NTCV COUNT TEXT-'),
         sg.Button('Find',s=(10,1),k='-NTCV FIND BUTTON-')],
        
        [sg.Tree(data=sg.TreeData(),
                 headings=['DateNT','DateYC','Name'],
                 k='-TREE NTCV-',
                 col0_heading='ID',
                 col0_width=2,
                 col_widths=[4,4,50],
                 auto_size_columns=False,
                 justification='c',
                 enable_events=True)],
        
        [sg.Push(),
        #  sg.Button('Add HM',s=(10,1),k='-ADD NTCV-'),
         sg.Button('Add',s=(10,1),k='-ADD NTCV-'),
         sg.Button('Edit',s=(10,1),k='-EDIT NTCV-'),
         sg.Button('Create a copy',s=(15,1),k='-CREATE COPY NTCV-'),
         sg.Button('Delete',s=(10,1),k='-DELETE NTCV-')]
    ]
    return layout

def tab_nktc_layout():
    layout = [
        [sg.Text('Find',s=(5,1)),
         sg.Input(s=(20,1),k='-NKTC SEARCH INPUT-'),
         sg.Text(s=(5,1),k='-NKTC COUNT TEXT-'),
         sg.Button('Find',s=(10,1),k='-NKTC FIND BUTTON-')],
        
        [sg.Tree(data=sg.TreeData(),
                 headings=['NKTC'],
                 k='-TREE NKTC-',
                 col0_heading='Date',
                 col0_width=20,
                 col_widths=[],
                 auto_size_columns=False,
                 enable_events=True)],
        
        [sg.Push(),
        #  sg.Button('Add HM',s=(10,1),k='-ADD HM-'),
         sg.Button('Add',s=(10,1),k='-ADD NKTC-'),
         sg.Button('Edit',s=(10,1),k='-EDIT NKTC-'),
         sg.Button('Create a copy',s=(15,1),k='-CREATE COPY NKTC-'),
         sg.Button('Delete',s=(10,1),k='-DELETE NKTC-')]
    ]
    return layout

def main_layout():
    layout = [
        menu_layout(),
        
        [sg.TabGroup([
            # [sg.Tab('Worker',tab_worker_layout(),k='-WORKER TAB-')],
            # [sg.Tab('Machine',tab_machine_layout(),k='-MACHINE TAB-')],
            # [sg.Tab('Material',tab_material_layout(),k='-MATERIAL TAB-')],
            [sg.Tab('Norm',tab_norm_layout(),k='-NORM TAB-')],
            [sg.Tab('Work',tab_work_layout(),k='-WORK TAB-')],
            [sg.Tab('NTCV',tab_ntcv_layout(),k='-NTCV TAB-')],
            [sg.Tab('LMTN',tab_lmtn_layout(),k='-LMTN TAB-')],
            [sg.Tab('NKTC',tab_nktc_layout(),k='-NKTC TAB-')],
            [sg.Tab('NTVL',tab_ntvl_layout(),k='-NTVL TAB-')],
            # [sg.Tab('NTCV',tab_ntcv_layout(),k='-NTCV TAB-')],
            
            ],k='-TAB GROUP-',enable_events=True)],
        
        [sg.Sizegrip(k='-CHANGE WINDOW SIZE-')]
    ]
    
    return layout

def GUI():
    sg.theme('DarkAmber')
    
    window = sg.Window('Main',
                layout=main_layout(),
                right_click_menu=right_click_menu_def,grab_anywhere=True,
                resizable=True,finalize=True,  
                # location=(300,300),
                margins=(0, 0)
    )
    
    # window['-TABLE MACHINE-'].expand(True,True)
    # window['-TABLE MATERIAL-'].expand(True,True)
    # window['-TABLE WORKER-'].expand(True,True)
    window['-TREE NORM-'].expand(True,True)
    window['-TREE WORK-'].expand(True,True)
    window['-TREE NKTC-'].expand(True,True)
    window['-TREE LMTN-'].expand(True,True)
    window['-TREE NTVL-'].expand(True,True)
    window['-TREE NTCV-'].expand(True,True)
    
    
    
    window['-TAB GROUP-'].expand(True,True)
    
    window['-NORM SEARCH INPUT-'].bind('<Return>', '_Enter')
    window['-WORK SEARCH INPUT-'].bind('<Return>', '_Enter')
    
    window.set_min_size((800,600))
    
    #------------------------------------WINDOW BIND------------------------------------
    # window[InputDinhMucTim.key].bind("<Return>", "_Enter")
    # window[InputCongTacKhoiLuong.key].bind("<Return>", "_Enter") 
    # window[InputCongTrinhEnd.key].bind("<Return>", "_Enter")
    window.bind('<F1>','-F1-')
    window.bind('<F2>','-F2-')
    window.bind('<F3>','-F3-')
    return window