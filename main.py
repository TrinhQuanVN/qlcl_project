import datetime
from random import randint
from py_linq import Enumerable
import Extension as ex
import Models
import Controllers
import DataAccess
import Repository
from Framework import Extension, Parameter,Route
from GUI import GUI
import PySimpleGUI as sg
################################################### GUI #######################################
window = GUI()
context = DataAccess.data_access(path='')
repo = Repository.base_repository(context)
controller = Controllers.base_controller(repo,window)



def to_machine(parameter:Parameter):
    id = parameter['id']
    name = parameter['name']
    unit = parameter['unit']
    return Models.machine(id,name,unit)

def to_material(parameter:Parameter):
    id = parameter['id']
    name = parameter['name']
    unit = parameter['unit']
    return Models.material(id,name,unit)

def to_worker(parameter:Parameter):
    id = parameter['id']
    name = parameter['name']
    unit = parameter['unit']
    return Models.worker(id,name,unit)

def to_norm(parameter:Parameter):
    id = parameter['id']
    name = parameter['name']
    unit = parameter['unit']
    return Models.norm(id,name,unit)

def to_worker_norm(parameter:Parameter):
    id1 = parameter['norm_id']
    id2 = parameter['id']
    amount = parameter['amount']
    return Models.worker_norm(id1,id2,amount)

def to_machine_norm(parameter:Parameter):
    id1 = parameter['norm_id']
    id2 = parameter['id']
    amount = parameter['amount']
    return Models.machine_norm(id1,id2,amount)

def to_material_norm(parameter:Parameter):
    id1 = parameter['norm_id']
    id2 = parameter['id']
    amount = parameter['amount']
    return Models.material_norm(id1,id2,amount)

def to_work(parameter:Parameter):
    id = parameter['id']
    name = parameter['name']
    unit = parameter['unit']
    amount = float(parameter['amount']) if parameter['amount'] else 0
    hm_id = parameter['hm_id']
    start = datetime.datetime.strptime(parameter['start'],r'%d/%m/%y') if parameter['start'] in parameter else None
    end = datetime.datetime.strptime(parameter['end'],r'%d/%m/%y') if parameter['end'] in parameter else None
    
    return Models.work(name,unit,amount,hm_id,start,end,id)

def to_worker_work(parameter:Parameter):
    id1 = parameter['work_id']
    id2 = parameter['id']
    amount = parameter['amount']
    return Models.worker_work(id1,id2,amount)

def to_machine_work(parameter:Parameter):
    id1 = parameter['work_id']
    id2 = parameter['id']
    amount = parameter['amount']
    return Models.machine_work(id1,id2,amount)

def to_material_work(parameter:Parameter):
    id1 = parameter['work_id']
    id2 = parameter['id']
    amount = parameter['amount']
    return Models.material_work(id1,id2,amount)

def to_hang_muc(parameter:Parameter):
    id = parameter['id']
    name = parameter['name']
    return Models.hang_muc(name,id)

def to_work_time(parameter:Parameter) -> Models.work_time:
    work_id = parameter['work_id']
    start = datetime.datetime.strptime(parameter['start'],r'%d/%m/%y') if 'start' in parameter else None
    end = datetime.datetime.strptime(parameter['end'],r'%d/%m/%y') if 'end' in parameter else None
    return Models.work_time(work_id,start,end)    

def to_worker_work_time(parameter:Parameter) -> Models.worker_work_time:
    work_id = parameter['work_id']
    id = parameter['id']
    amount = parameter['amount']
    date = datetime.datetime.strptime(parameter['date'],r'%d/%m/%y')
    return Models.worker_work_time(work_id,id,amount,date)

def event_tree_click_set_meta_data(window,**kwargs):
    window[kwargs['key']].metadata = kwargs['value']

def get_metadata(window,key):
    return window[key].metadata

def register():
#################################################### worker work time
    Route.Register('worker work time do create by work time',lambda p: controller.create_worker_work_time_by_work_time(to_work_time(p)))
    Route.Register('worker work time do delete by work id',lambda p: controller.delete_worker_work_by_work_id(p['work_id']))
    
#################################################### work time
    Route.Register('work time do delete by work id',lambda p: controller.delete_work_time(p['work_id']))
    Route.Register('work time do create',lambda p: controller.create_work_time(to_work_time(p)))
    Route.Register('work time list',controller.list_work_time)
    Route.Register('work time draw',controller.draw_work_time)
    Route.Register('work time update',lambda p: controller.edit_wrok_time(work_id=p['work_id']))
    Route.Register('work time do update',lambda p: controller.edit_wrok_time(work_id=p['work_id'],model=to_work_time(p)))
    
#################################################### HANG MUC
    Route.Register('file cons save', controller.save_file)
    Route.Register('file cons do save',lambda p: controller.save_file(p['path']))
    Route.Register('file cons load', controller.load_file)
    Route.Register('file cons do load',lambda p: controller.load_file(p['path']))
    
    
#################################################### HANG MUC
    Route.Register('hang muc create', controller.create_hang_muc)
    Route.Register('hang muc do create', lambda p: controller.create_hang_muc(to_hang_muc(p)))
#################################################### work
    Route.Register('work create', controller.create_work)
    Route.Register('work do create',lambda p: controller.create_work(model=to_work(p)))
    Route.Register('work create with norm id', lambda p: controller.create_work(p['id']))
    Route.Register('work list',controller.list_work)    
    Route.Register('work do list',lambda p: controller.list_work(p['key']))  
    
    Route.Register('work count',controller.count_work)
    Route.Register('work do count',lambda p: controller.count_work(p['count']))

    Route.Register('work edit',lambda p: controller.edit_work(p['id']))  
    Route.Register('work do edit',lambda p: controller.edit_work(p['id'],to_work(p)))  
    Route.Register('work do delete',lambda p: controller.delete_work(p['id']))
    Route.Register('work create copy',lambda p: controller.create_copy_work(p['id']))

#################################################### worker work    
    Route.Register('worker work do create',lambda p: controller.create_worker_work(to_worker_work(p)))
    Route.Register('worker work do delete by work id',lambda p: controller.delete_worker_work_by_work_id(p['work_id']))
    Route.Register('worker work do delete',lambda p: controller.delete_worker_work(p['work_id'],p['id']))
    Route.Register('worker work update',lambda p: controller.update_worker_work(p['work_id'],p['id']))
    Route.Register('worker work do update',lambda p: controller.update_worker_work(p['work_id'],p['old_id'],to_worker_work(p)))
#################################################### machine work    
    Route.Register('machine work do create',lambda p: controller.create_machine_work(to_machine_work(p)))
    Route.Register('machine work do delete by work id',lambda p: controller.delete_machine_work_by_work_id(p['work_id']))
    Route.Register('machine work do delete',lambda p: controller.delete_machine_work(p['work_id'],p['id']))
    Route.Register('machine work update',lambda p: controller.update_machine_work(p['work_id'],p['id']))
    Route.Register('machine work do update',lambda p: controller.update_machine_work(p['work_id'],p['old_id'],to_machine_work(p)))
#################################################### material work    
    Route.Register('material work do create',lambda p: controller.create_material_work(to_material_work(p)))
    Route.Register('material work do delete by work id',lambda p: controller.delete_material_work_by_work_id(p['work_id']))
    Route.Register('material work do delete',lambda p: controller.delete_material_work(p['work_id'],p['id']))
    Route.Register('material work update',lambda p: controller.update_material_work(p['work_id'],p['id']))
    Route.Register('material work do update',lambda p: controller.update_material_work(p['work_id'],p['old_id'],to_material_work(p))) 
      
#################################################### norm    
    Route.Register('norm create', controller.create_norm)
    Route.Register('norm do create',lambda p: controller.create_norm(to_norm(p)))
    Route.Register('norm list',controller.list_norm)    
    Route.Register('norm do list',lambda p: controller.list_norm(p['key'])) 
    Route.Register('norm do create from excel',lambda p: controller.create_from_excel(p['path']))
    Route.Register('norm create from excel',controller.create_from_excel)
    Route.Register('norm count',controller.count_norm)
    Route.Register('norm do count',lambda p: controller.count_norm(p['count']))  
    Route.Register('norm edit',lambda p: controller.edit_norm(p['id']))  
    Route.Register('norm do edit',lambda p: controller.edit_norm(p['id'],to_norm(p)))  
    Route.Register('norm do delete',lambda p: controller.delete_norm(p['id']))
    Route.Register('norm create copy',lambda p: controller.create_copy_norm(p['id']))
    
#################################################### workER norm    
    Route.Register('worker norm do create',lambda p: controller.create_worker_norm(to_worker_norm(p)))
    Route.Register('worker norm do delete by norm id',lambda p: controller.delete_by_norm_id(p['norm_id']))
    Route.Register('worker norm do delete',lambda p: controller.delete_worker_norm(p['norm_id'],p['id']))
    Route.Register('worker norm update',lambda p: controller.update_worker_norm(p['norm_id'],p['id']))
    Route.Register('worker norm do update',lambda p: controller.update_worker_norm(p['norm_id'],p['old_id'],to_worker_norm(p)))
   
#################################################### machine norm   
    Route.Register('machine norm do create',lambda p: controller.create_machine_norm(to_machine_norm(p)))
    Route.Register('machine norm do delete by norm id',lambda p: controller.delete_by_norm_id(p['norm_id']))
    Route.Register('machine norm do delete',lambda p: controller.delete_machine_norm(p['norm_id'],p['id']))
    Route.Register('machine norm update',lambda p: controller.update_machine_norm(p['norm_id'],p['id']))
    Route.Register('machine norm do update',lambda p: controller.update_machine_norm(p['norm_id'],p['old_id'],to_machine_norm(p)))
        
#################################################### material norm    
    Route.Register('material norm do create',lambda p: controller.create_material_norm(to_material_norm(p)))
    Route.Register('material norm do delete by norm id',lambda p: controller.delete_by_norm_id(p['norm_id']))
    Route.Register('material norm do delete',lambda p: controller.delete_material_norm(p['norm_id'],p['id']))
    Route.Register('material norm update',lambda p: controller.update_material_norm(p['norm_id'],p['id']))
    Route.Register('material norm do update',lambda p: controller.update_material_norm(p['norm_id'],p['old_id'],to_material_norm(p)))
        
#################################################### workER    
    Route.Register('worker create', controller.create_worker)
    Route.Register('worker do create',lambda p: controller.create_worker(to_worker(p)))
    Route.Register('worker list',controller.list_worker)
    Route.Register('worker do list',lambda p: controller.list_worker(p['key']))   
    Route.Register('worker count',controller.count_worker)
    Route.Register('worker do count',lambda p: controller.count_worker(p['count'])) 
      
#################################################### machine   
    Route.Register('machine create', controller.create_machine)
    Route.Register('machine do create',lambda p: controller.create_machine(to_machine(p)))
    Route.Register('machine list',controller.list_machine)
    Route.Register('machine do list',lambda p: controller.list_machine(p['key']))   
    Route.Register('machine count',controller.count_machine)
    Route.Register('machine do count',lambda p: controller.count_machine(p['count'])) 
       
#################################################### material    
    Route.Register('material create', controller.create_material)
    Route.Register('material do create',lambda p: controller.create_material(to_material(p)))
    Route.Register('material list',controller.list_material)
    Route.Register('material do list',lambda p: controller.list_material(p['key']))   
    Route.Register('material count',controller.count_material)
    Route.Register('material do count',lambda p: controller.count_material(p['count']))  

def refesh():
    Route.Foward('material list')
    Route.Foward('machine list')
    Route.Foward('worker list')
    Route.Foward('norm list')
    
    Route.Foward('norm count')
    Route.Foward('worker count')
    Route.Foward('machine count')
    Route.Foward('material count')
    
    Route.Foward('work count')
    Route.Foward('work list')

def add_worker(values=None):
    Route.Foward('worker create')
    Route.Foward('worker list') 
    Route.Foward('worker count')
    
def add_machine(values=None):
    Route.Foward('machine create')
    Route.Foward('machine list')
    Route.Foward('machine count')
    
def add_material(values=None):
    Route.Foward('material create')
    Route.Foward('material list')   
    Route.Foward('material count')    
    
def add_hang_muc(values=None):
    Route.Foward('hang muc create')
    Route.Foward('work list')   

def add_norm_from_excel(values=None):
    Route.Foward('norm create from excel')   
    refesh()

def add_norm(values=None):
    Route.Foward('norm create')
    Route.Foward('norm list')  
    Route.Foward('norm count')   

def add_work(values=None):
    if repo.hang_muc:
        Route.Foward('work create')
        Route.Foward('work list')  
        Route.Foward('work count')        

def save(values=None):
    Route.Foward('file cons save')
    
def open(values=None):
    Route.Foward('file cons load')

def norm_tree_select(values=None):
    if not values['-TREE NORM-']:
        return
    value = values['-TREE NORM-'][0]
    if not value:
        return
    if ex.is_norm(value):
        window['-SELECTED NORM INPUT-'].update(value)
    
def delete_norm(values=None):
    norm_id = values['-SELECTED NORM INPUT-']
    select_id = values['-TREE NORM-'][0]
    print(f'line 295 {norm_id} {select_id}')
    if not norm_id:
        return
    if select_id == norm_id:
        Route.Foward(f'norm do delete ? id = {norm_id}')
        Route.Foward(f'worker norm do delete by norm id ? norm_id={norm_id}')
        Route.Foward(f'machine norm do delete by norm id ? norm_id={norm_id}')
        Route.Foward(f'material norm do delete by norm id ? norm_id={norm_id}')
            
    if ex.is_worker(select_id):
        Route.Foward('worker norm do delete ? norm_id ={} & id = {}'.format(norm_id,select_id))
    elif ex.is_machine(select_id) or ex.is_dif_machine(select_id):
        Route.Foward('machine norm do delete ? norm_id ={} & id = {}'.format(norm_id,select_id))
    else:
        Route.Foward('material norm do delete ? norm_id ={} & id = {}'.format(norm_id,select_id))    
    
    Route.Foward('norm list')

def search_norm(values=None):
    id = values['-NORM SEARCH INPUT-']
    if id:
        Route.Foward('norm do list ? key = {}'.format(values['-NORM SEARCH INPUT-']))
        return
    Route.Foward('norm list')
    Route.Foward('norm count')

def edit_norm(values=None):
    norm_id = values['-SELECTED NORM INPUT-']
    if not norm_id:
        return
    Route.Foward('norm edit ? id = {}'.format(norm_id))
    Route.Foward('norm list')
    
def create_copy_norm(values=None):
    norm_id = values['-SELECTED NORM INPUT-']
    if not norm_id:
        return    
    Route.Foward(f'norm create copy ? id={norm_id}')    


         
func = {'-ADD WORKER-':add_worker,'-ADD MACHINE-':add_machine,'-ADD MATERIAL-':add_material,
        '-ADD HM-': add_hang_muc, '-ADD NORM-': add_norm, '-ADD WORK-': add_work,
        
        '-TREE NORM-' : norm_tree_select, '-DELETE NORM-': delete_norm, '-NORM FIND BUTTON-' : search_norm,
        '-NORM SEARCH INPUT-'+'_Enter' : search_norm, '-EDIT NORM-' : edit_norm,
         '-CREATE COPY NORM-' : create_copy_norm,
         
        'Save': save, 'Open': open,
        'Thêm từ dự toán':add_norm_from_excel}

def main():
    register()
    refesh()
    COPY = None
    
    while True:
        event, values = window.read()
        print(event)
        if event in [None,'Exit']:
            break
        
        if event in func:
            func[event](values)

#################################################### norm
        if event == 'Copy' and get_metadata(window,'-DELETE NORM-'):
            COPY = get_metadata(window,'-DELETE NORM-')
            print(COPY)
            
        if event == 'Paste' and get_metadata(window,'-EDIT NORM-'):
            norm = get_metadata(window,'-EDIT NORM-')[0]
            COPY = get_metadata(window,'-DELETE NORM-')
            for item in COPY:
                pass

        # if event == '-CREATE COPY NORM-' and get_metadata(window,'-DELETE NORM-'):
        #     norm_id_to_copy = Enumerable(get_metadata(window,'-DELETE NORM-')).where(lambda x: ex.is_norm(x)).to_list()
        #     for id in norm_id_to_copy:
        #         Route.Foward(f'norm create copy ? id={id}')
        
                    
                                    
#################################################### work    
        if event in ['-ADD WORK WITH NORM ID-'] and repo.hang_muc and get_metadata(window,'-EDIT NORM-'):
            norm_id =  get_metadata(window,'-EDIT NORM-')[0]
            print(norm_id)
            Route.Foward(f'work create with norm id ? id={norm_id}')
            Route.Foward('work list')  
            Route.Foward('work count')        
            
        if event == '-WORKER FIND BUTTON-':  #and values['-WORKER SEARCH INPUT-']/
            if values['-WORKER SEARCH INPUT-']:
                Route.Foward('worker do list ? key = {}'.format(values['-WORKER SEARCH INPUT-']))
            else:
                Route.Foward('worker list') 
                Route.Foward('worker count')
                
        if event == 'Copy' and get_metadata(window,'-DELETE WORK-'):
            COPY = get_metadata(window,'-DELETE WORK-')
            print(COPY)
            
        if event == 'Paste' and get_metadata(window,'-EDIT WORK-'):
            work = get_metadata(window,'-EDIT WORK-')[0]
            COPY = get_metadata(window,'-DELETE WORK-')
            for item in COPY:
                pass

        if event == '-CREATE COPY WORK-' and get_metadata(window,'-DELETE WORK-'):
            work_id_to_copy = Enumerable(get_metadata(window,'-DELETE WORK-')).where(lambda x: ex.is_work(x)).to_list()
            for id in work_id_to_copy:
                Route.Foward(f'work create copy ? id={id}')               
                
        if event == '-TREE WORK-':
            id = values['-TREE WORK-'] if values['-TREE WORK-'] else None
            event_tree_click_set_meta_data(window,key='-DELETE WORK-', value=id)
            if id:
                if ex.is_hang_muc(id[0]):
                    event_tree_click_set_meta_data(window,key='-EDIT WORK-',value=[id[0],None,None])
                elif ex.is_work(id[0]):
                    event_tree_click_set_meta_data(window,key='-EDIT WORK-',value=[get_metadata(window,'-EDIT WORK-')[0],id[0],None])
                else:
                    event_tree_click_set_meta_data(window,key='-EDIT WORK-',value=[get_metadata(window,'-EDIT WORK-')[0],get_metadata(window,'-EDIT WORK-')[1],id[0]])
                    
        if event == '-EDIT WORK-' and values['-TREE WORK-']:
            hm_id, work_id, other_id = get_metadata(window,'-EDIT WORK-')
            if not other_id and not work_id:
                Route.Foward('hang muc edit ? id = {}'.format(hm_id))
            elif not other_id:
                Route.Foward('work edit ? id = {}'.format(work_id))
            else:
                other_id = other_id
                if ex.is_worker(other_id):
                    Route.Foward('worker work update ? work_id = {} & id ={}'.format(work_id, other_id))
                if ex.is_machine(other_id) or ex.is_dif_machine(other_id):
                    Route.Foward('machine work update ? work_id = {} & id ={}'.format(work_id, other_id))
                if ex.is_material(other_id) or ex.is_dif_material(other_id):
                    Route.Foward('material work update ? work_id = {} & id ={}'.format(work_id, other_id))
                                                        
        if event == '-DELETE WORK-':
            hm_id, work_id, other_id = get_metadata(window,'-EDIT WORK-')
            if work_id and other_id:
                if ex.is_worker(other_id):
                    Route.Foward('worker work do delete ? work_id ={} & id = {}'.format(work_id,other_id))
                elif ex.is_machine(other_id) or ex.is_dif_machine(other_id):
                    Route.Foward('machine work do delete ? work_id ={} & id = {}'.format(work_id,other_id))
                else: #ex.is_machine(other_id) or ex.is_dif_machine(other_id):
                    Route.Foward('material work do delete ? work_id ={} & id = {}'.format(work_id,other_id))
            elif work_id and not other_id:
                Route.Foward(f'work do delete ? id = {work_id}')
                Route.Foward(f'worker work do delete by work id ? work_id={work_id}')
                Route.Foward(f'machine work do delete by work id ? work_id={work_id}')
                Route.Foward(f'material work do delete by work id ? work_id={work_id}')
            
            Route.Foward(f'work time do delete by work id ? work_id ={work_id}')
            Route.Foward(f'worker work time do delete by work id ? work_id ={work_id}')
            
            Route.Foward('work list')                
                

                
                

            
                
        # if event == "-GRAPH-":
        #     graph = window['-GRAPH-']
        #     graph.draw_circle(values['-GRAPH-'], fill_color='yellow', radius=10)                
                
        if event == '-MACHINE FIND BUTTON-':  #and values['-WORKER SEARCH INPUT-']/
            if values['-MACHINE SEARCH INPUT-']:
                Route.Foward('machine do list ? key = {}'.format(values['-MACHINE SEARCH INPUT-']))
            else:
                Route.Foward('machine list')
                Route.Foward('machine count')
                
        if event == '-MATERIAL FIND BUTTON-':  #and values['-WORKER SEARCH INPUT-']/
            if values['-MATERIAL SEARCH INPUT-']:
                Route.Foward('material do list ? key = {}'.format(values['-MATERIAL SEARCH INPUT-']))
            else:
                Route.Foward('material list')
                Route.Foward('material count')


            

    window.close()

if __name__ == "__main__":
    main()