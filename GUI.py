import Elements
import PySimpleGUI as sg
from Elements import Text
from enum import Enum

from Models import norm

class KeyGUI(Enum):
    norm_search_input = '-norm search input-'
    norm_count_text = '-norm count input-'
    norm_find_button = '-norm find button-'
    norm_selected_input = '-selected norm id input-'
    norm_tree = '-norm tree-'
    norm_id_create_work = '-create work with norm id-'
    norm_create = '-norm create button-'
    norm_edit = '-norm edit button-'
    norm_copy = '-norm copy button-'
    norm_delete = '-norm delete button-'

    work_search_input = '-work search input-'
    work_count_text = '-work count input-'
    work_find_button = '-work find button-'
    work_selected_input = '-selected work id input-'
    work_tree = '-work tree-'
    work_create = '-work create button-'
    work_edit = '-work edit button-'
    work_copy = '-work copy button-'
    work_delete = '-work delete button-'
    work_visualization = '-work visualization button-'
    
    hang_muc_create = '-hang muc create button-'
    phan_viec_create = '-phan viec create button-'    
        
    lmtn_search_input = '-lmtn search input-'
    lmtn_count_text = '-lmtn count input-'
    lmtn_find_button = '-lmtn find button-'
    lmtn_selected_input = '-selected lmtn id input-'
    lmtn_tree = '-lmtn tree-'
    lmtn_create = '-lmtn create button-'
    lmtn_edit = '-lmtn edit button-'
    lmtn_copy = '-lmtn copy button-'
    lmtn_delete = '-lmtn delete button-'        

    ntvl_search_input = '-ntvl search input-'
    ntvl_count_text = '-ntvl count input-'
    ntvl_find_button = '-ntvl find button-'
    ntvl_selected_input = '-selected ntvl id input-'
    ntvl_tree = '-ntvl tree-'
    ntvl_create = '-ntvl create button-'
    ntvl_edit = '-ntvl edit button-'
    ntvl_copy = '-ntvl copy button-'
    ntvl_delete = '-ntvl delete button-'
 
    ntcv_search_input = '-ntcv search input-'
    ntcv_count_text = '-ntcv count input-'
    ntcv_find_button = '-ntcv find button-'
    ntcv_selected_input = '-selected ntcv id input-'
    ntcv_tree = '-ntcv tree-'
    ntcv_create = '-ntcv create button-'
    ntcv_edit = '-ntcv edit button-'
    ntcv_copy = '-ntcv copy button-'
    ntcv_delete = '-ntcv delete button-'       

    nktc_search_input = '-nktc search input-'
    nktc_count_text = '-nktc count input-'
    nktc_find_button = '-nktc find button-'
    nktc_selected_input = '-selected nktc id input-'
    nktc_tree = '-nktc tree-'
    nktc_create = '-nktc create button-'
    nktc_edit = '-nktc edit button-'
    nktc_copy = '-nktc copy button-'
    nktc_delete = '-nktc delete button-'
    
    norm_tab = '-norm tab-'
    work_tab = '-work tab-'
    lmtn_tab = '-lmtn tab-'
    ntvl_tab = '-ntvl tab-'
    ntcv_tab = '-ntcv tab-'
    nktc_tab = '-nktc tab-'
    group_tab = '-group tab-'
    
class layout(Enum):
    WINDOWN_SIZE = (640,480)
    button_size10 = (10,1)
    text_size10 = (10,1)
    input_size20 = (20,1)
    input_size40 = (40,1)
    font13 = ('Courier',13)
    font11 = ('Courier',11)
    font9 = ('Courier',9)
    
    right_click_menu_def = [[], ['Quan', 'Yeu', 'Hang','More Nothing','Exit']]
    right_click_menu_tab_norm = [[], ['Create work','Create a copy', 'Edit', 'Delete', 'More']]
    right_click_menu_tab_work = [[], ['Create a copy', 'Edit', 'Delete', 'Add LMTN', 'Add NTVL']]
    
    menu_def = [['Công trình', ['Save','Open','Exit']],
            ['Định mức', ['Lưu định mức','Mở định mức','Thêm từ dự toán',]]]
    
    menubar_main_element = [sg.MenubarCustom(menu_def, font=font13)]  
     
    norm_tree_element = [sg.Tree(data=sg.TreeData(), 
                        headings=['ID','UNIT','amount'], 
                        k=KeyGUI.norm_tree.value, col0_heading='NORM',
                        col0_width=50, col_widths=[6,6,6],
                        auto_size_columns=False, enable_events=True,
                        right_click_menu= right_click_menu_tab_norm,
                        expand_x=True, expand_y= True,
                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED)]
    
    work_tree_element = [sg.Tree(data=sg.TreeData(),
                        headings=['ID','Unit','Amount','Days','Start','End'],
                        k= KeyGUI.work_tree.value,
                        col0_heading='WORK',
                        col0_width=50,
                        col_widths=[6,6,6],
                        auto_size_columns=False,
                        right_click_menu= right_click_menu_tab_work,
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True, expand_y= True,
                        enable_events=True)]    

    lmtn_tree_element = [sg.Tree(data=sg.TreeData(),
                        headings=['DateNT','DateYC','Name','SLTM','SLM','KTM','YC'],
                        k= KeyGUI.lmtn_tree.value,
                        col0_heading='ID',
                        col0_width= 6,
                        col_widths= [6,6,30,6,6,6,6],
                        auto_size_columns=False,
                        justification='l',
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True, expand_y= True,
                        enable_events=True)]
    
    ntvl_tree_element = [sg.Tree(data=sg.TreeData(),
                        headings=['DateNT','DateYC','Name'],
                        k= KeyGUI.ntvl_tree.value,
                        col0_heading='ID',
                        col0_width=2,
                        col_widths=[4,4,50],
                        auto_size_columns=False,
                        justification='l',
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True, expand_y= True,
                        enable_events=True)]

    ntcv_tree_element = [sg.Tree(data=sg.TreeData(),
                        headings=['DateNT','DateYC','Name'],
                        k= KeyGUI.ntcv_tree.value,
                        col0_heading='ID',
                        col0_width=2,
                        col_widths=[4,4,50],
                        auto_size_columns=False,
                        justification='l',
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True, expand_y= True,
                        enable_events=True)]

    nktc_tree_element = [sg.Tree(data=sg.TreeData(),
                        headings=['DateNT','DateYC','Name'],
                        k= KeyGUI.nktc_tree.value,
                        col0_heading='ID',
                        col0_width=2,
                        col_widths=[4,4,50],
                        auto_size_columns=False,
                        justification='l',
                        select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True, expand_y= True,
                        enable_events=True)]
   
    norm_tab_layout = [
                    [sg.Text('Find',s=text_size10), 
                    sg.Input(s= input_size20,k=KeyGUI.norm_search_input.value), 
                    sg.Text(s= text_size10,k= KeyGUI.norm_count_text.value), 
                    sg.Button('Find',s= button_size10,k=KeyGUI.norm_find_button.value), 
                    sg.Input(k= KeyGUI.norm_selected_input.value,visible=True)],
                    
                    norm_tree_element,
                    
                    [sg.Push(), 
                    sg.Button('Create work',s= button_size10,k= KeyGUI.norm_id_create_work.value),
                    sg.Button('Create',s= button_size10,k= KeyGUI.norm_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.norm_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.norm_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.norm_delete.value)]
                    ]
    
    work_tab_layout = [
                    [sg.Text('Find',s= text_size10), 
                    sg.Input(s= input_size20,k=KeyGUI.work_search_input.value), 
                    sg.Text(s= text_size10,k= KeyGUI.work_count_text.value), 
                    sg.Button('Find',s= button_size10,k=KeyGUI.work_search_input.value), 
                    sg.Input(k = KeyGUI.work_selected_input.value,visible=False)],
                    
                    work_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Đồ thị',s=button_size10, k= KeyGUI.work_visualization.value),
                    sg.Button('Create HM',s=button_size10, k= KeyGUI.hang_muc_create.value),
                    sg.Button('Create PV',s=button_size10, k= KeyGUI.phan_viec_create.value),
                    sg.Button('Create',s= button_size10,k= KeyGUI.work_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.work_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.work_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.work_delete.value)]
                    ]

    lmtn_tab_layout = [
                    [sg.Text('Find',s= text_size10), 
                    sg.Input(s= input_size20,k=KeyGUI.lmtn_search_input.value), 
                    sg.Text(s= text_size10,k= KeyGUI.lmtn_count_text.value), 
                    sg.Button('Find',s= button_size10,k=KeyGUI.lmtn_search_input.value), 
                    sg.Input(k = KeyGUI.lmtn_selected_input.value,visible=False)],
                    
                    lmtn_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.lmtn_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.lmtn_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.lmtn_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.lmtn_delete.value)]
                    ]

    ntvl_tab_layout = [
                    [sg.Text('Find',s= text_size10), 
                    sg.Input(s= input_size20,k=KeyGUI.ntvl_search_input.value), 
                    sg.Text(s= text_size10,k= KeyGUI.ntvl_count_text.value), 
                    sg.Button('Find',s= button_size10,k=KeyGUI.ntvl_search_input.value), 
                    sg.Input(k= KeyGUI.ntvl_selected_input.value,visible=False)],
                    
                    ntvl_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.ntvl_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.ntvl_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.ntvl_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.ntvl_delete.value)]
                    ]
    
    ntcv_tab_layout = [
                    [sg.Text('Find',s= text_size10), 
                    sg.Input(s= input_size20,k=KeyGUI.ntcv_search_input.value), 
                    sg.Text(s= text_size10,k= KeyGUI.ntcv_count_text.value), 
                    sg.Button('Find',s= button_size10,k=KeyGUI.ntcv_search_input.value), 
                    sg.Input(k= KeyGUI.ntcv_selected_input.value,visible=False)],
                    
                    ntcv_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.ntcv_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.ntcv_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.ntcv_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.ntcv_delete.value)]
                    ]    

    nktc_tab_layout = [
                    [sg.Text('Find',s= text_size10), 
                    sg.Input(s= input_size20,k=KeyGUI.nktc_search_input.value), 
                    sg.Text(s= text_size10,k= KeyGUI.nktc_count_text.value), 
                    sg.Button('Find',s= button_size10,k=KeyGUI.nktc_search_input.value), 
                    sg.Input(k= KeyGUI.nktc_selected_input.value,visible=False)],
                    
                    nktc_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.nktc_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.nktc_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.nktc_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.nktc_delete.value)]
                    ] 

    main_layout =   [
                    menubar_main_element,
                    [sg.TabGroup([
                        # [sg.Tab('Worker',tab_worker_layout(),k='-WORKER TAB-')],
                        # [sg.Tab('Machine',tab_machine_layout(),k='-MACHINE TAB-')],
                        # [sg.Tab('Material',tab_material_layout(),k='-MATERIAL TAB-')],
                        [sg.Tab('Norm', norm_tab_layout, k= KeyGUI.norm_tab.value)],
                        [sg.Tab('Work', work_tab_layout, k= KeyGUI.work_tab.value)],
                        [sg.Tab('NTCV', ntcv_tab_layout, k= KeyGUI.ntcv_tab.value)],
                        [sg.Tab('LMTN', lmtn_tab_layout, k= KeyGUI.lmtn_tab.value)],
                        [sg.Tab('NTVL', ntvl_tab_layout, k= KeyGUI.ntvl_tab.value)],
                        [sg.Tab('NKTC', nktc_tab_layout, k= KeyGUI.nktc_tab.value)],
                        
                        ],k= KeyGUI.group_tab.value, enable_events= True,expand_x= True, expand_y= True)],
                    
                    [sg.Sizegrip()]
                ]

# def tab_machine_layout():
#     layout = [
#         [Text('Find',(5,1)).GUI,sg.Input(s=(20,1),k='-MACHINE SEARCH INPUT-'),sg.Text(s=(5,1),k='-MACHINE COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-MACHINE FIND BUTTON-')],
#         [sg.Table(values=[],headings=['id','name','unit','amount'],k='-TABLE MACHINE-',col_widths=[6,35,6],auto_size_columns=False,justification='l')],
#         [sg.Push(),sg.Button('Add',s=(10,1),k='-ADD MACHINE-'),sg.Button('Edit',s=(10,1),k='-EDIT MACHINE-'),sg.Button('Delete',s=(10,1),k='-DELETE MACHINE-')]
#     ]
#     return layout

# def tab_material_layout():
#     layout = [
#         [Text('Find',(5,1)).GUI,sg.Input(s=(20,1),k='-MATERIAL SEARCH INPUT-'),sg.Text(s=(5,1),k='-MATERIAL COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-MATERIAL FIND BUTTON-')],
#         [sg.Table(values=[],headings=['id','name','unit','amount'],k='-TABLE MATERIAL-',col_widths=[6,35,6],auto_size_columns=False,justification='l')],
#         [sg.Push(),sg.Button('Add',s=(10,1),k='-ADD MATERIAL-'),sg.Button('Edit',s=(10,1),k='-EDIT MATERIAL-'),sg.Button('Delete',s=(10,1),k='-DELETE MATERIAL-')]
#     ]
#     return layout

# def tab_worker_layout():
#     layout = [
#         [Text('Find',(5,1)).GUI,sg.Input(s=(20,1),k='-WORKER SEARCH INPUT-'),sg.Text(s=(5,1),k='-WORKER COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-WORKER FIND BUTTON-')],
#         [sg.Table(values=[],headings=['id','name','unit','amount'],k='-TABLE WORKER-',col_widths=[6,35,6],auto_size_columns=False,justification='l')],
#         [sg.Push(),sg.Button('Add',s=(10,1),k='-ADD WORKER-'),sg.Button('Edit',s=(10,1),k='-EDIT WORKER-'),sg.Button('Delete',s=(10,1),k='-DELETE WORKER-')]
#     ]
#     return layout



def GUI():
    sg.theme('Dark')
    window = sg.Window('Main',
                layout=layout.main_layout.value,
                right_click_menu=layout.right_click_menu_def.value, 
                grab_anywhere=True,
                resizable=True,finalize=True,  
                # location=(300,300),
                margins=(0, 0)
    )

    window[KeyGUI.group_tab.value].expand(True,True)
    
    window[KeyGUI.norm_search_input.value].bind('<Return>', '_Enter')
    window[KeyGUI.work_search_input.value].bind('<Return>', '_Enter')
    
    window.set_min_size(layout.WINDOWN_SIZE.value)
    
    #------------------------------------WINDOW BIND------------------------------------
    # window[InputDinhMucTim.key].bind("<Return>", "_Enter")
    # window[InputCongTacKhoiLuong.key].bind("<Return>", "_Enter") 
    # window[InputCongTrinhEnd.key].bind("<Return>", "_Enter")
    window[KeyGUI.norm_tree.value].bind('<Double-Button-1>' , " double click")
    window[KeyGUI.work_tree.value].bind('<Double-Button-1>' , " double click")
    window[KeyGUI.lmtn_tree.value].bind('<Double-Button-1>' , " double click")
    window[KeyGUI.ntvl_tree.value].bind('<Double-Button-1>' , " double click")
    window[KeyGUI.ntcv_tree.value].bind('<Double-Button-1>' , " double click")
    window[KeyGUI.nktc_tree.value].bind('<Double-Button-1>' , " double click")
    
    
    window.bind('<F1>','-F1-')
    window.bind('<F2>','-F2-')
    window.bind('<F3>','-F3-')
    return window