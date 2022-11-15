from data_access import norm_db, qlcl_db
from repository1 import repository
import time
import PySimpleGUI as sg
from enum import Enum
import pandas as pd

class KeyGUI(Enum):
    # hang_muc_create_btn = '-hang muc create button-'
    # hang_muc_add_on_menu_work_tree = 'Thêm hạng mục'
    # phan_viec_add_on_menu_work_tree = 'Thêm phần việc'
    # phan_viec_create_btn = '-phan viec create button-' 
    
    norm_add_on_menu_bar = 'Thêm từ dự toán' # ok
    work_add_right_click_tree_norm = 'Thêm công việc' # ok
    norm_view_right_click_tree_norm = 'Xem định mức' #ok

    work_view_right_click_tree_norm = 'Xem công việc', #ok
    work_delete_right_click_tree_norm = 'Xóa công việc', #ok
    lmtn_add_right_click_tree_norm = 'Thêm LMTN',#ok
    ntvl_add_right_click_tree_norm = 'Thêm NTVL',#ok
    ntcv_add_right_click_tree_norm = 'Thêm NTCV',#ok

    hang_muc_add_on_menu_bar = 'Thêm hạng mục', #ok
    phan_viec_add_on_menu_bar = 'Thêm phần việc', #ok
    hang_muc_edit_on_menu_bar = 'Sửa hạng mục', #ok
    phan_viec_edit_on_menu_bar = 'Sửa phần việc', #ok
    
    norm_search_input = '-norm search input-'
    norm_count_text = '-norm count text-'
    norm_search_btn = '-norm search button-' #ok
    norm_tree = '-norm tree-'
    
    norm_id_create_work = '-create work with norm id-' #ok
    # norm_create = '-norm create button-'
    norm_edit = '-norm edit button-' #ok
    # norm_copy = '-norm copy button-'
    # norm_delete = '-norm delete button-'

    work_add_from_excel_btn = '-work add from excel button-'
    work_search_input = '-work search input-'
    work_count_text = '-work count text-'
    work_search_btn = '-work search button-' #ok
    work_tree = '-work tree-'
    
    work_create_btn = '-work create button-' #ok
    work_edit_btn = '-work edit button-'#ok
    work_copy_btn = '-work copy button-'#ok
    work_delete_btn = '-work delete button-'#ok
    work_visualization_btn = '-work visualization button-'#ok
        
    lmtn_search_input = '-lmtn search input-'
    lmtn_count_text = '-lmtn count input-'
    lmtn_search_button = '-lmtn search button-'
    lmtn_selected_input = '-selected lmtn id input-'
    lmtn_tree = '-lmtn tree-'
    lmtn_create = '-lmtn create button-'
    lmtn_edit = '-lmtn edit button-'
    lmtn_copy = '-lmtn copy button-'
    lmtn_delete = '-lmtn delete button-'        

    ntvl_search_input = '-ntvl search input-'
    ntvl_count_text = '-ntvl count input-'
    ntvl_search_button = '-ntvl search button-'
    ntvl_selected_input = '-selected ntvl id input-'
    ntvl_tree = '-ntvl tree-'
    ntvl_create = '-ntvl create button-'
    ntvl_edit = '-ntvl edit button-'
    ntvl_copy = '-ntvl copy button-'
    ntvl_delete = '-ntvl delete button-'
 
    ntcv_search_input = '-ntcv search input-'
    ntcv_count_text = '-ntcv count input-'
    ntcv_search_button = '-ntcv search button-'
    ntcv_selected_input = '-selected ntcv id input-'
    ntcv_tree = '-ntcv tree-'
    ntcv_create = '-ntcv create button-'
    ntcv_edit = '-ntcv edit button-'
    ntcv_copy = '-ntcv copy button-'
    ntcv_delete = '-ntcv delete button-'       

    nktc_search_input = '-nktc search input-'
    nktc_count_text = '-nktc count input-'
    nktc_search_button = '-nktc search button-'
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
    button_size10 = (15,1)
    text_size5 = (5,1)
    text_size10 = (10,1)
    input_size20 = (20,1)
    input_size40 = (40,1)
    font13 = ('Courier',13)
    font11 = ('Courier',11)
    font9 = ('Courier',9)
    
    right_click_menu_def = [[], ['Quan', 'Yeu', 'Hang','More Nothing','Exit']]
    right_click_menu_tab_norm = [[], [KeyGUI.norm_view_right_click_tree_norm.value, KeyGUI.work_add_right_click_tree_norm.value, 'More']]
    right_click_menu_tab_work = [[], [KeyGUI.work_view_right_click_tree_norm.value,
                                      KeyGUI.work_delete_right_click_tree_norm.value,
                                      KeyGUI.lmtn_add_right_click_tree_norm.value,
                                      KeyGUI.ntvl_add_right_click_tree_norm.value,
                                      KeyGUI.ntcv_add_right_click_tree_norm.value,]]
    
    menu_def = [['Công trình', ['Save','Open','Exit']],
            ['Định mức', [KeyGUI.norm_add_on_menu_bar.value,]],
            ['Công việc', [KeyGUI.norm_add_on_menu_bar.value,
                           KeyGUI.hang_muc_add_on_menu_bar.value,
                           KeyGUI.phan_viec_add_on_menu_bar.value,
                           KeyGUI.hang_muc_edit_on_menu_bar.value,
                           KeyGUI.phan_viec_edit_on_menu_bar.value,]]]
    
    menubar_main_element = [sg.MenubarCustom(menu_def, font=font13)]  

    norm_tree_element = [sg.Tree(data=sg.TreeData(), 
                        headings=['ID','UNIT','amount'], 
                        k=KeyGUI.norm_tree.value, col0_heading='NORM',
                        col0_width=50, col_widths=[6,6,6],
                        auto_size_columns=False,
                        right_click_menu= right_click_menu_tab_norm,
                        expand_x=True, expand_y= True,
                        select_mode= sg.TABLE_SELECT_MODE_EXTENDED,
                        enable_events=True,)]
    
    work_tree_element = [sg.Tree(data=sg.TreeData(),
                        headings=['work','norm_id','unit','amount','start','end'],
                        k= KeyGUI.work_tree.value,
                        col0_heading='ID',
                        col0_width=6,
                        col_widths=[40,6,6,6,6,6],
                        auto_size_columns=False,
                        right_click_menu= right_click_menu_tab_work,
                        select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
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
                    [sg.Input(s= input_size20,k=KeyGUI.norm_search_input.value), 
                    sg.Text(s= text_size5,k= KeyGUI.norm_count_text.value), 
                    sg.Button('Search',s= button_size10,k=KeyGUI.norm_search_btn.value)],
                    
                    norm_tree_element,
                    
                    [sg.Push(), 
                    sg.Button('Thêm công việc',s= button_size10,k= KeyGUI.norm_id_create_work.value),
                    sg.Button('Xem thông tin',s= button_size10,k= KeyGUI.norm_edit.value),]
                    # sg.Button('Copy',s= button_size10,k= KeyGUI.norm_copy.value),
                    # sg.Button('Delete',s= button_size10,k= KeyGUI.norm_delete.value)
                    ]
    
    work_tab_layout = [
                    [sg.Input(s= input_size20,k=KeyGUI.work_search_input.value), 
                    sg.Text(s= text_size5,k= KeyGUI.work_count_text.value), 
                    sg.Button('search',s= button_size10,k=KeyGUI.work_search_input.value)],
                    
                    work_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Đồ thị',s=button_size10, k= KeyGUI.work_visualization_btn.value),
                    sg.Button('Thêm',s= button_size10,k= KeyGUI.work_create_btn.value),
                    sg.Button('Thêm bằng excel',s= button_size10,k= KeyGUI.work_add_from_excel_btn.value),
                    sg.Button('Xem-Sửa',s= button_size10,k= KeyGUI.work_edit_btn.value),
                    sg.Button('Tạo copy',s= button_size10,k= KeyGUI.work_copy_btn.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.work_delete_btn.value),]
                    ]

    lmtn_tab_layout = [
                    [sg.Input(s= input_size20,k=KeyGUI.lmtn_search_input.value), 
                    sg.Text(s= text_size5,k= KeyGUI.lmtn_count_text.value), 
                    sg.Button('search',s= button_size10,k=KeyGUI.lmtn_search_input.value), 
                    sg.Input(k = KeyGUI.lmtn_selected_input.value,visible=False)],
                    
                    lmtn_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.lmtn_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.lmtn_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.lmtn_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.lmtn_delete.value)]
                    ]

    ntvl_tab_layout = [
                    [sg.Input(s= input_size20,k=KeyGUI.ntvl_search_input.value), 
                    sg.Text(s= text_size5,k= KeyGUI.ntvl_count_text.value), 
                    sg.Button('search',s= button_size10,k=KeyGUI.ntvl_search_input.value), 
                    sg.Input(k= KeyGUI.ntvl_selected_input.value,visible=False)],
                    
                    ntvl_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.ntvl_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.ntvl_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.ntvl_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.ntvl_delete.value)]
                    ]
    
    ntcv_tab_layout = [
                    [sg.Input(s= input_size20,k=KeyGUI.ntcv_search_input.value), 
                    sg.Text(s= text_size5,k= KeyGUI.ntcv_count_text.value), 
                    sg.Button('search',s= button_size10,k=KeyGUI.ntcv_search_input.value), 
                    sg.Input(k= KeyGUI.ntcv_selected_input.value,visible=False)],
                    
                    ntcv_tree_element,
                    
                    [sg.Push(),
                    sg.Button('Create',s= button_size10,k= KeyGUI.ntcv_create.value),
                    sg.Button('Edit',s= button_size10,k= KeyGUI.ntcv_edit.value),
                    sg.Button('Create copy',s= button_size10,k= KeyGUI.ntcv_copy.value),
                    sg.Button('Delete',s= button_size10,k= KeyGUI.ntcv_delete.value)]
                    ]    

    nktc_tab_layout = [
                    [sg.Input(s= input_size20,k=KeyGUI.nktc_search_input.value), 
                    sg.Text(s= text_size5,k= KeyGUI.nktc_count_text.value), 
                    sg.Button('search',s= button_size10,k=KeyGUI.nktc_search_input.value), 
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
                        [sg.Tab('Norm', norm_tab_layout, k= KeyGUI.norm_tab.value)],
                        [sg.Tab('Work', work_tab_layout, k= KeyGUI.work_tab.value)],
                        [sg.Tab('NTCV', ntcv_tab_layout, k= KeyGUI.ntcv_tab.value)],
                        [sg.Tab('LMTN', lmtn_tab_layout, k= KeyGUI.lmtn_tab.value)],
                        [sg.Tab('NTVL', ntvl_tab_layout, k= KeyGUI.ntvl_tab.value)],
                        [sg.Tab('NKTC', nktc_tab_layout, k= KeyGUI.nktc_tab.value)],
                        
                        ],k= KeyGUI.group_tab.value, enable_events= True,expand_x= True, expand_y= True)],
                    
                    [sg.Sizegrip()]
                ]

class QLCL:
    def __init__(self, window, norm_db:norm_db, qlcl_db:qlcl_db) -> None:
        self.window = window
        self.norm_db = norm_db
        self.qlcl_db = qlcl_db
        self.norm_db.connect()
        self.qlcl_db.connect()
        self.norm_db.create_database()
        self.qlcl_db.create_database()
        
        self.norm_tree = self.window[KeyGUI.norm_tree.value]
        self.work_tree = self.window[KeyGUI.work_tree.value]
        
        
    def handling_event(self,event,values):
        event_dict = {KeyGUI.group_tab.value: self.show,
                      KeyGUI.work_add_from_excel_btn.value: self.work_add_from_excel_btn_click}
        self.values = values
        if event in event_dict:
            event_dict[event]()
            
    def show(self):
        # display tree
        tree_name = self.values[KeyGUI.group_tab.value]
        display_dict = {KeyGUI.norm_tab.value: self.show_tree_norm,
                        KeyGUI.work_tab.value: self.show_tree_work,}
        if tree_name in display_dict:
            display_dict[tree_name]()
            
    def work_add_from_excel_btn_click(self):
        path = sg.popup_get_file('Nhập đường dẫn file excel công việc',
                                 'Công việc',
                                 default_extension='.xlsx',
                                 file_types=(("Excel Files", "*.xlsx"),))
        if path:
            if self._work_add_from_excel(path):
                sg.PopupOK('Công việc thêm thành công', auto_close=True, keep_on_top=True)
            

    def _work_add_from_excel(self,path):
        try:
            self._import_to_data_base(self._read_excel(path))
            return 1
        except:
            print(f'Error on {self.__class__.__name__}._work_add_from_excel')
            return 0
    
    @staticmethod
    def _read_excel(path):
        try:
            df_dict = {}
            xls = pd.ExcelFile(path)
            for name in xls.sheet_names:
                df_dict[name] = xls.parse(name,header=0,index_col=0,)
            return df_dict
        except:
            print(f'Error on staticmethod qlcl._read_excel')
            return 0

    def _import_to_data_base(self, df_dict:dict):
        try:
            if 'work' in df_dict:
                df_dict['work'].to_sql(name='work',con=self.qlcl_db.conn,if_exists='replace')
            return 1
        except:
            print(f'Error on {self.__class__.__name__}._import_to_data_base')
            return 0
    
    def event_create_norm_from_du_toan(self,path):
        pass
    
    def show_tree_norm(self):
        norm = self.norm_db.fetchall("SELECT * FROM norm ORDER BY id")
        if norm:
            self._norm_tree_display(norm)

    def show_tree_work(self):
        work = self.qlcl_db.fetchall("SELECT * FROM work ORDER BY id")
        if work:
            self._work_tree_display(work)

    def _work_tree_display(self, work):
        treedata = sg.TreeData()
        for item in work:
            treedata.Insert('',item[0],item[0],[item[1],item[2], item[3], item[4], item[5], item[6]])
        self.work_tree.update(treedata)
            
    def _norm_tree_display(self, norm):
        treedata = sg.TreeData()
        for item in norm:
            treedata.Insert('',item[0],item[1],[item[0],item[2]])
        self.norm_tree.update(treedata)

def main():
    normDB = norm_db('norm.db')
    qlclDB = qlcl_db('qlcl.db')
    
    window = sg.Window('Quản lý chất lượng công trình', layout.main_layout.value, finalize=True, resizable=True, margins=(0, 0))
    qlcl = QLCL(window, normDB, qlclDB)
    while True:
        event, values = window.read()
        print(event,'\n', values)
        if event in [None,'Exit']:
            break
        else:
            qlcl.handling_event(event, values)
    
    normDB.disconect()
    qlclDB.disconect()

if __name__ == "__main__":
    start = time.time()
    main()
    print('time exe: ', round((time.time()-start)*10**3,2),' ms')
