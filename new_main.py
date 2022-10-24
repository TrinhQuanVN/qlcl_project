import PySimpleGUI as sg



class GUI():
    def __init__(self):
        self.font1 = ('Courier', 9, 'bold')
        self.font2 = ('Courier', 12, 'bold')
        self.button_size = 10
        self.line_width = 100
        self.book = 'Book.json'
        self.treedata = sg.TreeData()
        
    def Main_Layout(self):
        menu_def = [['Công trình', ['Save','Open','Exit']],
            ['Định mức', ['Show nhân công','Show máy','Show vật liệu','Mở định mức','Thêm từ dự toán',]]]
        
        right_click_menu_def = [[], ['Quan', 'Yeu', 'Hang','More Nothing','Exit']]
        
        right_click_menu_tab_norm = [['a'], ['Copy', 'Paste', 'Delete','Create a copy','More']]
        
        layout_tab_norm = [
        [sg.Text('Find',(5,1)),sg.Input(s=(20,1),k='-NORM SEARCH INPUT-'),sg.Text(s=(5,1),k='-NORM COUNT TEXT-'),sg.Button('Find',s=(10,1),k='-NORM FIND BUTTON-')],
        [sg.Tree(data=sg.TreeData(),headings=['ID','UNIT','amount'],k='-TREE NORM-',col0_heading='NORM',col0_width=50,col_widths=[6,6,6],auto_size_columns=False,enable_events=True)],
        [sg.Push(),sg.Button('Add work',s=(10,1),k='-ADD WORK WITH NORM ID-'),sg.Button('Add',s=(10,1),k='-ADD NORM-'),sg.Button('Edit',s=(10,1),k='-EDIT NORM-'),sg.Button('Create a copy',s=(15,1),k='-CREATE COPY NORM-'),sg.Button('Delete',s=(10,1),k='-DELETE NORM-')]
    ]
        
        return [
                [sg.MenubarCustom(menu_def, font=self.font1)], #Menubar
                
                [sg.TabGroup(layout=[
                    [sg.Tab('Norm',layout_tab_norm,k='-NORM TAB-',right_click_menu=right_click_menu_tab_norm)]
                                    ]
                            ,k='-TAB GROUP-',enable_events=True)],
                # [self.Input('Load File'), self.Browse_File('Load File'),
                #  self.Input('Load Path'), self.Browse_Path('Load Path'),
                #  self.Button('Sort'),           self.Button('Rename'),
                #  self.Button('Delete'),         self.Button('Move Up'),
                #  self.Button('Move Down'),      self.Button('Quit')],
                # [self.Tree('TREE'), self.Multiline('MULTILINE')]
                ]

    def Window(self, layout,theme:str):
        sg.theme(theme)
        self.window = sg.Window('Trịnh Tiến Quân', layout=layout,
            margins=(0, 0), use_default_focus=False, finalize=True)
        # self.tree = self.window['TREE']
        # self.multiline = self.window['MULTILINE']
        # self.tree.Widget.configure(show='tree')    # Invisiable Header
        # self.tree.bind('<Button-1>', 'Down')       # add Button-1 event to Tree

    def text(self,text='',k='',s=(5,1),justification='r'):
        return sg.Text(text=text,s=s, justification=justification, font=self.font1)

    def Button(self, key):
        return sg.Button(key, enable_events=True, size=(self.button_size, 1),
            font=self.font1, pad=((0, 5), 5))

    def Tree(self, key):
        return sg.Tree(data=self.treedata, headings=['Notes',], pad=(0, 0),
        show_expanded=False, col0_width=30, auto_size_columns=False,
        visible_column_map=[False,], select_mode=sg.TABLE_SELECT_MODE_BROWSE,
        enable_events=True, #  text_color='black', background_color='white'
        font=self.font2, num_rows=28, row_height=20, key=key)

    def Input(self, key):
        return sg.Input('', font=self.font1, key=key, visible=False,
            enable_events=True, do_not_clear=False, pad=((0, 5), 5))

    def Multiline(self, key):
        return sg.Multiline(default_text='', enable_events=False, pad=((0, 5), 5),
            size=(self.line_width, 31), do_not_clear=True, disabled=True,
            key=key, border_width=0, focus=False, font=self.font1,)
            #text_color='white', background_color='blue')

    def Browse_File(self, key):
        return sg.FileBrowse(button_text=key, target=key, font=self.font1,
            size=(self.button_size, 1), enable_events=True, pad=((0, 5), 5),
            file_types=(("ALL Python Files", "*.py"),))
        
    def load_norm_from_excel(self):
        pass
def main():
    G = GUI()
    G.Window(G.Main_Layout(),theme='DarkAmber')
    # G.Load_Book()
    func = {'Thêm từ dự toán':G.load_norm_from_excel, 'Load Path':G.Load_Path, 'Sort'   :G.Sort,
            'Rename'   :G.Rename,    'Delete'   :G.Delete,    'Move Up':G.Move_Up,
            'Move Down':G.Move_Down}
    while True:

        event, values = G.window.Read()
        print(event)

        if event in [None, 'Exit']:
            break

    #     elif event in func:
    #         func[event](values)

    #     key = G.Where()
    #     txt = G.treedata.tree_dict[key].values[0] if key else ''
    #     G.multiline.Update(value=txt)

    # G.Save_Book()
    G.window.close()
    
if __name__ == "__main__":
    main()