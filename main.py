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
    return Models.work(name,unit,amount,hm_id,id)

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
    start = datetime.datetime.strptime(parameter['start'],r'%d/%m/%Y')
    end = datetime.datetime.strptime(parameter['end'],r'%d/%m/%Y')
    return Models.work_time(work_id,start,end)    

def event_tree_click_set_meta_data(window,**kwargs):
    window[kwargs['key']].metadata = kwargs['value']

def get_metadata(window,key):
    return window[key].metadata

def register():
#################################################### work time
    Route.Register('work time do create',lambda p: controller.create_work_time(to_work_time(p)))
    Route.Register('work time initial',controller.inital_work_time)
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

#################################################### workER work    
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
    
def main():
    register()
    refesh()
    COPY = None
    while True:
        event, values = window.read()
        print(event)
        if event in [None]:
            break
        
        if event == '-ADD WORKER-':
            Route.Foward('worker create')
            Route.Foward('worker list') 
            Route.Foward('worker count')        
        
        if event == '-ADD MACHINE-':
            Route.Foward('machine create')
            Route.Foward('machine list')
            Route.Foward('machine count')
            
        if event == '-ADD MATERIAL-':
            Route.Foward('material create')
            Route.Foward('material list')   
            Route.Foward('material count')
#################################################### work time
        if event == '-TAB GROUP-':
            if values['-TAB GROUP-'] == '-TIME TAB-':
                Route.Foward('work time initial')
                Route.Foward('work time list')
                Route.Foward('work time draw')
                # sg.Graph().draw_line(point_from=,point_to=,color=,width=)
                # sg.Graph().draw_text(text=,location=,color=,font=,angle=,text_location='TEXT_LOCATION_CENTER')
        if event == '-GRAPH-_Configure':
            graph = window['-GRAPH-']
            e = graph.user_bind_event
            w0, h0 = graph.CanvasSize
            # Update the canvas size for coordinate conversion
            w1, h1 = graph.CanvasSize = e.width, e.height
            w_scale, h_scale = w1/w0, h1/h0
            graph.widget.scale("all", 0, 0, w_scale, h_scale) 

        if event == '-TREE TIME-':
            id = values['-TREE TIME-'] if values['-TREE TIME-'] else None
            event_tree_click_set_meta_data(window,key='-SHOW WORK-', value=id)                

        if event == '-SHOW WORK-' and values['-TREE TIME-']:
            work_id= get_metadata(window,'-SHOW WORK-')[0]
            if work_id:
                Route.Foward('work edit ? id = {}'.format(work_id))

        if event == '-EDIT TIME-' and values['-TREE TIME-']:
            work_id= get_metadata(window,'-SHOW WORK-')[0]
            if work_id:
                Route.Foward('work time update ? work_id = {}'.format(work_id))
            
#################################################### HANG MUC
        if event == '-ADD HM-':
            Route.Foward('hang muc create')
            Route.Foward('work list')

#################################################### norm
        if event == 'Copy' and get_metadata(window,'-DELETE NORM-'):
            COPY = get_metadata(window,'-DELETE NORM-')
            print(COPY)
            
        if event == 'Paste' and get_metadata(window,'-EDIT NORM-'):
            norm = get_metadata(window,'-EDIT NORM-')[0]
            COPY = get_metadata(window,'-DELETE NORM-')
            for item in COPY:
                pass

        if event == '-CREATE COPY NORM-' and get_metadata(window,'-DELETE NORM-'):
            norm_id_to_copy = Enumerable(get_metadata(window,'-DELETE NORM-')).where(lambda x: ex.is_norm(x)).to_list()
            for id in norm_id_to_copy:
                Route.Foward(f'norm create copy ? id={id}')
    
        if event == '-ADD NORM-':  
            Route.Foward('norm create')
            Route.Foward('norm list')  
            Route.Foward('norm count')
        
        if event == '-TREE NORM-':
            id = values['-TREE NORM-'] if values['-TREE NORM-'] else None
            event_tree_click_set_meta_data(window,key='-DELETE NORM-', value=id)
            print(get_metadata(window,'-DELETE NORM-'))
            if id:
                if ex.is_norm(id[0]):
                    event_tree_click_set_meta_data(window,key='-EDIT NORM-',value=[id[0],None])
                else:
                    event_tree_click_set_meta_data(window,key='-EDIT NORM-',value=[get_metadata(window,'-EDIT NORM-')[0],id])
                print(get_metadata(window,'-EDIT NORM-'))
                    
        if event == '-EDIT NORM-' and values['-TREE NORM-']:
            norm_id, other_id = get_metadata(window,'-EDIT NORM-')
            if not other_id:
                Route.Foward('norm edit ? id = {}'.format(norm_id))
            elif len(other_id)==1:
                other_id = other_id[0]
                if ex.is_worker(other_id):
                    Route.Foward('worker norm update ? norm_id = {} & id ={}'.format(norm_id, other_id))
                if ex.is_machine(other_id) or ex.is_dif_machine(other_id):
                    Route.Foward('machine norm update ? norm_id = {} & id ={}'.format(norm_id, other_id))
                if ex.is_material(other_id) or ex.is_dif_material(other_id):
                    Route.Foward('material norm update ? norm_id = {} & id ={}'.format(norm_id, other_id))
                                                        
        if event == '-DELETE NORM-':
            norm_id, other_id = get_metadata(window,'-EDIT NORM-')
            if norm_id and other_id:
                other_id = other_id[0]
                if ex.is_worker(other_id):
                    Route.Foward('worker norm do delete ? norm_id ={} & id = {}'.format(norm_id,other_id))
                elif ex.is_machine(other_id) or ex.is_dif_machine(other_id):
                    Route.Foward('machine norm do delete ? norm_id ={} & id = {}'.format(norm_id,other_id))
                else: #ex.is_machine(other_id) or ex.is_dif_machine(other_id):
                    Route.Foward('material norm do delete ? norm_id ={} & id = {}'.format(norm_id,other_id))
            elif norm_id and not other_id:
                Route.Foward(f'norm do delete ? id = {norm_id}')
                Route.Foward(f'worker norm do delete by norm id ? norm_id={norm_id}')
                Route.Foward(f'machine norm do delete by norm id ? norm_id={norm_id}')
                Route.Foward(f'material norm do delete by norm id ? norm_id={norm_id}')
                   
            Route.Foward('norm list')
              
#################################################### work    
        if event in ['-ADD WORK-'] and repo.hang_muc:  
            Route.Foward('work create')
            Route.Foward('work list')  
            Route.Foward('work count')
            
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
                   
            Route.Foward('work list')                
                

                
                
        if event == 'Save':
            Route.Foward('file cons save')

        if event == 'Open':
            Route.Foward('file cons load')
            
                
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

        if event in ['-NORM FIND BUTTON-', '-NORM SEARCH INPUT-'+'_Enter']:  #and values['-WORKER SEARCH INPUT-']/
            if values['-NORM SEARCH INPUT-']:
                Route.Foward('norm do list ? key = {}'.format(values['-NORM SEARCH INPUT-']))
            else:
                Route.Foward('norm list')
                Route.Foward('norm count')
            
        if event == 'Thêm từ dự toán':
            Route.Foward('norm create from excel')   
            refesh()
    window.close()

if __name__ == "__main__":
    main()