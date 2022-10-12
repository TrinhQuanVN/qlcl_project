import PySimpleGUI as sg
from itertools import count
FONT_ANY_13 =('Any',13)
FONT_ANY_11 = ('Any',11)

class CheckBox:
    id_iter = count()
    def __init__(self,text,size,default=True,tooltip='Chưa có',enableEvent=True) -> None:
        self.text = text
        self.size = size
        self.default = default
        self.enableEvent = enableEvent
        self.tooltip = tooltip
        self.key = f'-CHECKBOX{next(self.id_iter)}-'
    
    @property
    def GUI(self):
        # return sg.Checkbox(self.text,s=self.size,default=self.default,tooltip=self.tooltip,k=self.key,enable_events=self.enableEvent,font=FONT_ANY_11)
        # return sg.Checkbox(self.text,self.default,self.size,font=FONT_ANY_11,enable_events=self.enableEvent,tooltip=self.tooltip)
        return sg.Checkbox('Checkbox', default=True, k='-CB-')
    
class Combo:
    id_iter = count()
    def __init__(self,size,values=[],enableEvent=False,default='') -> None:
        self.values = values
        self.size = size
        self.Event = enableEvent
        self.default = default
        self.key = f'-COMBO{next(self.id_iter)}-'
    @property
    def GUI(self):
        return sg.Combo(self.values,s=self.size,k=self.key,font=FONT_ANY_11,enable_events=self.Event,default_value=self.default)
       
class Button:
    id_iter = count()
    def __init__(self,text,size) -> None:
        self.text = text
        self.key = f'-BUTTON{next(self.id_iter)}-'
        self.size = size
        
    @property
    def GUI(self):
        return sg.Button(self.text,s=self.size,k=self.key,font=FONT_ANY_11)
    
class Input:
    id_iter = count()
    def __init__(self,size,defaultText='',expand_x=True,enableEvent=False) -> None:
        self.size = size
        self.defaultText = defaultText
        self.expand_x = expand_x
        self.event = enableEvent
        self.key = f'-INPUT{next(self.id_iter)}-'
    
    @property
    def GUI(self):
        return sg.Input(s=self.size,expand_x=self.expand_x,k=self.key,default_text=self.defaultText,enable_events=self.event,font=FONT_ANY_11)
    
class Tab:
    id_iter = count()
    def __init__(self,title,layout,tooltip='Chưa có',elementJusfication='l',expandX=True,expandY=True) -> None:
        self.title = title
        self.layout = layout
        self.key = f'-TAB{next(self.id_iter)}-'
        self.tooltip = tooltip
        self.elementJus = elementJusfication
        self.expX = expandX
        self.expY = expandY
        
    @property
    def GUI(self):
        return sg.Tab(self.title,self.layout,tooltip=self.tooltip,k=self.key,font=FONT_ANY_13,
                      element_justification=self.elementJus,expand_x=self.expX,expand_y=self.expY)

class Text:
    id_iter = count()
    def __init__(self,text,size,tooltip='Chưa có',justification='r',enableEvent =False) -> None:
        self.text = text
        self.size = size
        self.jus = justification
        self.key = f'-TEXT{next(self.id_iter)}-'
        self.tooltip = tooltip
        self.enEvent = enableEvent
    
    @property
    def GUI(self):
        return sg.Text(self.text,s=self.size,tooltip=self.tooltip,
                       k=self.key,font=FONT_ANY_11,justification=self.jus,
                       enable_events=self.enEvent)

class TreeData:
    def __init__(self) -> None:
        self.data = sg.TreeData()
        
    @property
    def GUI(self):
        return self.data
    
    def Insert(self,parent,key,text,values):
        self.data.Insert(parent,key,text,values)

class Tree:
    id_iter = count()
    def __init__(self,treeData:TreeData,headings,col0_width,col0_heading,col_widths,justification='c',rcMenu=[]) -> None:
        self.treeData = treeData
        self.headings = headings
        self.col0Width = col0_width
        self.col0Heading = col0_heading
        self.jus = justification
        self.key = f'-TREE{next(self.id_iter)}-'
        self.colWidths = col_widths
        self.rcMenu = [[],rcMenu] if rcMenu else None
    
    @property
    def GUI(self):
        return sg.Tree(self.treeData.GUI,headings=self.headings,
                       col0_width=self.col0Width,col0_heading=self.col0Heading,
                       col_widths= self.colWidths,
                       expand_x=True,expand_y=True,auto_size_columns=False, # Mới thêm auto_size
                       justification=self.jus,k=self.key,font=FONT_ANY_11,
                       enable_events=True,vertical_scroll_only=False,right_click_menu=self.rcMenu)   
    
def main():
    for _ in range(10):
        button = Button('a',(1,1))
        print(button.key)
        
if __name__ == "__main__":
    main()