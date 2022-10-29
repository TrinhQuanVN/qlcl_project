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

def to_ntvl(parameter:Parameter):
    return Models.ntvl(name= parameter['name'],
                    #    work_id= parameter['work_id'] if parameter['work_id'] else None,
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
    Route.Registers({
    'ntvl create': lambda p: controller.create_ntvl(work_id=p['work_id']),
    'ntvl do create': lambda p: controller.create_ntvl(to_ntvl(p)),
    'ntvl list':controller.list_ntvl,
    'ntvl do list':lambda p: controller.list_ntvl(p['key']), 
    'ntvl count':controller.count_ntvl,
    'ntvl do count':lambda p: controller.count_ntvl(p['count']),
        
    'ntcv create': controller.create_ntcv,
    'ntcv do create': lambda p: controller.create_ntcv(to_ntcv(p)),
    'ntcv list':controller.list_ntcv,
    'ntcv do list':lambda p: controller.list_ntcv(p['key']), 
    'ntcv count':controller.count_ntcv,
    'ntcv do count':lambda p: controller.count_ntcv(p['count']),
    
    'lmtn choose default': lambda p: controller.choose_default_lmtn(p['dateNT']),
    'lmtn create with default': lambda p: controller.create_lmtn( dateNT=p['dateNT'], default_id=p['default_id']),
    'lmtn do create': lambda p: controller.create_lmtn(model=to_lmtn(p)),
    'lmtn list': controller.list_lmtn,   
    
    'file cons save': controller.save_file,
    'file cons do save': lambda p: controller.save_file(p['path']),
    'file cons load': controller.load_file,
    'file cons do load': lambda p: controller.load_file(p['path']),  
     
    'hang muc create': controller.create_hang_muc,
    'hang muc do create': lambda p: controller.create_hang_muc(to_hang_muc(p)),  
    
    'phan viec create': controller.create_phan_viec,
    'phan viec do create': lambda p: controller.create_phan_viec(to_phan_viec(p)),
    
    'work create': controller.create_work,
    'work do create': lambda p: controller.create_work(model=to_work(p)),
    'work create with norm id': lambda p: controller.create_work(p['id']),
    'work list': controller.list_work,   
    'work do list': lambda p: controller.list_work(p['key']),  
    
    'work count': controller.count_work,
    'work do count': lambda p: controller.count_work(p['count']),

    'work edit': lambda p: controller.edit_work(p['id']),
    'work do edit': lambda p: controller.edit_work(p['id'],to_work(p)), 
    'work do delete': lambda p: controller.delete_work(p['id']),
    'work create copy': lambda p: controller.create_copy_work(p['id']),

    'worker work do create': lambda p: controller.create_worker_work(to_worker_work(p)),
    'worker work do delete by work id': lambda p: controller.delete_worker_work_by_work_id(p['work_id']),
    'worker work do delete': lambda p: controller.delete_worker_work(p['work_id'],p['id']),
    'worker work update': lambda p: controller.update_worker_work(p['work_id'],p['id']),
    'worker work do update': lambda p: controller.update_worker_work(p['work_id'],p['old_id'],to_worker_work(p)),
    
    'machine work do create': lambda p: controller.create_machine_work(to_machine_work(p)),
    'machine work do delete by work id': lambda p: controller.delete_machine_work_by_work_id(p['work_id']),
    'machine work do delete': lambda p: controller.delete_machine_work(p['work_id'],p['id']),
    'machine work update': lambda p: controller.update_machine_work(p['work_id'],p['id']),
    'machine work do update': lambda p: controller.update_machine_work(p['work_id'],p['old_id'],to_machine_work(p)),
    
    'material work do create': lambda p: controller.create_material_work(to_material_work(p)),
    'material work do delete by work id': lambda p: controller.delete_material_work_by_work_id(p['work_id']),
    'material work do delete': lambda p: controller.delete_material_work(p['work_id'],p['id']),
    'material work update':lambda p: controller.update_material_work(p['work_id'],p['id']),
    'material work do update': lambda p: controller.update_material_work(p['work_id'],p['old_id'],to_material_work(p)),   
       
    'norm create': controller.create_norm,
    'norm do create': lambda p: controller.create_norm(to_norm(p)),
    'norm list': controller.list_norm,  
    'norm do list': lambda p: controller.list_norm(p['key']),
    'norm count': controller.count_norm,
    'norm do count': lambda p: controller.count_norm(p['count']),
    
    'norm do create from excel': lambda p: controller.create_from_excel(p['path']),
    'norm create from excel': controller.create_from_excel,
  
    'norm edit':lambda p: controller.edit_norm(p['id']),
    'norm do edit': lambda p: controller.edit_norm(p['id'],to_norm(p)),
    'norm do delete': lambda p: controller.delete_norm(p['id']),
    'norm create copy': lambda p: controller.create_copy_norm(p['id']),
    
#################################################### workER norm    
    'worker norm do create' : lambda p: controller.create_worker_norm(to_worker_norm(p)),
    'worker norm do delete by norm id': lambda p: controller.delete_by_norm_id(p['norm_id']),
    'worker norm do delete': lambda p: controller.delete_worker_norm(p['norm_id'],p['id']),
    'worker norm update': lambda p: controller.update_worker_norm(p['norm_id'],p['id']),
    'worker norm do update': lambda p: controller.update_worker_norm(p['norm_id'],p['old_id'],to_worker_norm(p)),
   
#################################################### machine norm   
    'machine norm do create': lambda p: controller.create_machine_norm(to_machine_norm(p)),
    'machine norm do delete by norm id': lambda p: controller.delete_by_norm_id(p['norm_id']),
    'machine norm do delete': lambda p: controller.delete_machine_norm(p['norm_id'],p['id']),
    'machine norm update': lambda p: controller.update_machine_norm(p['norm_id'],p['id']),
    'machine norm do update': lambda p: controller.update_machine_norm(p['norm_id'],p['old_id'],to_machine_norm(p)),
        
#################################################### material norm    
    'material norm do create': lambda p: controller.create_material_norm(to_material_norm(p)),
    'material norm do delete by norm id': lambda p: controller.delete_by_norm_id(p['norm_id']),
    'material norm do delete': lambda p: controller.delete_material_norm(p['norm_id'],p['id']),
    'material norm update': lambda p: controller.update_material_norm(p['norm_id'],p['id']),
    'material norm do update': lambda p: controller.update_material_norm(p['norm_id'],p['old_id'],to_material_norm(p)),
        
#################################################### workER    
    'worker create': controller.create_worker,
    'worker do create': lambda p: controller.create_worker(to_worker(p)),
    # 'worker list': controller.list_worker,
    # 'worker do list': lambda p: controller.list_worker(p['key']),  
    # 'worker count': controller.count_worker,
    # 'worker do count': lambda p: controller.count_worker(p['count']), 
      
#################################################### machine   
    'machine create': controller.create_machine,
    'machine do create': lambda p: controller.create_machine(to_machine(p)),
    # 'machine list': controller.list_machine,
    # 'machine do list': lambda p: controller.list_machine(p['key']),   
    # 'machine count': controller.count_machine,
    # 'machine do count': lambda p: controller.count_machine(p['count']), 
       
#################################################### material    
    'material create': controller.create_material,
    'material do create':lambda p: controller.create_material(to_material(p)),
    # 'material list': controller.list_material,
    # 'material do list': lambda p: controller.list_material(p['key']),   
    # 'material count': controller.count_material,
    # 'material do count': lambda p: controller.count_material(p['count']), 
     
    })
    
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
    if repo.get_item('hang_muc'):
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
    work = repo.get_item('work',id=work_id)[0]
    Route.Foward(f"lmtn choose default?dateNT={work.start}")
    
def create_ntvl(values=None):
    work_id = values['-SELECTED WORK INPUT-']
    Route.Foward(f'ntvl create? work_id = {work_id}')
             

func = {'-ADD WORKER-':add_worker,'-ADD MACHINE-':add_machine,'-ADD MATERIAL-':add_material,
        '-ADD HM-': add_hang_muc, '-ADD NORM-': add_norm, '-ADD WORK-': add_work,
        
        '-TREE NORM-' : norm_tree_select, '-DELETE NORM-': delete_norm, '-NORM FIND BUTTON-' : search_norm,
        '-NORM SEARCH INPUT-'+'_Enter' : search_norm, '-EDIT NORM-' : edit_norm,
        '-CREATE COPY NORM-' : create_copy_norm,
         
        '-TREE WORK-' : work_tree_select, '-DELETE WORK-': delete_work, '-WORK FIND BUTTON-' : search_work,
        '-WORK SEARCH INPUT-'+'_Enter' : search_work, '-EDIT WORK-' : edit_work,
        '-CREATE COPY WORK-' : create_copy_work, '-ADD WORK WITH NORM ID-' : add_work_with_norm_id,   
               
        '-TAB GROUP-': change_tab, #Change tab do item list
        'Add LMTN' : choose_default_lmtn, 'Add NTVL' : create_ntvl,
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