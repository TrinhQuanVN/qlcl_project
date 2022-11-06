from cgi import print_arguments
import datetime
import Framework
import Extension as ex
import Models
import PySimpleGUI as sg
from py_linq import Enumerable

def Combo(values=[],s=(20,1),k='',default_value=None,enable_event=True,font=('Any',11),expand_x=True):
    return sg.Combo(values=values,s=s,k=k,default_value=default_value,enable_events=enable_event,font=font,expand_x=expand_x)

def I(s=(10,1),k='',default_text='',readonly=False,text_color=None,justification='l',font=('Any',11)):
    return sg.Input(s=s,k=k,default_text=default_text,readonly=readonly,text_color=text_color,justification=justification,font=font)

def T(text='',k='',s=(5,1),justification='r',font=('Any',11)):
    return sg.Text(text=text,s=s, justification=justification, font=font)

def Btn(button_text='',k='',s=(10,1)):
    return sg.Button(button_text=button_text,k=k,s=s)

def layout(text_input:list,input_size=(30,1),buttons:list=[]):
    text_size = (max([len(key) for key in text_input]),1)
    button_size = (max(len(b) for b in buttons),1)
    l = []
    for text in text_input:
        l.append([sg.Text(text,s=text_size),sg.Input(k=f'{text} input',s=input_size)])
    l.append([sg.Button(b, k=b, s=button_size) for b in buttons])
    return l


def window(layout, title, elemnt_bind:dict=None, **kwargs):
    sg.theme('DarkAmber')
    window = sg.Window(title,layout,font=('Any',13),keep_on_top=True,finalize=True, **kwargs)
    if not elemnt_bind:
        return window
    for element, bind in elemnt_bind.items():
        if element:
            window[element].bind(bind[0],bind[1])
        else:
            window.bind(bind[0],bind[1])
    return window 
    
layout_create_ntvl = layout(['name','dateNT'], buttons=['Create','Clear','Cancel'])


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
        Framework.Route.Foward(result.strip()[:-1])

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

def get_amount(id,item_work):
    return Enumerable(item_work).where(lambda x: x.id == id).to_list()[0].amount

def work_create_layout(norm = None, hang_muc = None, phan_viec =None,
                       workers = None, machines = None, materials = None,
                       worker = None, machine = None, material = None,
                       worker_norm = None, machine_norm = None, material_norm = None):
    
    id_text = sg.Text('ID', s=(10,1))
    name_text = sg.Text('Name', s=(10,1))
    unit_text = sg.Text('Unit', s=(10,1))
    amount_text = sg.Text('Amount', s=(10,1))
    start_text = sg.Text('Start', s=(10,1))
    end_text = sg.Text('End', s=(10,1))
    hm_text = sg.Text('Hang mục', s=(10,1))
    pv_text = sg.Text('Phần việc', s=(10,1))
    
    
    # id_in = sg.Input(s=(15,1),k='-ID IN-',expand_x=True,default_text=work_id,readonly=True,text_color='black')
    name_in = sg.Input(s=(15,1),
                       expand_x=True,
                       default_text = norm.name if norm else '',
                       k='-NAME IN-')
    
    unit_in = sg.Input(s=(15,1),
                       expand_x=True,
                       default_text=norm.unit if norm else '',
                       k='-UNIT IN-')
    amount_in = sg.Input(s=(15,1),expand_x=True,k='-AMOUNT IN-',enable_events=True)
    start_in = sg.Input(s=(15,1),expand_x=True,k='-START IN-',enable_events=True)
    end_in = sg.Input(s=(15,1),expand_x=True,k='-END IN-',enable_events=True)
    hm_combo = sg.Combo(hang_muc,k=f'-COMBO HM-',default_value=hang_muc[-1],enable_events=True,font=('Any',11),expand_x=True)
    pv_combo = sg.Combo(phan_viec, k=f'-COMBO PV-',enable_events=True,font=('Any',11),expand_x=True, default_value=phan_viec[-1])
    
    create_btn = sg.Button('Create',s=(10,1),k='-CREATE-')
    clear_btn =  sg.Button('Clear',s=(10,1),k='-CLEAR-')   
    cancel_btn = sg.Button('Cancel',s=(10,1),k='-CANCEL-')    
    
    layout =[
        [hm_text,hm_combo],
        [pv_text,pv_combo],
        [name_text,name_in,sg.Checkbox('NTCV',k='-CheckBox NTCV-',default=True)],
        [unit_text,unit_in],
        [amount_text,amount_in],
        [start_text,start_in],
        [end_text,end_in],
        
        [sg.Text('Worker',s=(20,1),justification='c'),
         sg.Text('Unit',s=(7,1),justification='c'),
         sg.Text('Amount',s=(7,1),justification='c'),
         sg.Text('Machine',s=(20,1),justification='c'),
         sg.Text('Unit',s=(7,1),justification='c'),
         sg.Text('Amount',s=(7,1),justification='c'),
         sg.Text('Material',s=(20,1),justification='c'),
         sg.Text('Unit',s=(7,1),justification='c'),
         sg.Text('Amount',s=(7,1),justification='c')],
            ]

    for i in range(10):
        layout.append([
            Combo(values=workers,
                  s=(20,1),
                  k=f'-COMBO WORKER{i}-',
                  default_value=worker[i] if i <len(worker) else None),
            
            I(s=(7,1),
              k=f'-UNIT WORKER{i}-',
              readonly=True,
              text_color='black',
              justification='c',
              default_text=worker[i].unit if i <len(worker) and worker else None),
            
            I(s=(10,1),
              k=f'-INPUT WORKER{i}-',
              default_text=get_amount(worker[i].id,worker_norm) if i <len(worker) and worker else None),
            
            Combo(values=machines,
                  s=(20,1),
                  k=f'-COMBO MACHINE{i}-',
                  default_value=machine[i] if i <len(machine) and machine else None),
            
            I(s=(7,1),
              k=f'-UNIT MACHINE{i}-',
              readonly=True,
              text_color='black',
              justification='c',
              default_text=machine[i].unit if i <len(machine) and machine else None),
            
            I(s=(10,1),
              k=f'-INPUT MACHINE{i}-',
              default_text=get_amount(machine[i].id,machine_norm) if i <len(machine) and machine else None),
            
            Combo(values=materials,
                  s=(20,1),k=f'-COMBO MATERIAL{i}-',
                  default_value=material[i] if i <len(material) and material else None),
            
            I(s=(7,1),
              k=f'-UNIT MATERIAL{i}-',
              readonly=True,
              text_color='black',
              justification='c',
              default_text=material[i].unit if i <len(material) and material else None),
            
            I(s=(10,1),
              k=f'-INPUT MATERIAL{i}-',
              default_text=get_amount(material[i].id,material_norm) if i <len(material) and material else None),
            ])
        
    layout.append(
        [create_btn,clear_btn,cancel_btn]
    )
    
    return layout

def work_create_windown(title:str,layout):
    pass


class work_create_with_norm_id_view(base_view):
    def Render(self):
        layout = work_create_layout(norm = self.kwargs['norm'],
                                    hang_muc = self.kwargs['hang_muc'],
                                    phan_viec = self.kwargs['phan_viec'],
                                    workers = self.kwargs['workers'],
                                    machines = self.kwargs['machines'],
                                    materials = self.kwargs['materials'],
                                    worker = self.kwargs['worker'],
                                    machine = self.kwargs['machine'],
                                    material = self.kwargs['material'],
                                    worker_norm = self.kwargs['worker_norm'],
                                    machine_norm = self.kwargs['machine_norm'],
                                    material_norm = self.kwargs['material_norm'])
        
        window = sg.Window('Create work',layout,font=('Any',13),keep_on_top=True,finalize=True)
        
        window['-NAME IN-'].bind("<Return>", "_Enter")
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window.bind('<Escape>','-ESCAPE-')
        
        def multi_amount(values=None):
            if not values['-AMOUNT IN-']:
                return
            window['-AMOUNT IN-'].update(round(eval(values['-AMOUNT IN-']),2))
            for i in range(10):
                if values[f'-INPUT WORKER{i}-']:
                    window[f'-INPUT WORKER{i}-'].update(
                        round(eval('{}*{}'.format(
                                                values['-AMOUNT IN-'],
                                                get_amount(values[f'-COMBO WORKER{i}-'].id,
                                                          self.kwargs['worker_norm']))),2))
                    
                if values[f'-INPUT MACHINE{i}-']:
                    window[f'-INPUT MACHINE{i}-'].update(
                        round(eval('{}*{}'.format(
                                                values['-AMOUNT IN-'],
                                                get_amount(values[f'-COMBO MACHINE{i}-'].id,
                                                        self.kwargs['machine_norm']))),2))
                    
                if values[f'-INPUT MATERIAL{i}-']:
                    window[f'-INPUT MATERIAL{i}-'].update(
                        round(eval('{}*{}'.format(
                                                values['-AMOUNT IN-'],
                                                get_amount(values[f'-COMBO MATERIAL{i}-'].id,
                                                        self.kwargs['material_norm']))),2))            
        
        def update_unit(values=None):
            for i in range(10):
                if values[f'-COMBO WORKER{i}-']:
                    window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                    
            for i in range(10):                        
                if values[f'-COMBO MACHINE{i}-']:
                    window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)
                    
            for i in range(10):                        
                if values[f'-COMBO MATERIAL{i}-']:
                    window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit)

        def create_ntcv():
            if window['-CheckBox NTCV-']:
                pass
        def create(values=None):
            work_id = next(Models.work.id_iter)
            if window['-CheckBox NTCV-']:
                ntcv_id = next(Models.ntcv.id_iter)
                self.foward('ntcv do create',
                            name= values['-NAME IN-'],
                            work_id= work_id,
                            dateNT= values['-END IN-'],
                            id =ntcv_id)
            # try:
            #     amount = float(values['-AMOUNT IN-'])
            # except ValueError:
            #     window['-AMOUNT IN-'].set_focus()
            #     return
            self.foward('work do create',
                            id =work_id,
                            name = values['-NAME IN-'],
                            unit = values['-UNIT IN-'],
                            amount = values['-AMOUNT IN-'],
                            hm_id = values['-COMBO HM-'].id,
                            pv_id = values['-COMBO PV-'].id,
                            start = values['-START IN-'],
                            end = values['-END IN-'])
                
            for i in range(10):
                if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                    self.foward('worker work do create',
                                work_id=work_id,
                                id=values[f'-COMBO WORKER{i}-'].id,
                                amount=values[f'-INPUT WORKER{i}-'])
                    
                if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                    self.foward('machine work do create',
                                work_id=work_id,
                                id=values[f'-COMBO MACHINE{i}-'].id,
                                amount=values[f'-INPUT MACHINE{i}-']) 
                    
                if values[f'-COMBO MATERIAL{i}-'] and values[f'-INPUT MATERIAL{i}-']:
                    self.foward('material work do create',
                                work_id=work_id,
                                id=values[f'-COMBO MATERIAL{i}-'].id,
                                amount=values[f'-INPUT MATERIAL{i}-'])                       

            create_ntcv()
            self.foward('work list')
            
            window.close()

        def clear(values=None):
            for key in ['-NAME IN-','-UNIT IN-','-AMOUNT IN-']:
                window[key].update('')

        func = {'-AMOUNT IN-'+'_Enter':multi_amount,
                '-CREATE-':create, '-CLEAR-':clear}
        
        for i in range(10):
            func.update({f'-COMBO WORKER{i}-' : update_unit})
            func.update({f'-COMBO MACHINE{i}-' : update_unit})
            func.update({f'-COMBO MATERIAL{i}-' : update_unit})
            
        while True:
            event, values = window.read()
            if event in [sg.WIN_CLOSED, '-ESCAPE-', '-CANCEL-']:
                break
            
            if event in func:
                func[event](values)
            
        window.close()

class work_create_view(base_view):
    def Render(self):
        layout = work_create_layout(hang_muc = self.kwargs['hang_muc'],
                                    phan_viec = self.kwargs['phan_viec'],
                                    workers = self.kwargs['worker'],
                                    materials = self.kwargs['material'],
                                    machines = self.kwargs['machine'])
  
        window = sg.Window('Create work',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window['-NAME IN-'].bind("<Return>", "_Enter")
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window.bind('<Escape>','-ESCAPE-')

        def multi_amount(values=None):
            if not values['-AMOUNT IN-']:
                return
            window['-AMOUNT IN-'].update(round(eval(values['-AMOUNT IN-']),2))
            
            # for i in range(10):
            #     if values[f'-INPUT WORKER{i}-']:
            #         window[f'-INPUT WORKER{i}-'].update(round(eval('{}*{}'.format(values['-AMOUNT IN-'],get_amount(values[f'-COMBO WORKER{i}-'].id,worker_norm))),2))
                    
            #     if values[f'-INPUT MACHINE{i}-']:
            #         window[f'-INPUT MACHINE{i}-'].update(round(eval('{}*{}'.format(values['-AMOUNT IN-'],get_amount(values[f'-COMBO MACHINE{i}-'].id,machine_norm))),2))
                    
            #     if values[f'-INPUT MATERIAL{i}-']:
            #         window[f'-INPUT MATERIAL{i}-'].update(round(eval('{}*{}'.format(values['-AMOUNT IN-'],get_amount(values[f'-COMBO MATERIAL{i}-'].id,material_norm))),2))            
        
        
        def update_unit(values=None):
            for i in range(10):
                if values[f'-COMBO WORKER{i}-']:
                    window[f'-UNIT WORKER{i}-'].update(values[f'-COMBO WORKER{i}-'].unit)
                    
            for i in range(10):                        
                if values[f'-COMBO MACHINE{i}-']:
                    window[f'-UNIT MACHINE{i}-'].update(values[f'-COMBO MACHINE{i}-'].unit)
                    
            for i in range(10):                        
                if values[f'-COMBO MATERIAL{i}-']:
                    window[f'-UNIT MATERIAL{i}-'].update(values[f'-COMBO MATERIAL{i}-'].unit)
        
        def create(values=None):
            self.foward('work do create',
                            id ='W{}'.format(next(Models.work.id_iter)),
                            name = values['-NAME IN-'],
                            unit = values['-UNIT IN-'],
                            amount = values['-AMOUNT IN-'],
                            hm_id = values['-COMBO HM-'].id,
                            pv_id = values['-COMBO PV-'].id if values['-COMBO PV-'] else '',
                            start = values['-START IN-'],
                            end = values['-END IN-'])
                
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
            window.close()

        def clear(values=None):
            for key in ['-NAME IN-','-UNIT IN-','-AMOUNT IN-']:
                window[key].update('')
        
        func = {'-AMOUNT IN-'+'_Enter':multi_amount, 
                
                '-CREATE-':create, '-CLEAR-':clear}
        
        for i in range(10):
            func.update({f'-COMBO WORKER{i}-':update_unit})
            func.update({f'-COMBO MACHINE{i}-':update_unit})
            func.update({f'-COMBO MATERIAL{i}-':update_unit})        
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            
            if event in func:
                func[event](values)
 
        window.close()

class work_edit_view(base_view):
    def Render(self):
        work = self.kwargs['work']
        hang_muc = self.kwargs['hang_muc']
        phan_viec = self.kwargs['phan_viec']
        hang_mucs = self.kwargs['hang_mucs']
        phan_viecs = self.kwargs['phan_viecs']
            
        worker_work = self.kwargs['worker_work']
        machine_work = self.kwargs['machine_work']
        material_work = self.kwargs['material_work']
        
        workers = self.kwargs['workers'] # all worker
        materials = self.kwargs['materials'] # all material
        machines = self.kwargs['machines'] # all machine
        ori_work_amount = work.amount
        ori_worker_work_amount = [item.amount for item in worker_work] if worker_work else []
        ori_machine_work_amount = [item.amount for item in machine_work] if machine_work else []
        ori_material_work_amount = [item.amount for item in material_work] if material_work else []
        
        layout =[
            [sg.Text('Hạng mục',(10,1)), sg.Combo(hang_mucs,k=f'-COMBO HM-',default_value= hang_muc, expand_x=True)],
            [sg.Text('Phần việc',(10,1)), sg.Combo(phan_viecs,k=f'-COMBO PV-',default_value= phan_viec, expand_x=True)],
            [sg.Text('ID',(10,1)), sg.Input(s=(15,1),expand_x=True,default_text=work.id,k='-ID IN-')],
            [sg.Text('Name',(10,1)), sg.Input(s=(15,1),expand_x=True,default_text=work.name,k='-NAME IN-')],
            [sg.Text('Unit',(10,1)), sg.Input(s=(15,1),expand_x=True,default_text=work.unit,k='-UNIT IN-')],
            [sg.Text('Amount',(10,1)), sg.Input(s=(15,1),expand_x=True,k='-AMOUNT IN-',enable_events=True, default_text=work.amount)],
            [sg.Text('Start',(10,1)), sg.Input(s=(15,1),expand_x=True,k='-START IN-',enable_events=True, default_text=work.start)],
            [sg.Text('End',(10,1)), sg.Input(s=(15,1),expand_x=True,k='-END IN-',enable_events=True, default_text=work.end)],
            [sg.Text('Worker',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c'),
             sg.Text('Machine',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c'),
             sg.Text('Material',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c')],
        ]        
        
        for i in range(10):
            layout.append([
                sg.Combo(values=workers,s=(20,1),k=f'-COMBO WORKER{i}-'),
                I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True, text_color='black',justification='c'),
                I(s=(10,1),k=f'-INPUT WORKER{i}-'),
                Combo(values=machines,s=(20,1),k=f'-COMBO MACHINE{i}-'),
                I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c'),
                sg.I(s=(10,1),k=f'-INPUT MACHINE{i}-'),
                sg.Combo(values=materials,s=(20,1),k=f'-COMBO MATERIAL{i}-'),
                I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c'),
                I(s=(10,1),k=f'-INPUT MATERIAL{i}-'),
                ])
            
        layout.append( [sg.Push(),
                        sg.Button('Update',s=(15,1), key= 'update'),
                        sg.Button('Clear',s=(15,1), key= 'clear'),
                        sg.Button('Cancel',s=(15,1), key= 'cancel'),])
        window = sg.Window('Edit work', layout, font=('Any',13), keep_on_top=True, finalize=True)
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window['-AMOUNT IN-'].bind("<Return>", "_Enter")
        window['-AMOUNT IN-'].bind('<FocusOut>', '_INPUT FocusOut')
        window.bind(KEYCAP_ESC,ESCAPE)
        
        if worker_work:
            for i, item in enumerate(worker_work):
                worker = Enumerable(workers).where(lambda x: x.id == item.id).to_list()[0]
                window[f'-COMBO WORKER{i}-'].update(worker)
                window[f'-UNIT WORKER{i}-'].update(worker.unit)
                window[f'-INPUT WORKER{i}-'].update(item.amount)
        if machine_work:
            for i, item in enumerate(machine_work):
                machine = Enumerable(machines).where(lambda x: x.id == item.id).to_list()[0]
                window[f'-COMBO MACHINE{i}-'].update(machine)
                window[f'-UNIT MACHINE{i}-'].update(machine.unit)
                window[f'-INPUT MACHINE{i}-'].update(item.amount)  
        if material_work:
            print('trịnh',material_work)
            for i, item in enumerate(material_work):
                material = Enumerable(materials).where(lambda x: x.id == item.id).to_list()[0]
                window[f'-COMBO MATERIAL{i}-'].update(material)
                window[f'-UNIT MATERIAL{i}-'].update(material.unit)
                window[f'-INPUT MATERIAL{i}-'].update(item.amount)
                        
        while True:
            event,values = window.read()
            print(event)
            
            if event in [sg.WIN_CLOSED,'cancel',ESCAPE]:
                break

            if event in ['-AMOUNT IN-'+'_Enter','-AMOUNT IN-'+'_INPUT FocusOut'] and  values['-AMOUNT IN-']:
                window['-AMOUNT IN-'].update(eval(values['-AMOUNT IN-']))
                new_work_amount = values['-AMOUNT IN-']
                if ori_worker_work_amount:
                    for i, amount in enumerate(ori_worker_work_amount):
                        window[f'-INPUT WORKER{i}-'].update(round(eval('{}*{}/{}'.format(new_work_amount,amount,ori_work_amount)),2))
                if ori_machine_work_amount:
                    for i, amount in enumerate(ori_machine_work_amount):
                        window[f'-INPUT MACHINE{i}-'].update(round(eval('{}*{}/{}'.format(new_work_amount,amount,ori_work_amount)),2))
                if ori_material_work_amount:
                    for i, amount in enumerate(ori_material_work_amount):
                        window[f'-INPUT MATERIAL{i}-'].update(round(eval('{}*{}/{}'.format(new_work_amount,amount,ori_work_amount)),2))                                        
                window['-START IN-'].set_focus()
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
            
            if event in ['update'] and values['-ID IN-']:
                self.foward('work do update',
                            id = values['-ID IN-'],
                            name = values['-NAME IN-'],
                            unit = values['-UNIT IN-'],
                            amount = values['-AMOUNT IN-'],
                            hm_id = values['-COMBO HM-'].id,
                            pv_id = values['-COMBO PV-'].id,
                            start = values['-START IN-'],
                            end = values['-END IN-'])
                
                # Xóa những cái worker work cũ:
                self.foward('worker work do delete', work_id=work.id, id= '')
                self.foward('machine work do delete', work_id=work.id, id= '')
                self.foward('material work do delete', work_id=work.id, id= '')
                
                for i in range(10):
                    if values[f'-COMBO WORKER{i}-'] and values[f'-INPUT WORKER{i}-']:
                        self.foward('worker work do create',
                                    work_id = values['-ID IN-'],
                                    id = values[f'-COMBO WORKER{i}-'].id,
                                    amount = values[f'-INPUT WORKER{i}-'])
                    if values[f'-COMBO MACHINE{i}-'] and values[f'-INPUT MACHINE{i}-']:
                        self.foward('machine work do create',
                                    work_id = values['-ID IN-'],
                                    id = values[f'-COMBO MACHINE{i}-'].id,
                                    amount = values[f'-INPUT MACHINE{i}-'])
                    if values[f'-COMBO MATERIAL{i}-']  and values[f'-INPUT MATERIAL{i}-']:
                        self.foward('material work do create',
                                    work_id = values['-ID IN-'],
                                    id = values[f'-COMBO MATERIAL{i}-'].id,
                                    amount = values[f'-INPUT MATERIAL{i}-'])                                               
                break                                              

            if event == 'clear':
                for key in ['-NAME IN-','-UNIT IN-']:
                    window[key].update('')
        window.close()

############################################################ WORKER
class worker_update_view(base_view):
    def Render(self):
        id_text = sg.Text('ID',(5,1))
        name_text = sg.Text('Name',(5,1))
        unit_text = sg.Text('Unit',(5,1))
        id_in = sg.Input((15,1))
        name_in = sg.Input((15,1))
        unit_in = sg.Input((15,1))
        
        update_btn = sg.Button('Update',(10,1))
        clear_btn =  sg.Button('Clear',(10,1))   
        cancel_btn = sg.Button('Cancel',(10,1))    
        
        layout =[
            [id_text,id_in],
            [name_text,name_in],
            [unit_text,unit_in],
            [update_btn,clear_btn,cancel_btn]
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
        id_text = sg.Text('ID',(5,1))
        name_text = sg.Text('Name',(5,1))
        unit_text = sg.Text('Unit',(5,1))
        id_in = sg.Input((15,1))
        name_in = sg.Input((15,1))
        unit_in = sg.Input((15,1))
        
        update_btn = sg.Button('Update',(10,1))
        clear_btn =  sg.Button('Clear',(10,1))   
        cancel_btn = sg.Button('Cancel',(10,1))    
        
        layout =[
            [id_text,id_in],
            [name_text,name_in],
            [unit_text,unit_in],
            [update_btn,clear_btn,cancel_btn]
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
        id_text = sg.Text('ID',(5,1))
        name_text = sg.Text('Name',(5,1))
        unit_text = sg.Text('Unit',(5,1))
        id_in = sg.Input((15,1))
        name_in = sg.Input((15,1))
        unit_in = sg.Input((15,1))
        
        update_btn = sg.Button('Update',(10,1))
        clear_btn =  sg.Button('Clear',(10,1))   
        cancel_btn = sg.Button('Cancel',(10,1))    
        
        layout =[
            [id_text,id_in],
            [name_text,name_in],
            [unit_text,unit_in],
            [update_btn,clear_btn,cancel_btn]
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
        
        id_text = sg.Text('ID',(5,1))
        name_text = sg.Text('Name',(5,1))
        unit_text = sg.Text('Unit',(5,1))
        id_in = sg.Input((15,1))
        name_in = sg.Input((15,1))
        unit_in = sg.Input((15,1))
        
        Create_btn = sg.Button('Create',(10,1))
        clear_btn =  sg.Button('Clear',(10,1))   
        cancel_btn = sg.Button('Cancel',(10,1))    
        
        layout =[
            [id_text,id_in],
            [name_text,name_in],
            [unit_text,unit_in],
            [sg.Text('Worker',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c'),
             sg.Text('Machine',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c'),
             sg.Text('Material',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c')],
        ]
        for i in range(10):
            layout.append([
                Combo(worker,k=f'-COMBO WORKER{i}-'), I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT WORKER{i}-',justification='r'),
                Combo(machine,k=f'-COMBO MACHINE{i}-'), I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT MACHINE{i}-',justification='r'),
                Combo(material,k=f'-COMBO MATERIAL{i}-'), I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c'), I(s=(7,1),k=f'-INPUT MATERIAL{i}-',justification='r'),
                ])
            
        layout.append(
            [Create_btn,clear_btn,cancel_btn]
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
        def get_amount(id,item_norm):
            return Enumerable(item_norm).where(lambda x: x.id == id).to_list()[0].amount
        
        def get_amount(id,item_norm):
            return Enumerable(item_norm).where(lambda x: x.id == id).to_list()[0].amount

        def get_amount(id,item_norm):
            return Enumerable(item_norm).where(lambda x: x.id == id).to_list()[0].amount 
         
        norm = self.kwargs['norm']
        worker_norm = self.kwargs['worker_norm']
        machine_norm = self.kwargs['machine_norm']
        material_norm = self.kwargs['material_norm']
        
        # worker = self.kwargs['worker']
        # material = self.kwargs['material']
        # machine = self.kwargs['machine']  
              
        workers = self.kwargs['workers']
        materials = self.kwargs['materials']
        machines = self.kwargs['machines']
        
        layout =[
            [sg.Text('ID',(7,1)), sg.Input(s=(15,1),expand_x=True,default_text=norm.id,k='-ID IN-')],
            [sg.Text('Name',(7,1)), sg.Input(s=(15,1),expand_x=True,default_text=norm.name,k='-NAME IN-')],
            [sg.Text('Unit',(7,1)), sg.Input(s=(15,1),expand_x=True,default_text=norm.unit,k='-UNIT IN-')],
            [sg.Text('Worker',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c'),
             sg.Text('Machine',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c'),
             sg.Text('Material',(20,1),justification='c'), sg.Text('Unit',(7,1),justification='c'), sg.Text('Amount',(7,1),justification='c')],
        ]        
        
        for i in range(10):
            layout.append([
                Combo(values=workers,s=(20,1),k=f'-COMBO WORKER{i}-'),
                
                I(s=(7,1),k=f'-UNIT WORKER{i}-',readonly=True, text_color='black',justification='c'),
                
                I(s=(10,1),k=f'-INPUT WORKER{i}-'),
                
                Combo(values=machines,s=(20,1),k=f'-COMBO MACHINE{i}-'),
                
                I(s=(7,1),k=f'-UNIT MACHINE{i}-',readonly=True,text_color='black',justification='c'),
                
                sg.I(s=(10,1),k=f'-INPUT MACHINE{i}-'),
                
                Combo(values=materials,s=(20,1),k=f'-COMBO MATERIAL{i}-'),
              
                I(s=(7,1),k=f'-UNIT MATERIAL{i}-',readonly=True,text_color='black',justification='c'),
                
                I(s=(10,1),k=f'-INPUT MATERIAL{i}-'),
                
                ])                
            
        layout.append( [sg.Push(),
                        sg.Button('Update',s= (12,1), k= 'update'),
                        sg.Button('Clear',s= (12,1), k= 'clear'),
                        sg.Button('Cancel',s= (12,1), k= 'cancel')])
        
        window = sg.Window('Edit norm',layout,font=('Any',13),keep_on_top=True,finalize=True)
        window.bind('<Escape>','-ESCAPE-')
        
        if worker_norm:
            for i, item in enumerate(worker_norm):
                worker = Enumerable(workers).where(lambda x: x.id == item.id).to_list()[0]
                window[f'-COMBO WORKER{i}-'].update(worker)
                window[f'-UNIT WORKER{i}-'].update(worker.unit)
                window[f'-INPUT WORKER{i}-'].update(item.amount)
        if machine_norm:
            for i, item in enumerate(machine_norm):
                machine = Enumerable(machines).where(lambda x: x.id == item.id).to_list()[0]
                window[f'-COMBO MACHINE{i}-'].update(machine)
                window[f'-UNIT MACHINE{i}-'].update(machine.unit)
                window[f'-INPUT MACHINE{i}-'].update(item.amount)  
        if material_norm:
            for i, item in enumerate(material_norm):
                material = Enumerable(materials).where(lambda x: x.id == item.id).to_list()[0]
                window[f'-COMBO MATERIAL{i}-'].update(material)
                window[f'-UNIT MATERIAL{i}-'].update(material.unit)
                window[f'-INPUT MATERIAL{i}-'].update(item.amount)              
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'cancel',ESCAPE]:
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
            
            elif event in ['update'] and values['-ID IN-']:
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

            elif event == 'clear':
                for key in ['-NAME IN-','-UNIT IN-']:
                    window[key].update('')
        window.close()
############################################################ WORKER NORM
class worker_norm_update_view:
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
class machine_norm_update_view:
    def Render(self,**kwargs):
        machine_norm = kwargs['machine_norm']
        machines = kwargs['machines']
        machine = Enumerable(machines).where(lambda x: x.id == machine_norm.id).to_list()[0]
        
        layout = [
            [T('ID NORM','-TEXT0-',s=(10,1),justification='c'), T('MACHINE','-TEXT1-',s=(30,1),justification='c'), T('UNIT','-TEXT1-',s=(7,1),justification='c'),T('AMOUnT','-TEXT1-',s=(10,1),justification='c')],
            [I(k='-ID NORM-',readonly=True,text_color='black',default_text=machine_norm.id_norm), Combo(machines,s=(30,1),k='-MACHINE COMBO-',default_value=machine),I(k='-UNIT-',s=(7,1),readonly=True,text_color='black',default_text=machine.unit,justification='c'),I(k='-AMOUnT-',default_text=machine_norm.amount,justification='r')],
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
            
            if event == '-UPDATE-' and values['-AMOUNT-'] and values['-MATERIAL COMBO-']:
                request = '''material norm do update ?
                    id_norm = {} &
                    old_id = {} &
                    id = {} &
                    amount = {}'''.format(values['-ID NORM-'],material_norm.id,values['-MATERIAL COMBO-'].id,values['-AMOUnT-'])
                Framework.Route.Foward(request)
                Framework.Route.Foward('norm list')
                break
                
            elif event == '-CLEAR-':
                for key in ['-INPUT-']:
                    window[key].update('')            
        window.close()
       
class create_norm_from_excel_view(base_view):
    def Render(self):
        # self.window.finalize()
        path = sg.popup_get_file('Please select du toan excel file',title='EXCEL PATH')
        if path:
            requset = f'norm do create from excel ? path={path}'
            Framework.Route.Foward(requset)
            
############################################################ HANG MUC
def layout_to_create_hang_muc():
    name_text = sg.Text('Name',s=(5,1))
    name_in = sg.Input(s=(30,1),k='-NAME IN-',enable_events=True,expand_x=True)

    create_btn = sg.Button('create',s=(10,1),k='-CREATE-')
    clear_btn =  sg.Button('Clear',s=(10,1),k='-CLEAR-')   
    cancel_btn = sg.Button('Cancel',s=(10,1),k='-CANCEL-')    
    
    layout =[
        [name_text,name_in],
        [create_btn,clear_btn,cancel_btn]
    ]    
    
    return layout

def general_window(layout, title, elemnt_bind:dict=None):
    window = sg.Window(title,layout,font=('Any',13),keep_on_top=True,finalize=True)
    if not elemnt_bind:
        return window
    for element, bind in elemnt_bind.items():
        if element:
            window[element].bind(bind[0],bind[1])
        else:
            window.bind(bind[0],bind[1])
    return window 

class hang_muc_create_view(base_view):
    def Render(self):
        window = general_window(layout= layout_to_create_hang_muc(),
                                title= 'Create hạng mục',
                                elemnt_bind= {'' : ['<Escape>','-ESCAPE-'],
                                              '-NAME IN-' : ["<Return>", "_Enter"]})
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            elif event in ['-CREATE-','-NAME IN-'+'_Enter']:
                self.foward('hang muc do create', 
                            id='{}'.format(next(Models.hang_muc.id_iter)),name=values['-NAME IN-'])
                # self.foward('work list')
                break
            elif event == '-CLEAR-':
                for key in ['-ID IN-']:
                    window[key].update('')
        window.close()
        
class phan_viec_create_view(base_view):
    def Render(self):
        window = general_window(layout= layout_to_create_hang_muc(),
                                title= 'Create phần việc',
                                elemnt_bind= {'' : ['<Escape>','-ESCAPE-'],
                                              '-NAME IN-' : ["<Return>", "_Enter"]})        
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            elif event in ['-CREATE-','-NAME IN-'+'_Enter']:
                self.foward('hphan viec do create', 
                            id='{}'.format(next(Models.hang_muc.id_iter)),name=values['-NAME IN-'])
                # self.foward('work list')
                break
            elif event == '-CLEAR-':
                for key in ['-ID IN-']:
                    window[key].update('')
        window.close()
        
############################################################ LMTN
def layout_text_input(text, input_key, text_size=(7,1), input_size= (50,1), input_en_event=False):
    return [sg.Text(text,s=text_size),
            sg.Input(s=input_size, k=input_key, enable_events= input_en_event, expand_x=True)]


class lmtn_choose_default(base_view):
    def Render(self):
        dateNT = self.kwargs['dateNT']
        default_lmtn = self.kwargs['default']
        # d = dict(zip([item.name for item in default_lmtn], [item.id for item in default_lmtn]))
        layout= [
            [sg.Listbox(values= default_lmtn,
                        size=(50,20),
                        k='-LB-',
                        font=('Any' , 11),
                        enable_events=True,
                        bind_return_key=True)],
            
            [sg.Button('Choose',s=(10,1),k='-CHOOSE-'),
             sg.Button('Cancel',s=(10,1),k='-CANCEL-')]
        ]
        window = general_window(layout= layout,
                                title= 'Choose default LMTN',
                                elemnt_bind= {'' : ['<Escape>','-ESCAPE-'],
                                              '-LB-' : ["<Return>", "_Enter"]})            

        while True:
            event, values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                self.foward('lmtn create without default', dateNT = dateNT)
                break
            elif event in ['-CHOOSE-','-LB-'+'_Enter']:
                self.foward('lmtn create with default', default_id= values['-LB-'][0].id, dateNT = dateNT)

                break
        window.close()

class lmtn_create_with_default_view(base_view):
    def Render(self):
        dateNT = self.kwargs['dateNT']
        default = self.kwargs['default']
        layout =[
            # [sg.Combo(default_dict.keys(),s=(20,1),expand_x=True,k='-COMBO-',enable_events=True)],
            layout_text_input('Name','-NAME IN-'),
            # layout_text_input('Work ID','-WORK ID IN-'),
            # layout_text_input('Work ID','-WORK ID IN-'),
            layout_text_input('DateNT','-DATENT IN-'),
            # layout_text_input('DateYC','-WORK ID IN-'),
            layout_text_input('SLTM','-SLTM IN-'),
            layout_text_input('SLM','-SLM IN-'),
            layout_text_input('KTM','-KTM IN-'),
            layout_text_input('YC','-YC IN-'),
            
            [sg.Button('Create',s=(10,1),k='-CREATE-'),
             sg.Button('Clear',s=(10,1),k='-CLEAR-'),
             sg.Button('Cancel',s=(10,1),k='-CANCEL-')]
        ]        
        
        
        window = general_window(layout= layout,
                                title= 'Create LMTN',
                                elemnt_bind= {'' : ['<Escape>','-ESCAPE-'],})
        
        window['-NAME IN-'].update(default.name)
        window['-SLTM IN-'].update(default.sltm)
        window['-SLM IN-'].update(default.slm)
        window['-KTM IN-'].update(default.ktm)
        window['-YC IN-'].update(default.yc)
        window['-DATENT IN-'].update(dateNT)
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'-CANCEL-','-ESCAPE-']:
                break
            elif event in ['-CREATE-','-NAME IN-'+'_Enter']:
                id = next(Models.lmtn.id_iter)
                self.foward('lmtn do create',
                            name = values['-NAME IN-'],
                            sltm = values['-SLTM IN-'],
                            slm = values['-SLM IN-'],
                            ktm = values['-KTM IN-'],
                            yc = values['-YC IN-'],
                            dateNT = values['-DATENT IN-'],
                            id=id)
                # self.foward('work list')
                break
            elif event == '-CLEAR-':
                for key in ['-ID IN-']:
                    window[key].update('')
        window.close()
        
class ntvl_create_view(base_view):
    def Render(self):
        window = general_window(layout= layout_create_ntvl,
                                title= 'Create NTVL',
                                elemnt_bind= {'' : ['<Escape>','-ESCAPE-'],
                                              'name input' : ["<Return>", "_Enter"]})        
        if not self.kwargs:
            while True:
                event,values = window.read()
                if event in [sg.WIN_CLOSED,'Cancel','-ESCAPE-']:
                    break
                elif event in ['Create']:
                    self.foward('ntvl do create', 
                                id= next(Models.ntvl.id_iter),
                                name= values['name input'],
                                dateNT= values['dateNT input'],)
                    break
                elif event == 'Clear':
                    for key in ['name input','dateNT input']:
                        window[key].update('')
            window.close()
            
        work = self.kwargs['work']
        window['name input'].update(work.name)
        window['dateNT input'].update(work.start)
        
        while True:
            event,values = window.read()
            if event in [sg.WIN_CLOSED,'Cancel','-ESCAPE-']:
                break
            elif event in ['Create']:
                self.foward('ntvl do create', 
                            id='{}'.format(next(Models.ntvl.id_iter)),
                            name= values['name input'],
                            dateNT= values['dateNT input'],)
                break
            elif event == 'Clear':
                for key in ['name','dateNT','dateYC']:
                    window[key].update('')
        window.close()
          