from datetime import datetime
import Framework
import Extension as ex
import Models
import PySimpleGUI as sg
import Elements
from py_linq import Enumerable

def Combo(values=[],s=(20,1),k='',default_value=None,enable_event=True,font=('Any',11),expand_x=True):
    return sg.Combo(values=values,s=s,k=k,default_value=default_value,enable_events=enable_event,font=font,expand_x=expand_x)

def I(s=(10,1),k='',default_text='',readonly=False,text_color=None,justification='l',font=('Any',11)):
    return sg.Input(s=s,k=k,default_text=default_text,readonly=readonly,text_color=text_color,justification=justification,font=font)

def T(text='',k='',s=(5,1),justification='r',font=('Any',11)):
    return sg.Text(text=text,s=s, justification=justification, font=font)

def Btn(button_text='',k='',s=(10,1)):
    return sg.Button(button_text=button_text,k=k,s=s)

KEYCAP_ESC = '<ESCAPE>'
KEYCAP_ENTER = "<Return>"

ESCAPE = '-ESCAPE-'
ENTER = '-ENTER-'

def show_all():
    Framework.Route.Foward('material list')
    Framework.Route.Foward('machine list')
    Framework.Route.Foward('worker list')
    Framework.Route.Foward('norm list')
    
    Framework.Route.Foward('norm count')
    Framework.Route.Foward('worker count')
    Framework.Route.Foward('machine count')
    Framework.Route.Foward('material count')
    
    Framework.Route.Foward('work count')
    Framework.Route.Foward('work list')
    

class base_view:
    def __init__(self,**kwargs) -> None:
        self.kwargs = kwargs
        
    @staticmethod
    def foward(route,**kwargs):
        if not kwargs:
            Framework.Route.Foward(route)
            return
        request = []
        for key in kwargs:
            request.append('{} = {} &'.format(key,kwargs[key]))
        result = route + '?' + ''.join(request)
        print(request)
        Framework.Route.Foward(result.strip()[:-1])
        print(result)

class save_file_menu_bar_view(base_view):
    def Render(self):
        layout =[
            [sg.Text('Đường dẫn'),sg.Input(k='-INPUT-'),sg.FileSaveAs('Browse')],
            [sg.Button('Save'),sg.Button('Clear'),sg.Button('Cancel')]
        ]
        window = sg.Window('Save file',layout,keep_on_top=True)
        while True:
            event,values = window.read()
            if event in [None,'Cancel']:
                break
            elif event == 'Save' and values['-INPUT-']:
                self.foward('file cons do save', path = values['-INPUT-'])
                break
            if event == 'Clear':
                window['-INPUT-'].update('')
        window.close()

class load_file_menu_bar_view(base_view):
    def Render(self):
        layout = [
            [sg.Text('Đường dẫn'),sg.Input(k='-INPUT-'),sg.FileBrowse('Browse')],
            # [sg.Text('Tên sheet'),sg.Input(k='-INPUT SHEET-',default_text='Chiết tính')],
            
            [sg.Button('Load'),sg.Button('Clear'),sg.Button('Cancel')]
        ]
        window = sg.Window('Save file',layout,keep_on_top=True)
        while True:
            event,values = window.read()
            if event in [None,'Cancel']:
                break
            elif event == 'Load' and values['-INPUT-']:
                self.foward('file cons do load', path = values['-INPUT-'])
                show_all()
                break
            if event == 'Clear':
                window['-INPUT-'].update('')
        window.close()

############################################################ HANG MUC
class work_time_update_view(base_view):
    def Render(self):
        wt = self.kwargs['work_time']
        
        id_text = T('Work ID',k='-WORK ID TEXT-')
        start_text = T('Start',k='-START TEXT-')
        end_text = T('End',k='-END TEXT-')

        default_start = ex.display_date_time(wt.start) if wt.start else ''
        default_end = ex.display_date_time(wt.end) if wt.end else ''
        
        id_in = I(k='-ID IN-',default_text=wt.work_id,readonly=True,text_color='black')
        start_in = I(k='-START IN-',default_text=default_start)
        end_in = I(k='-END IN-',default_text=default_end)
        
        update_btn = Btn('Update',k='-UPDATE-')
        clear_btn =  Btn('Clear',k='-CLEAR-')   
        cancel_btn = Btn('Cancel',k='-CANCEL-')    
        
        layout =[
            [id_text,id_in],
            [start_text,start_in],
            [end_text,end_in],
            [update_btn,clear_btn,cancel_btn]
        ]
        window = sg.Window('Update work time',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-',ESCAPE]:
                break
            elif event in ['-UPDATE-'] and values['-ID IN-']:
                self.foward('work time do update',work_id=values['-ID IN-'],start=values['-START IN-'],end=values['-END IN-'])

                self.foward('worker work time do create by work time',work_id=values['-ID IN-'],start=values['-START IN-'],end=values['-END IN-'])
                self.foward('work time list')
                break
            elif event == '-CLEAR-':
                for key in ['-START IN-','-END IN-']:
                    window[key].update('')
        window.close()

############################################################ WORK
class work_create_with_norm_id_view(base_view):
    def Render(self):
        def get_worker_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount
        
        def get_machine_amount(id,item_work):
            print(id)
            print(item_work)
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount

        def get_material_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount
        
        hang_muc = self.kwargs['hang_muc']
        
        workers = self.kwargs['workers']
        machines = self.kwargs['machines']
        materials = self.kwargs['materials']
        
        norm = self.kwargs['norm']
        worker_norm = self.kwargs['worker_norm']
        machine_norm = self.kwargs['machine_norm']
        material_norm = self.kwargs['material_norm']
        
        worker = self.kwargs['worker']
        machine = self.kwargs['machine']
        material = self.kwargs['material']
        
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        amount_text = Elements.Text('Amount',(5,1))
        hm_text = Elements.Text('Hang muc',(7,1))
        
        # id_in = sg.Input(s=(15,1),k='-ID IN-',expand_x=True,default_text=work_id,readonly=True,text_color='black')
        name_in = sg.Input(s=(15,1),expand_x=True,default_text=norm.name,k='-NAME IN-')
        unit_in = sg.Input(s=(15,1),expand_x=True,default_text=norm.unit,k='-UNIT IN-')
        amount_in = sg.Input(s=(15,1),expand_x=True,k='-AMOUNT IN-',enable_events=True)
        hm_combo = Combo(hang_muc,k=f'-COMBO HM-',default_value=hang_muc[-1])
        
        Create_btn = Elements.Button('Create',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [hm_text.GUI,hm_combo],
            [name_text.GUI,name_in],
            [unit_text.GUI,unit_in],
            [amount_text.GUI,amount_in],
            
            [Elements.Text('Worker',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Machine',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Material',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI],
        ]
        for i in range(10):
            layout.append([
                Combo(values=workers,s=(20,1),k=f'-COMBO WORKER{i}-',default_value=worker[i] if i <len(worker) else None),
                
                I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True,text_color='black',justification='c',default_text=worker[i].unit if i <len(worker) else None),
                
                I(s=(10,1),k=f'-INPUT WORKER{i}-',default_text=get_worker_amount(worker[i].id,worker_norm) if i <len(worker) else None),
                
                Combo(values=machines,s=(20,1),k=f'-COMBO MACHINE{i}-',default_value=machine[i] if i <len(machine) else None),
                
                I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c',default_text=machine[i].unit if i <len(machine) else None),
                
                I(s=(10,1),k=f'-INPUT MACHINE{i}-',default_text=get_machine_amount(machine[i].id,machine_norm) if i <len(machine) else None),
                
                Combo(values=materials,s=(20,1),k=f'-COMBO MATERIAL{i}-',default_value=material[i] if i <len(material) else None),
              
                I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c',default_text=material[i].unit if i <len(material) else None),
                
                I(s=(10,1),k=f'-INPUT MATERIAL{i}-',default_text=get_material_amount(material[i].id,material_norm) if i <len(material) else None),
                
                ])
            
        layout.append(
            [Create_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        )
        window = sg.Window('Create work',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window['-NAME IN-'].bind("<Return>", "_Enter")
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            print(event)
            if event in [sg.WIN_CLOSED,cancel_btn.key,'-ESCAPE-']:
                break
            
            if event == '-NAME IN-'+'_Enter' and  ex.is_norm(values['-NAME IN-'].lower().strip()):
                id = values['-NAME IN-'].lower().strip()
                self.foward('work create with norm id', id=id)
                break
            
            if event == '-AMOUNT IN-'+'_Enter' and  values['-AMOUNT IN-']:
                window['-AMOUNT IN-'].update(round(eval(values['-AMOUNT IN-']),2))
                for i in range(10):
                    if values[f'-INPUT WORKER{i}-']:
                        window[f'-INPUT WORKER{i}-'].update(round(eval('{}*{}'.format(values['-AMOUNT IN-'],get_worker_amount(values[f'-COMBO WORKER{i}-'].id,worker_norm))),2))
                        
                    if values[f'-INPUT MACHINE{i}-']:
                        window[f'-INPUT MACHINE{i}-'].update(round(eval('{}*{}'.format(values['-AMOUNT IN-'],get_machine_amount(values[f'-COMBO MACHINE{i}-'].id,machine_norm))),2))
                        
                    if values[f'-INPUT MATERIAL{i}-']:
                        window[f'-INPUT MATERIAL{i}-'].update(round(eval('{}*{}'.format(values['-AMOUNT IN-'],get_material_amount(values[f'-COMBO MATERIAL{i}-'].id,material_norm))),2))  
                                                                     
            if event in [f'-COMBO WORKER{i}-' for i in range(10)]:
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-']:
                        window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                        
            if event in [f'-COMBO MACHINE{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MACHINE{i}-']:
                        window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)
                        
            if event in [f'-COMBO MATERIAL{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MATERIAL{i}-']:
                        window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit) 
                              
            if event in [Create_btn.key]:
                id= 'W{}'.format(next(Models.work.id_iter))
                self.foward('work do create',
                            id= id,
                            name=values['-NAME IN-'],
                            unit=values['-UNIT IN-'],
                            amount=values['-AMOUNT IN-'],
                            hm_id=values['-COMBO HM-'].id)

                
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                        self.foward('worker work do create',
                                    work_id=id,
                                    id=values[f'-COMBO WORKER{i}-'].id,
                                    amount=values[f'-INPUT WORKER{i}-'])
                        
                    if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                        self.foward('machine work do create',
                                    work_id=id,
                                    id=values[f'-COMBO MACHINE{i}-'].id,
                                    amount=values[f'-INPUT MACHINE{i}-']) 
                        
                    if values[f'-COMBO MATERIAL{i}-'] and values[f'-INPUT MATERIAL{i}-']:
                        self.foward('material work do create',
                                    work_id=id,
                                    id=values[f'-COMBO MATERIAL{i}-'].id,
                                    amount=values[f'-INPUT MATERIAL{i}-'])                       

                self.foward('work list')

                self.foward('work time do create', work_id= id) # create work time
                break

            if event == clear_btn.key:
                for key in ['-NAME IN-','-UNIT IN-','-AMOUNT IN-']:
                    window[key].update('')
        window.close()

class work_create_view(base_view):
    def Render(self):
        def get_worker_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount
        
        def get_machine_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount

        def get_material_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount
        hang_muc = self.kwargs['hang_muc']
        
        worker = self.kwargs['worker']
        material = self.kwargs['material']
        machine = self.kwargs['machine']
        
        # id_text = Elements.Text('ID',(7,1))
        name_text = Elements.Text('Name',(7,1))
        unit_text = Elements.Text('Unit',(7,1))
        amount_text = Elements.Text('Amount',(7,1))
        hm_text = Elements.Text('Hang muc',(7,1))
        
        
        # id_in = sg.Input(s=(15,1),k='-ID IN-',expand_x=True,default_text=work_id,readonly=True,text_color='black')
        name_in = sg.Input(s=(15,1),expand_x=True,k='-NAME IN-')
        unit_in = sg.Input(s=(15,1),expand_x=True,k='-UNIT IN-')
        amount_in = sg.Input(s=(15,1),expand_x=True,k='-AMOUNT IN-')
        hm_combo = Combo(hang_muc,k=f'-COMBO HM-',default_value=hang_muc[-1])
        
        Create_btn = Elements.Button('Create',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [hm_text.GUI,hm_combo],
            [name_text.GUI,name_in],
            [unit_text.GUI,unit_in],
            [amount_text.GUI,amount_in],
            [Elements.Text('Worker',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Machine',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Material',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI],
        ]
        for i in range(10):
            layout.append([
                Combo(worker,k=f'-COMBO WORKER{i}-'), I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT WORKER{i}-',justification='r'),
                Combo(machine,k=f'-COMBO MACHINE{i}-'), I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT MACHINE{i}-',justification='r'),
                Combo(material,k=f'-COMBO MATERIAL{i}-'), I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT MATERIAL{i}-',justification='r'),
                ])
            
        layout.append(
            [Create_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        )
        window = sg.Window('Create work',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window['-NAME IN-'].bind("<Return>", "_Enter")
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window.bind('<Escape>','-ESCAPE-')
        
        while True:
            event,values = window.read()
            print(event)
            if event in [sg.WIN_CLOSED,cancel_btn.key,'-ESCAPE-']:
                break
            
            if event == '-AMOUNT IN-'+'_Enter' and  values['-AMOUNT IN-']:
                window['-AMOUNT IN-'].update(round(eval(values['-AMOUNT IN-']),2))
            
            if event in [f'-COMBO WORKER{i}-' for i in range(10)]:
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-']:
                        window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                        
            if event in [f'-COMBO MACHINE{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MACHINE{i}-']:
                        window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)
                        
            if event in [f'-COMBO MATERIAL{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MATERIAL{i}-']:
                        window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit) 
                              
            if event in [Create_btn.key]:
                id= 'W{}'.format(next(Models.work.id_iter))
                self.foward('work do create',
                            id= id,
                            name=values['-NAME IN-'],
                            unit=values['-UNIT IN-'],
                            amount=values['-AMOUNT IN-'],
                            hm_id=values['-COMBO HM-'].id)
                
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                        self.foward('worker work do create',
                                    work_id=id,
                                    id=values[f'-COMBO WORKER{i}-'].id,
                                    amount=values[f'-INPUT WORKER{i}-'])
                        
                    if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                        self.foward('machine work do create',
                                    work_id=id,
                                    id=values[f'-COMBO MACHINE{i}-'].id,
                                    amount=values[f'-INPUT MACHINE{i}-']) 
                        
                    if values[f'-COMBO MATERIAL{i}-'] and values[f'-INPUT MATERIAL{i}-']:
                        self.foward('material work do create',
                                    work_id=id,
                                    id=values[f'-COMBO MATERIAL{i}-'].id,
                                    amount=values[f'-INPUT MATERIAL{i}-'])                      

                self.foward('work list')
                break                                              

            if event == clear_btn.key:
                for key in [name_in.key,unit_in.key]:
                    window[key].update('')
        window.close()

class work_edit_view(base_view):
    def Render(self):
        def get_worker_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount
        
        def get_machine_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount

        def get_material_amount(id,item_work):
            return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount
        
        work = self.kwargs['work']
        hang_muc = self.kwargs['hang_muc']
        
        worker_work = self.kwargs['worker_work']
        machine_work = self.kwargs['machine_work']
        material_work = self.kwargs['material_work']
        
        worker = self.kwargs['worker']
        material = self.kwargs['material']
        machine = self.kwargs['machine']  

        hang_mucs = self.kwargs['hang_mucs']
        workers = self.kwargs['workers']
        materials = self.kwargs['materials']
        machines = self.kwargs['machines']
        
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        amount_text = Elements.Text('Amount',(5,1))
        hm_text = Elements.Text('Hang muc',(7,1))
        
        id_in = sg.Input(s=(15,1),expand_x=True,default_text=work.id,k='-ID IN-')
        name_in = sg.Input(s=(15,1),expand_x=True,default_text=work.name,k='-NAME IN-')
        unit_in = sg.Input(s=(15,1),expand_x=True,default_text=work.unit,k='-UNIT IN-')
        amount_in = sg.Input(s=(15,1),expand_x=True,k='-AMOUNT IN-',enable_events=True,default_text=work.amount)
        hm_combo = Combo(hang_mucs,k=f'-COMBO HM-',default_value=hang_muc)
        
        update_btn = Elements.Button('Update',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [id_text.GUI,id_in],
            [hm_text.GUI,hm_combo],
            [name_text.GUI,name_in],
            [unit_text.GUI,unit_in],
            [amount_text.GUI,amount_in],
            [Elements.Text('Worker',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Machine',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Material',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI],
        ]        
        
        for i in range(10):
            layout.append([
                Combo(values=workers,s=(20,1),k=f'-COMBO WORKER{i}-',default_value=worker[i] if i <len(worker) else None),
                
                I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True,text_color='black',justification='c',default_text=worker[i].unit if i <len(worker) else None),
                
                I(s=(10,1),k=f'-INPUT WORKER{i}-',default_text=get_worker_amount(worker[i].id,worker_work) if i <len(worker) else None),
                
                Combo(values=machines,s=(20,1),k=f'-COMBO MACHINE{i}-',default_value=machine[i] if i <len(machine) else None),
                
                I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c',default_text=machine[i].unit if i <len(machine) else None),
                
                sg.I(s=(10,1),k=f'-INPUT MACHINE{i}-',default_text=get_machine_amount(machine[i].id,machine_work) if i <len(machine) else None),
                
                Combo(values=materials,s=(20,1),k=f'-COMBO MATERIAL{i}-',default_value=material[i] if i <len(material) else None),
              
                I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c',default_text=material[i].unit if i <len(material) else None),
                
                I(s=(10,1),k=f'-INPUT MATERIAL{i}-',default_text=get_material_amount(material[i].id,material_work) if i <len(material) else None),
                
                ])
            
        layout.append( [update_btn.GUI,clear_btn.GUI,cancel_btn.GUI])
        window = sg.Window('Edit work',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window.bind(KEYCAP_ESC,ESCAPE)
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,ESCAPE]:
                break

            if event == '-AMOUNT IN-'+'_Enter' and  values['-AMOUNT IN-']:
                window['-AMOUNT IN-'].update(eval(values['-AMOUNT IN-']))
                for i in range(10):
                    if values[f'-INPUT WORKER{i}-']:
                        window[f'-INPUT WORKER{i}-'].update(round(eval('{}*{}/{}'.format(values['-AMOUNT IN-'],values[f'-INPUT WORKER{i}-'],work.amount)),2))
                        
                    if values[f'-INPUT MACHINE{i}-']:
                        window[f'-INPUT MACHINE{i}-'].update(round(eval('{}*{}/{}'.format(values['-AMOUNT IN-'],values[f'-INPUT MACHINE{i}-'],work.amount)),2))
                        
                    if values[f'-INPUT MATERIAL{i}-']:
                        window[f'-INPUT MATERIAL{i}-'].update(round(eval('{}*{}/{}'.format(values['-AMOUNT IN-'],values[f'-INPUT MATERIAL{i}-'],work.amount)),2)) 
            
            if event in [f'-COMBO WORKER{i}-' for i in range(10)]:
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-']:
                        window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                        
            if event in [f'-COMBO MACHINE{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MACHINE{i}-']:
                        window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)
                        
            if event in [f'-COMBO MATERIAL{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MATERIAL{i}-']:
                        window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit) 
            
            elif event in [update_btn.key] and values['-ID IN-']:
                self.foward('work do update',
                            id=values['-ID IN-'],
                            name=values['-NAME IN-'],
                            unit=values['-UNIT IN-'],
                            amout=values['-AMOUNT IN-'],
                            hm_id=values['-COMBO HM-'].id)
                
                # Xóa những cái worker work cũ:
                self.foward('worker work do delete by work id', work_id=work.id)
                self.foward('machine work do delete by work id', work_id=work.id)
                self.foward('material work do delete by work id', work_id=work.id)
                
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                        request = '''worker work do create ?
                            work_id = {} &
                            id = {} &
                            amount = {} '''.format(values['-ID IN-'],values[f'-COMBO WORKER{i}-'].id,values[f'-INPUT WORKER{i}-']) 
                        Framework.Route.Foward(request)
                    if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                        request = '''machine work do create ?
                            work_id = {} &
                            id = {} &
                            amount = {} '''.format(values['-ID IN-'],values[f'-COMBO MACHINE{i}-'].id,values[f'-INPUT MACHINE{i}-']) 
                        Framework.Route.Foward(request)
                    if values[f'-COMBO MATERIAL{i}-']  and values[f'-INPUT MATERIAL{i}-']:
                        request = '''material work do create ?
                            work_id = {} &
                            id = {} &
                            amount = {} '''.format(values['-ID IN-'],values[f'-COMBO MATERIAL{i}-'].id,values[f'-INPUT MATERIAL{i}-']) 
                        Framework.Route.Foward(request)                                                
                Framework.Route.Foward('work list')                                               

            elif event == clear_btn.key:
                for key in ['-NAME IN-','-UNIT IN-']:
                    window[key].update('')
        window.close()

############################################################ WORKER
class worker_update_view(base_view):
    def Render(self):
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        id_in = Elements.Input((15,1))
        name_in = Elements.Input((15,1))
        unit_in = Elements.Input((15,1))
        
        update_btn = Elements.Button('Update',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [id_text.GUI,id_in.GUI],
            [name_text.GUI,name_in.GUI],
            [unit_text.GUI,unit_in.GUI],
            [update_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        ]
        window = sg.Window('Update worker',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,ESCAPE]:
                break
            elif event in [update_btn.key] and values[id_in.key]:
                self.foward('worker do update',id=values[id_in.key],name=values[name_in.key],unit=values[unit_in.key])
                # break
            elif event == clear_btn.key:
                for key in [id_in.key,name_in.key,unit_in.key]:
                    window[key].update('')
        window.close()
############################################################ MACHINE
class machine_update_view(base_view):
    def Render(self):
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        id_in = Elements.Input((15,1))
        name_in = Elements.Input((15,1))
        unit_in = Elements.Input((15,1))
        
        update_btn = Elements.Button('Update',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [id_text.GUI,id_in.GUI],
            [name_text.GUI,name_in.GUI],
            [unit_text.GUI,unit_in.GUI],
            [update_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        ]
        window = sg.Window('Update machine',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,ESCAPE]:
                break
            elif event in [update_btn.key] and values[id_in.key]:
                self.foward('machine do update',id=values[id_in.key],name=values[name_in.key],unit=values[unit_in.key])
                Framework.Route.Foward('machine list')
                self.foward('material list')
                # break
            elif event == clear_btn.key:
                for key in [id_in.key,name_in.key,unit_in.key]:
                    window[key].update('')
        window.close()
############################################################ MATERIAL
class material_update_view(base_view):
    def Render(self):
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        id_in = Elements.Input((15,1))
        name_in = Elements.Input((15,1))
        unit_in = Elements.Input((15,1))
        
        update_btn = Elements.Button('Update',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [id_text.GUI,id_in.GUI],
            [name_text.GUI,name_in.GUI],
            [unit_text.GUI,unit_in.GUI],
            [update_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        ]
        
        window = sg.Window('Update material',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,ESCAPE]:
                break
            elif event in [update_btn.key] and values[id_in.key]:
                self.foward('material do update',id=values[id_in.key],name=values[name_in.key],unit=values[unit_in.key])
                self.foward('material list')
                # break
            elif event == clear_btn.key:
                for key in [id_in.key,name_in.key,unit_in.key]:
                    window[key].update('')
        window.close()
############################################################ NORM
class norm_create_view(base_view):
    def Render(self):
        
        worker = self.kwargs['worker']
        material = self.kwargs['material']
        machine = self.kwargs['machine']
        
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        id_in = Elements.Input((15,1))
        name_in = Elements.Input((15,1))
        unit_in = Elements.Input((15,1))
        
        Create_btn = Elements.Button('Create',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [id_text.GUI,id_in.GUI],
            [name_text.GUI,name_in.GUI],
            [unit_text.GUI,unit_in.GUI],
            [Elements.Text('Worker',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Machine',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Material',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI],
        ]
        for i in range(10):
            layout.append([
                Combo(worker,k=f'-COMBO WORKER{i}-'), I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT WORKER{i}-',justification='r'),
                Combo(machine,k=f'-COMBO MACHINE{i}-'), I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT MACHINE{i}-',justification='r'),
                Combo(material,k=f'-COMBO MATERIAL{i}-'), I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT MATERIAL{i}-',justification='r'),
                ])
            
        layout.append(
            [Create_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        )
        window = sg.Window('Create norm',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        # window['-INPUT-'].bind("<Return>", "_Enter")
        # self.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,ESCAPE]:
                break
            
            if event in [f'-COMBO WORKER{i}-' for i in range(10)]:
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-']:
                        window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                        
            if event in [f'-COMBO MACHINE{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MACHINE{i}-']:
                        window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)
                        
            if event in [f'-COMBO MATERIAL{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MATERIAL{i}-']:
                        window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit) 
                              
            if event in [Create_btn.key] and values[id_in.key]:

                self.foward('norm do create', id=values[id_in.key],name=values[name_in.key],unit=values[unit_in.key])
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                        self.foward('worker norm do create', id_norm=values[id_in.key],id=values[f'-COMBO WORKER{i}-'].id,amount=values[f'-INPUT WORKER{i}-'])
                        
                    if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                        self.foward('machine norm do create', id_norm=values[id_in.key],id=values[f'-COMBO MACHINE{i}-'].id,amount=values[f'-INPUT MACHINE{i}-'])
                        
                    if values[f'-COMBO MATERIAL{i}-']  and values[f'-INPUT MATERIAL{i}-']:
                        self.foward('material norm do create', id_norm=values[id_in.key],id=values[f'-COMBO MATERIAL{i}-'].id,amount=values[f'-INPUT MATERIAL{i}-'])

            if event == clear_btn.key:
                for key in [id_in.key,name_in.key,unit_in.key]:
                    window[key].update('')
        window.close()

class norm_edit_view(base_view):
    def Render(self):
        def get_worker_amount(id,item_norm):
            return Enumerable(item_norm).where(lambda x: x.id == id).to_list()[0].amount
        
        def get_machine_amount(id,item_norm):
            return Enumerable(item_norm).where(lambda x: x.id == id).to_list()[0].amount

        def get_material_amount(id,item_norm):
            return Enumerable(item_norm).where(lambda x: x.id == id).to_list()[0].amount 
         
        norm = self.kwargs['norm']
        worker_norm = self.kwargs['worker_norm']
        machine_norm = self.kwargs['machine_norm']
        material_norm = self.kwargs['material_norm']
        
        worker = self.kwargs['worker']
        material = self.kwargs['material']
        machine = self.kwargs['machine']  
              
        workers = self.kwargs['workers']
        materials = self.kwargs['materials']
        machines = self.kwargs['machines']
        
        id_text = Elements.Text('ID',(5,1))
        name_text = Elements.Text('Name',(5,1))
        unit_text = Elements.Text('Unit',(5,1))
        id_in = sg.Input(s=(15,1),expand_x=True,default_text=norm.id,k='-ID IN-')
        name_in = sg.Input(s=(15,1),expand_x=True,default_text=norm.name,k='-NAME IN-')
        unit_in = sg.Input(s=(15,1),expand_x=True,default_text=norm.unit,k='-UNIT IN-')
        
        update_btn = Elements.Button('Update',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [id_text.GUI,id_in],
            [name_text.GUI,name_in],
            [unit_text.GUI,unit_in],
            [Elements.Text('Worker',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Machine',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI,
             Elements.Text('Material',(20,1),justification='c').GUI, Elements.Text('Unit',(7,1),justification='c').GUI, Elements.Text('Amount',(7,1),justification='c').GUI],
        ]        
        
        for i in range(10):
            layout.append([
                Combo(values=workers,s=(20,1),k=f'-COMBO WORKER{i}-',default_value=worker[i] if i <len(worker) else None),
                
                I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True,text_color='black',justification='c',default_text=worker[i].unit if i <len(worker) else None),
                
                I(s=(10,1),k=f'-INPUT WORKER{i}-',default_text=get_worker_amount(worker[i].id,worker_norm) if i <len(worker) else None),
                
                Combo(values=machines,s=(20,1),k=f'-COMBO MACHINE{i}-',default_value=machine[i] if i <len(machine) else None),
                
                I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c',default_text=machine[i].unit if i <len(machine) else None),
                
                sg.I(s=(10,1),k=f'-INPUT MACHINE{i}-',default_text=get_machine_amount(machine[i].id,machine_norm) if i <len(machine) else None),
                
                Combo(values=materials,s=(20,1),k=f'-COMBO MATERIAL{i}-',default_value=material[i] if i <len(material) else None),
              
                I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c',default_text=material[i].unit if i <len(material) else None),
                
                I(s=(10,1),k=f'-INPUT MATERIAL{i}-',default_text=get_material_amount(material[i].id,material_norm) if i <len(material) else None),
                
                ])
            
        layout.append( [update_btn.GUI,clear_btn.GUI,cancel_btn.GUI])
        window = sg.Window('Edit norm',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,ESCAPE]:
                break

            if event in [f'-COMBO WORKER{i}-' for i in range(10)]:
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-']:
                        window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                        
            if event in [f'-COMBO MACHINE{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MACHINE{i}-']:
                        window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)

                        
            if event in [f'-COMBO MATERIAL{i}-' for i in range(10)]:
                for i in range(10):                        
                    if values[f'-COMBO MATERIAL{i}-']:
                        window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit)
            
            elif event in [update_btn.key] and values['-ID IN-']:
                self.foward('norm do update',id=values['-ID IN-'],name=values['-NAME IN-'],unit=values['-UNIT IN-'])
                
                # Xóa những cái worker norm cũ:
                self.foward('worker norm do delete by norm id',id_norm=norm.id)
                self.foward('machine norm do delete by norm id',id_norm=norm.id)
                self.foward('material norm do delete by norm id',id_norm=norm.id)
                
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                        self.foward('worker norm do create',id_norm=values['-ID IN-'],id=values[f'-COMBO WORKER{i}-'].id,amount=values[f'-INPUT WORKER{i}-'])
                        
                    if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                        self.foward('machine norm do create',id_norm=values['-ID IN-'],id=values[f'-COMBO MACHINE{i}-'].id,amount=values[f'-INPUT MACHINE{i}-'])
                        
                    if values[f'-COMBO MATERIAL{i}-']  and values[f'-INPUT MATERIAL{i}-']:
                        self.foward('material norm do create',id_norm=values['-ID IN-'],id=values[f'-COMBO MATERIAL{i}-'].id,amount=values[f'-INPUT MATERIAL{i}-'])
                self.foward('norm list')                                               

            elif event == clear_btn.key:
                for key in ['-NAME IN-','-UNIT IN-']:
                    window[key].update('')
        window.close()
############################################################ WORKER NORM
class WorkerNormUpdateView:
    def Render(self,**kwargs):
        worker_norm = kwargs['worker_norm']
        workers = kwargs['workers']
        worker = Enumerable(workers).where(lambda x: x.id == worker_norm.id).to_list()[0]
        
        layout = [
            [T('ID NORM','-TEXT0-',s=(10,1),justification='c'),T('WORKER','-TEXT1-',s=(30,1),justification='c'),T('UNIT','-TEXT1-',s=(7,1),justification='c'),T('AMOUnT','-TEXT1-',s=(10,1),justification='c')],
            [I(k='-ID NORM-',readonly=True,text_color='black',default_text=worker_norm.id_norm),Combo(workers,s=(30,1),k='-WORKER COMBO-',default_value=worker),I(k='-UNIT-',s=(7,1),readonly=True,text_color='black',default_text=worker.unit,justification='c'),I(k='-AMOUnT-',default_text=worker_norm.amount,justification='r')],
            [sg.Push(),Btn('Update','-UPDATE-'),Btn('Clear','-CLEAR-'),Btn('Cancel','-CANCEL-')]
        ]
        window = sg.Window('Edit worker norm',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            if event == '-WORKER COMBO-' and values['-WORKER COMBO-']:
                window['-UNIT-'].update(values['-WORKER COMBO-'].unit)
            
            if event == '-UPDATE-' and values['-AMOUnT-'] and values['-WORKER COMBO-']:
                request = '''worker norm do update ?
                    id_norm = {} &
                    old_id = {} &
                    id = {} &
                    amount = {}'''.format(values['-ID NORM-'],worker_norm.id,values['-WORKER COMBO-'].id,values['-AMOUnT-'])
                Framework.Route.Foward(request)
                Framework.Route.Foward('norm list')
                
            elif event == '-CLEAR-':
                for key in ['-INPUT-']:
                    window[key].update('')            
        window.close()
############################################################ MACHINE NORM
class MachineNormUpdateView:
    def Render(self,**kwargs):
        machine_norm = kwargs['machine_norm']
        machines = kwargs['machines']
        machine = Enumerable(machines).where(lambda x: x.id == machine_norm.id).to_list()[0]
        
        layout = [
            [T('ID NORM','-TEXT0-',s=(10,1),justification='c'),T('MACHINE','-TEXT1-',s=(30,1),justification='c'),T('UNIT','-TEXT1-',s=(7,1),justification='c'),T('AMOUnT','-TEXT1-',s=(10,1),justification='c')],
            [I(k='-ID NORM-',readonly=True,text_color='black',default_text=machine_norm.id_norm),Combo(machines,s=(30,1),k='-MACHINE COMBO-',default_value=machine),I(k='-UNIT-',s=(7,1),readonly=True,text_color='black',default_text=machine.unit,justification='c'),I(k='-AMOUnT-',default_text=machine_norm.amount,justification='r')],
            [sg.Push(),Btn('Update','-UPDATE-'),Btn('Clear','-CLEAR-'),Btn('Cancel','-CANCEL-')]
        ]
        window = sg.Window('Edit machine norm',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            if event == '-MACHINE COMBO-' and values['-MACHINE COMBO-']:
                window['-UNIT-'].update(values['-MACHINE COMBO-'].unit)
            
            if event == '-UPDATE-' and values['-AMOUnT-'] and values['-MACHINE COMBO-']:
                request = '''machine norm do update ?
                    id_norm = {} &
                    old_id = {} &
                    id = {} &
                    amount = {}'''.format(values['-ID NORM-'],machine_norm.id,values['-MACHINE COMBO-'].id,values['-AMOUnT-'])
                Framework.Route.Foward(request)
                Framework.Route.Foward('norm list')
                
            elif event == '-CLEAR-':
                for key in ['-INPUT-']:
                    window[key].update('')            
        window.close()
############################################################ MATERIAL NORM
class material_norm_update_view:
    def Render(self,**kwargs):
        material_norm = kwargs['material_norm']
        materials = kwargs['materials']
        material = Enumerable(materials).where(lambda x: x.id == material_norm.id).to_list()[0]
        
        layout = [
            [T('ID NORM','-TEXT0-',s=(10,1),justification='c'),T('MATERIAL','-TEXT1-',s=(30,1),justification='c'),T('UNIT','-TEXT1-',s=(7,1),justification='c'),T('AMOUnT','-TEXT1-',s=(10,1),justification='c')],
            [I(k='-ID NORM-',readonly=True,text_color='black',default_text=material_norm.id_norm),Combo(materials,s=(30,1),k='-MATERIAL COMBO-',default_value=material),I(k='-UNIT-',s=(7,1),readonly=True,text_color='black',default_text=material.unit,justification='c'),I(k='-AMOUnT-',default_text=material_norm.amount,justification='r')],
            [sg.Push(),Btn('Update','-UPDATE-'),Btn('Clear','-CLEAR-'),Btn('Cancel','-CANCEL-')]
        ]
        window = sg.Window('Edit material norm',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            if event == '-MATERIAL COMBO-' and values['-MATERIAL COMBO-']:
                window['-UNIT-'].update(values['-MATERIAL COMBO-'].unit)
            
            if event == '-UPDATE-' and values['-AMOUnT-'] and values['-MATERIAL COMBO-']:
                request = '''material norm do update ?
                    id_norm = {} &
                    old_id = {} &
                    id = {} &
                    amount = {}'''.format(values['-ID NORM-'],material_norm.id,values['-MATERIAL COMBO-'].id,values['-AMOUnT-'])
                Framework.Route.Foward(request)
                Framework.Route.Foward('norm list')
                
            elif event == '-CLEAR-':
                for key in ['-INPUT-']:
                    window[key].update('')            
        window.close()
       
class create_norm_from_excel_view(base_view):
    def Render(self):
        # self.window.finalize()
        path = sg.popup_get_file('Please select du toan excel file',title='EXCEL PATH')
        if path:
            requset = f'norm do create from excel ? path = {path}'
            Framework.Route.Foward(requset)
            
############################################################ HANG MUC
class hang_muc_create_view(base_view):
    def Render(self):
        name_text = Elements.Text('Name',(5,1))
        # id_in = sg.Input(s=(30,1),k='-ID IN-',default_text=id,readonly=True,text_color='black',expand_x=True)
        name_in = sg.Input(s=(30,1),k='-NAME IN-',enable_events=True,expand_x=True)
        
        create_btn = Elements.Button('create',(10,1))
        clear_btn =  Elements.Button('Clear',(10,1))   
        cancel_btn = Elements.Button('Cancel',(10,1))    
        
        layout =[
            [name_text.GUI,name_in],
            [create_btn.GUI,clear_btn.GUI,cancel_btn.GUI]
        ]
        window = sg.Window('create hang muc',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window['-NAME IN-'].bind("<Return>", "_Enter")
        window.bind('<Escape>','-ESCAPE-')
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,cancel_btn.key,'-ESCAPE-']:
                break
            elif event in [create_btn.key,'-NAME IN-'+'_Enter']:
                self.foward('hang muc do create',id='HM{}'.format(next(Models.hang_muc.id_iter)),name=values['-NAME IN-'])
                self.foward('work list')
                self.foward('hang muc create')
                break
            elif event == clear_btn.key:
                for key in ['-ID IN-']:
                    window[key].update('')
        window.close()