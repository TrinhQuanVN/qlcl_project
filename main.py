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
from GUI import GUI, KeyGUI
import PySimpleGUI as sg

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
    # 'ntvl create': lambda p: controller.create_ntvl(work_id=p['work_id']),
    'ntvl do create': lambda p: controller.create_ntvl(model=to_ntvl(p)),
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
    # 'work create with norm id': lambda p: controller.create_work(p['id']),
    'work list': controller.list_work,   
    # 'work do list': lambda p: controller.list_work(p['key']),  
    
    'work count': controller.count_work,
    'work do count': lambda p: controller.count_work(p['count']),

    # 'work edit': lambda p: controller.edit_work(p['id']),
    # 'work do edit': lambda p: controller.edit_work(p['id'],to_work(p)), 
    # 'work do delete': lambda p: controller.delete_work(p['id']),
    # 'work create copy': lambda p: controller.create_copy_work(p['id']),

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
    
    'norm do create from excel': lambda p: controller.create_from_excel(path=p['path']),
  
    # 'norm edit':lambda p: controller.edit_norm(p['id']),
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

def add_hang_muc(values=None):
    Route.Foward('hang muc create')
    Route.Foward('work list')   

def change_tab(values):
    d = {KeyGUI.ntcv_tab.value : 'ntcv list',
         KeyGUI.work_tab.value: 'work list', # 
         KeyGUI.norm_tab.value: 'norm list', # 
         KeyGUI.lmtn_tab.value: 'lmtn list',
         KeyGUI.ntvl_tab.value: 'ntvl list',
         KeyGUI.nktc_tab.value: 'nktc list',}
    Route.Foward(d[values[KeyGUI.group_tab.value]])
    
func = {
        # '-ADD WORKER-':add_worker,'-ADD MACHINE-':add_machine,'-ADD MATERIAL-':add_material,
        KeyGUI.hang_muc_create.value: controller.create_hang_muc,
        KeyGUI.norm_create.value: controller.create_norm,
        KeyGUI.work_create.value: controller.create_work,
        
        KeyGUI.norm_delete.value: controller.delete_norm,
        KeyGUI.norm_find_button.value: controller.list_norm,
        KeyGUI.norm_search_input.value+'_Enter' : controller.list_norm,
        KeyGUI.norm_edit.value : controller.edit_norm,
        KeyGUI.norm_copy.value : controller.create_copy_norm,
        KeyGUI.norm_tree.value + ' double click': controller.edit_norm,
        
         
        KeyGUI.work_delete.value: controller.delete_work,
        KeyGUI.work_find_button.value : controller.list_work,
        KeyGUI.work_find_button.value+'_Enter' : controller.list_work,
        # KeyGUI.work_edit.value : controller.,
        KeyGUI.work_copy.value : controller.create_copy_work,
        KeyGUI.norm_id_create_work.value : controller.create_work,   
               
        KeyGUI.group_tab.value: change_tab, #Change tab do item list
        KeyGUI.lmtn_create : controller.create_lmtn, # 'Add NTVL' : controller.create_ntvl,
        # 'Save': save, 'Open': open,
        'Thêm từ dự toán' : controller.create_from_excel}


def load_test():
    path = r'D:\Python\QuanProject\qlcl project git\qlcl_project\PLHĐ nha thanh tra Kim Bang 2022.xls'
    Route.Foward(f'norm do create from excel?path={path}')
    
    id = next(Models.hang_muc.id_iter)
    name = 'Nhà 3 tầng thanh tra huyện kim bảng'
    Route.Foward(f'hang muc do create?id={id}&name={name}')
def main():
    register()
    load_test()
    # refesh()
    
    while True:
        event, values = window.read()
        print(event)
        print(values)
        if event in [None,'Exit']:
            break
        
        if event in func:
            func[event](values = values)

    window.close()

if __name__ == "__main__":
    main()