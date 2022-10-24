import PySimpleGUI as sg



class GUI():

    def __init__(self):
        self.font1 = ('Courier', 12, 'bold')
        self.font2 = ('Courier', 12, 'bold')
        self.button_size = 10
        self.line_width = 100
        self.book = 'Book.json'
        self.treedata = sg.TreeData()
        
    def Layout(self):
        return [[self.Input('Load File'), self.Browse_File('Load File'),
                 self.Input('Load Path'), self.Browse_Path('Load Path'),
                 self.Button('Sort'),           self.Button('Rename'),
                 self.Button('Delete'),         self.Button('Move Up'),
                 self.Button('Move Down'),      self.Button('Quit')],
                [self.Tree('TREE'), self.Multiline('MULTILINE')]]

    def Window(self, layout):
        sg.theme('Topanga')
        self.window = sg.Window('Docstring for Python Files', layout=layout,
            margins=(0, 0), use_default_focus=False, finalize=True)
        self.tree = self.window['TREE']
        self.multiline = self.window['MULTILINE']
        self.tree.Widget.configure(show='tree')    # Invisiable Header
        # self.tree.bind('<Button-1>', 'Down')       # add Button-1 event to Tree

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
        
        
G = GUI()
G.Window(G.Layout())
G.Load_Book()
func = {'Load File':G.Load_File, 'Load Path':G.Load_Path, 'Sort'   :G.Sort,
        'Rename'   :G.Rename,    'Delete'   :G.Delete,    'Move Up':G.Move_Up,
        'Move Down':G.Move_Down}
while True:

    event, values = G.window.Read()

    if event in [None, 'Quit']:
        break

    elif event in func:
        func[event](values)

    key = G.Where()
    txt = G.treedata.tree_dict[key].values[0] if key else ''
    G.multiline.Update(value=txt)

G.Save_Book()
G.window.close()