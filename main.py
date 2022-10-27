import datetime
from random import randint
from tabnanny import check
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

def to_worker(parameter:Parameter):
    return Models.worker(id= parameter['id'],
                          name= parameter['name'],
                          unit= parameter['unit'])

def to_machine(parameter:Parameter):
    return Models.machine(id= parameter['id'],
                          name= parameter['name'],
                          unit= parameter['unit'])

def to_material(parameter:Parameter):
    return Models.material(id= parameter['id'],
                          name= parameter['name'],
                          unit= parameter['unit'])

def to_norm(parameter:Parameter):
    return Models.norm(id= parameter['id'],
                          name= parameter['name'],
                          unit= parameter['unit'])

def to_worker_norm(parameter:Parameter):
    return Models.worker_norm(norm_id= parameter['norm_id'],
                              id= parameter['id'],
                              amount= parameter['amount'])

def to_machine_norm(parameter:Parameter):
    return Models.machine_norm(norm_id= parameter['norm_id'],
                              id= parameter['id'],
                              amount= parameter['amount'])

def to_material_norm(parameter:Parameter):
    return Models.material_norm(norm_id= parameter['norm_id'],
                              id= parameter['id'],
                              amount= parameter['amount'])

def to_work(parameter:Parameter):
    return Models.work(name= parameter['name'],
                       unit= parameter['unit'],
                       amount= float(parameter['amount']) if parameter['amount'] else 0,
                       hm_id= int(parameter['hm_id']),
                       pv_id= int(parameter['pv_id']) if parameter['pv_id'] else 0,
                       start= ex.to_date(parameter['start']) if parameter['start'] else None,
                       end= ex.to_date(parameter['end']) if parameter['end'] else None,
                       id= parameter['id'])

def to_worker_work(parameter:Parameter):
    return Models.worker_work(work_id= parameter['work_id'],
                            id= parameter['id'],
                            amount = parameter['amount'])

def to_machine_work(parameter:Parameter):
    return Models.machine_work(work_id= parameter['work_id'],
                            id= parameter['id'],
                            amount = parameter['amount'])

def to_material_work(parameter:Parameter):
    return Models.material_work(work_id= parameter['work_id'],
                            id= parameter['id'],
                            amount = parameter['amount'])

def to_hang_muc(parameter:Parameter):
    return Models.hang_muc(name= parameter['name'],
                           id=parameter['id'])

def to_phan_viec(parameter:Parameter):
    return Models.phan_viec(name= parameter['name'],
                           id=parameter['id'])

def to_ntcv(parameter:Parameter):
    return Models.ntcv(name= parameter['name'],
                       work_id= parameter['work_id'] if parameter['work_id'] else None,
                       dateNT= ex.to_date(parameter['dateNT']) if parameter['dateNT'] else None,
                       id=parameter['id'])

def to_lmtn(parameter:Parameter):
    return Models.lmtn(name= parameter['name'],
                       sltm= parameter['sltm'],
                       slm= parameter['slm'],
                       ktm= parameter['ktm'],
                       yc= parameter['yc'],
                       dateNT= ex.to_date(parameter['dateNT']) if parameter['dateNT'] else None,
                       id=parameter['id'])

def register():
#################################################### NTCV
    Route.Register('ntcv create', controller.create_ntcv)
    Route.Register('ntcv do create', lambda p: controller.create_ntcv(to_ntcv(p)))
    Route.Register('ntcv list',controller.list_ntcv)    
    Route.Register('ntcv do list',lambda p: controller.list_ntcv(p['key'])) 
    Route.Register('ntcv count',controller.count_ntcv)
    Route.Register('ntcv do count',lambda p: controller.count_ntcv(p['count']))

#################################################### LMTN
    Route.Register('lmtn choose default',lambda p: controller.choose_default_lmtn(p['dateNT']))
    Route.Register('lmtn create with default',lambda p: controller.create_lmtn( dateNT=p['dateNT'], default_id=p['default_id']))
    Route.Register('lmtn do create', lambda p: controller.create_lmtn(model=to_lmtn(p)))
    Route.Register('lmtn list',controller.list_lmtn)    
    

#################################################### File
    Route.Register('file cons save', controller.save_file)
    Route.Register('file cons do save',lambda p: controller.save_file(p['path']))
    Route.Register('file cons load', controller.load_file)
    Route.Register('file cons do load',lambda p: controller.load_file(p['path']))
    
#################################################### HANG MUC
    Route.Register('hang muc create', controller.create_hang_muc)
    Route.Register('hang muc do create', lambda p: controller.create_hang_muc(to_hang_muc(p)))
    
#################################################### Phan viec
    Route.Register('phan viec create', controller.create_phan_viec)
    Route.Register('phan viec do create', lambda p: controller.create_phan_viec(to_phan_viec(p)))
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
    Route.Register('norm count',controller.count_norm)
    Route.Register('norm do count',lambda p: controller.count_norm(p['count']))
    
    Route.Register('norm do create from excel',lambda p: controller.create_from_excel(p['path']))
    Route.Register('norm create from excel',controller.create_from_excel)
  
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
    # Route.Register('worker list',controller.list_worker)
    # Route.Register('worker do list',lambda p: controller.list_worker(p['key']))   
    # Route.Register('worker count',controller.count_worker)
    # Route.Register('worker do count',lambda p: controller.count_worker(p['count'])) 
      
#################################################### machine   
    Route.Register('machine create', controller.create_machine)
    Route.Register('machine do create',lambda p: controller.create_machine(to_machine(p)))
    # Route.Register('machine list',controller.list_machine)
    # Route.Register('machine do list',lambda p: controller.list_machine(p['key']))   
    # Route.Register('machine count',controller.count_machine)
    # Route.Register('machine do count',lambda p: controller.count_machine(p['count'])) 
       
#################################################### material    
    Route.Register('material create', controller.create_material)
    Route.Register('material do create',lambda p: controller.create_material(to_material(p)))
    # Route.Register('material list',controller.list_material)
    # Route.Register('material do list',lambda p: controller.list_material(p['key']))   
    # Route.Register('material count',controller.count_material)
    # Route.Register('material do count',lambda p: controller.count_material(p['count']))  

def refesh():
    Route.Foward('material list')
    Route.Foward('machine list')
    Route.Foward('worker list')
    Route.Foward('norm list')
    
    Route.Foward('norm count')
    # Route.Foward('worker count')
    # Route.Foward('machine count')
    # Route.Foward('material count')
    
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

############################## WORK
def work_tree_select(values=None):
    if not values['-TREE WORK-']:
        return
    window['-SELECTED WORK INPUT-'].update(values['-TREE WORK-'][0])
        
def delete_work(values=None):
    work_id = values['-SELECTED WORK INPUT-']
    select_id = values['-TREE WORK-'][0]
    print(f'line 295 {work_id} {select_id}')
    if not work_id:
        return
    if select_id == work_id:
        Route.Foward(f'work do delete ? id = {work_id}')
        Route.Foward(f'worker work do delete by work id ? work_id={work_id}')
        Route.Foward(f'machine work do delete by work id ? work_id={work_id}')
        Route.Foward(f'material work do delete by work id ? work_id={work_id}')
            
    if ex.is_worker(select_id):
        Route.Foward('worker work do delete ? work_id ={} & id = {}'.format(work_id,select_id))
    elif ex.is_machine(select_id) or ex.is_dif_machine(select_id):
        Route.Foward('machine work do delete ? work_id ={} & id = {}'.format(work_id,select_id))
    elif ex.is_material(select_id) or ex.is_dif_material(select_id):
        Route.Foward('material work do delete ? work_id ={} & id = {}'.format(work_id,select_id))    
    
    Route.Foward('work list')
        
def search_work(values=None):
    id = values['-WORK SEARCH INPUT-']
    if id:
        Route.Foward('work do list ? key = {}'.format(values['-WORK SEARCH INPUT-']))
        return
    Route.Foward('work list')
    Route.Foward('work count')

def edit_work(values=None):
    work_id = values['-SELECTED WORK INPUT-']
    if not work_id:
        return
    Route.Foward('work edit ? id = {}'.format(work_id))
    Route.Foward('work list')
    
def create_copy_work(values=None):
    work_id = values['-SELECTED WORK INPUT-']
    if not work_id:
        return    
    Route.Foward(f'work create copy ? id={work_id}') 
    
def check_hang_muc():
    if repo.hang_muc:
        return True
    repond = sg.popup_ok_cancel('Không tìm thấy hạng mục. Bạn có muốn tạo hạng mục mới ?')
    print(repond)
    if repond == 'OK':
        Route.Foward('hang muc create')
    return False
    
def add_work_with_norm_id(values):
    norm_id = values['-SELECTED NORM INPUT-']
    if not norm_id:
        return
    if check_hang_muc():
        Route.Foward(f'work create with norm id ? id={norm_id}')
        Route.Foward('work list')  
        Route.Foward('work count')    

def change_tab(values):
    d = {'-NTCV TAB-': 'ntcv list',
         '-WORK TAB-': '', # work list
         '-NORM TAB-': '', # norm list
         '-LMTN TAB-': 'lmtn list',
         '-NTVL TAB-': 'ntvl list',
         '-NKTC TAB-': 'nktc list',}
    Route.Foward(d[values['-TAB GROUP-']])
    
def choose_default_lmtn(values=None):
    work_id = values['-SELECTED WORK INPUT-']
    if not work_id:
        Route.Foward("lmtn choose default?dateNT=''")
    work = repo.get_work_by_id(work_id)
    Route.Foward(f"lmtn choose default?dateNT={work.start}")
    

         
func = {'-ADD WORKER-':add_worker,'-ADD MACHINE-':add_machine,'-ADD MATERIAL-':add_material,
        '-ADD HM-': add_hang_muc, '-ADD NORM-': add_norm, '-ADD WORK-': add_work,
        
        '-TREE NORM-' : norm_tree_select, '-DELETE NORM-': delete_norm, '-NORM FIND BUTTON-' : search_norm,
        '-NORM SEARCH INPUT-'+'_Enter' : search_norm, '-EDIT NORM-' : edit_norm,
        '-CREATE COPY NORM-' : create_copy_norm,
         
        '-TREE WORK-' : work_tree_select, '-DELETE WORK-': delete_work, '-WORK FIND BUTTON-' : search_work,
        '-WORK SEARCH INPUT-'+'_Enter' : search_work, '-EDIT WORK-' : edit_work,
        '-CREATE COPY WORK-' : create_copy_work, '-ADD WORK WITH NORM ID-' : add_work_with_norm_id,   
               
        '-TAB GROUP-': change_tab, #Change tab do item list
        'Add LMTN' : choose_default_lmtn,
        'Save': save, 'Open': open,
        'Thêm từ dự toán' : add_norm_from_excel}


def load_test():
    path = r'D:\Python\QuanProject\qlcl project git\qlcl_project\PLHĐ nha thanh tra Kim Bang 2022.xls'
    Route.Foward(f'norm do create from excel?path={path}')
    
    id = next(Models.hang_muc.id_iter)
    name = 'Nhà 3 tầng thanh tra huyện kim bảng'
    Route.Foward(f'hang muc do create?id={id}&name={name}')
def main():
    register()
    load_test()
    refesh()
    
    while True:
        event, values = window.read()
        # print(event, values)
        if event in [None,'Exit']:
            break
        
        if event in func:
            func[event](values)
       
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