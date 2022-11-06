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
                       hm_id= parameter['hm_id'],
                       pv_id= parameter['pv_id'],
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
    'ntvl do create': lambda p: controller.create(model=to_ntvl(p)),
        
    'ntcv do create': lambda p: controller.create_ntcv(model= to_ntcv(p)),
    
    'lmtn do create': lambda p: controller.create_lmtn(model=to_lmtn(p)),
    
    'file cons save': controller.save_file,
    'file cons do save': lambda p: controller.save_file(p['path']),
    'file cons load': controller.load_file,
    'file cons do load': lambda p: controller.load_file(p['path']),  
     
    'hang muc do create': lambda p: controller.create(model= to_hang_muc(p)),  
    
    'phan viec do create': lambda p: controller.create(model= to_phan_viec(p)),
    
    'work do create': lambda p: controller.create(model=to_work(p)),
    'work do update': lambda p: controller.work_edit(work_id=p['id'], model=to_work(p)), 
    'work do delete': lambda p: controller._work_delete(p['id']),


    'worker work do create': lambda p: controller.create(model = to_worker_work(p)),
    'worker work do delete': lambda p: controller.delete(what= 'worker_work',work_id= p['work_id'],id= p['id']),
    # 'worker work update': lambda p: controller.update_worker_work(p['work_id'],p['id']),
    # 'worker work do update': lambda p: controller.update_worker_work(p['work_id'],p['old_id'],to_worker_work(p)),
    
    'machine work do create': lambda p: controller.create(model = to_machine_work(p)),
    'machine work do delete': lambda p: controller.delete('machine_work',work_id= p['work_id'],id= p['id']),
    # 'machine_work update': lambda p: controller.update_machine_work(p['work_id'],p['id']),
    # 'machine_work do update': lambda p: controller.update_machine_work(p['work_id'],p['old_id'],to_machine_work(p)),
    
    'material work do create': lambda p: controller.create(model = to_material_work(p)),
    'material work do delete': lambda p: controller.delete('material_work',work_id= p['work_id'],id= p['id']),
    # 'material_work update':lambda p: controller.update_material_work(p['work_id'],p['id']),
    # 'material_work do update': lambda p: controller.update_material_work(p['work_id'],p['old_id'],to_material_work(p)),   
       
    'norm do create': lambda p: controller.create(model=to_norm(p)),
    'norm do create from excel': lambda p: controller.norm_create_from_excel(path=p['path']),
  
    # 'norm edit':lambda p: controller.edit_norm(p['id']),
    'norm do edit': lambda p: controller.norm_edit(norm_id= p['id'],model= to_norm(p)),
    'norm do delete': lambda p: controller.delete('norm', id= p['id']),
    
#################################################### workER norm    
    'worker norm do create' : lambda p: controller.create(model= to_worker_norm(p)),
    'worker norm do delete by norm id': lambda p: controller.delete('norm', norm_id= ['norm_id']),
    'worker norm do delete': lambda p: controller.delete('norm',norm_id= p['norm_id'],id= p['id']),
    # 'worker_norm update': lambda p: controller.update_worker_norm(p['norm_id'],p['id']),
    # 'worker_norm do update': lambda p: controller.update_worker_norm(p['norm_id'],p['old_id'],to_worker_norm(p)),
   
#################################################### machine norm   
    'machine norm do create' : lambda p: controller.create(model= to_machine_norm(p)),
    'machine norm do delete by norm id': lambda p: controller.delete('norm', norm_id= ['norm_id']),
    'machine norm do delete': lambda p: controller.delete('norm',norm_id= p['norm_id'],id= p['id']),
    # 'machine_norm update': lambda p: controller.update_machine_norm(p['norm_id'],p['id']),
    # 'machine_norm do update': lambda p: controller.update_machine_norm(p['norm_id'],p['old_id'],to_machine_norm(p)),
        
#################################################### material norm    
    'material norm do create' : lambda p: controller.create(model= to_material_norm(p)),
    'material norm do delete by norm id': lambda p: controller.delete('norm', norm_id= ['norm_id']),
    'material norm do delete': lambda p: controller.delete('norm',norm_id= p['norm_id'],id= p['id']),
    # 'material_norm update': lambda p: controller.update_material_norm(p['norm_id'],p['id']),
    # 'material_norm do update': lambda p: controller.update_material_norm(p['norm_id'],p['old_id'],to_material_norm(p)),
        
#################################################### workER    
    'worker do create': lambda p: controller.create(model= to_worker(p)),
    # 'worker list': controller.list_worker,
    # 'worker do list': lambda p: controller.list_worker(p['key']),  
    # 'worker count': controller.count_worker,
    # 'worker do count': lambda p: controller.count_worker(p['count']), 
      
#################################################### machine   
    'machine do create': lambda p: controller.create(model= to_machine(p)),
    # 'machine list': controller.list_machine,
    # 'machine do list': lambda p: controller.list_machine(p['key']),   
    # 'machine count': controller.count_machine,
    # 'machine do count': lambda p: controller.count_machine(p['count']), 
       
#################################################### material    
    'material do create':lambda p: controller.create(model= to_material(p)),
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

def load_test():
    path = r'D:\Python\QuanProject\qlcl project git\qlcl_project\PLHĐ nha thanh tra Kim Bang 2022.xls'
    Route.Foward(f'norm do create from excel?path={path}')
    
    id = next(Models.hang_muc.id_iter)
    name = 'Nhà 3 tầng thanh tra huyện kim bảng'
    Route.Foward(f'hang muc do create?id={id}&name={name}')
def main():
    register()
    # load_test()
    # refesh()
    
    while True:
        event, values = window.read()
        print(event)
        print(values)
        if event in [None,'Exit']:
            break
        
        if event in controller.event_action:
            controller.activate_event(event, values)

    window.close()

if __name__ == "__main__":
    main()