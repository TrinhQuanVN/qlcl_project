from datetime import date, datetime, timedelta
import re
from turtle import color
import pandas as pd
import itertools
import Views
import Repository
import Models
import PySimpleGUI as sg
import Extension as ex
from py_linq import Enumerable
from GUI import KeyGUI


class base_controller:
    def __init__(self,repository:Repository.base_repository,window:sg.Window=None) -> None:
        self.Repository = repository
        self.window = window
    def Render(self,view:Views.base_view,**kwargs):
        if kwargs:
            view(**kwargs).Render()
        else:
            view().Render()
            
    def save_file(self,path=None):
        if not path:
            self.Render(Views.save_file_menu_bar_view)
            return
        if self.Repository.save_change(path):
            print('Constrc saved successfully')
        
    def load_file(self,path=None):
        if not path:
            self.Render(Views.load_file_menu_bar_view)
            return
        if self.Repository.load_file(path):
            print('Constrc loaded successfully')

    def Read(self,values):
        self.values = values
        
    def Update(self,**kwargs):
        self.window[kwargs['key']].update(kwargs['values'])
        
    def create(self,what:str=None,model=None,**kwargs):
        if not model:
            return
        # create with model
        self.Repository.insert_item(model)
    
    @property
    def event_action(self):
        return {
            KeyGUI.work_add_right_click_tree_norm.value : self.event_add_work_on_norm_tree,
            KeyGUI.norm_view_right_click_tree_norm.value : self.event_edit_norm_btn,
            KeyGUI.work_view_right_click_tree_norm.value : self.event_edit_work_btn,
            KeyGUI.work_delete_right_click_tree_norm.value : self.event_delete_work_btn,
            KeyGUI.lmtn_add_right_click_tree_norm.value : self.event_add_lmtn_btn,
            KeyGUI.ntvl_add_right_click_tree_norm.value : self.event_add_ntvl_btn,
            KeyGUI.ntcv_add_right_click_tree_norm.value : self.event_add_ntcv_btn,
            KeyGUI.hang_muc_add_on_menu_bar.value : self.event_add_hang_muc,
            KeyGUI.phan_viec_add_on_menu_bar.value : self.event_add_phan_viec,
            # KeyGUI.hang_muc_edit_on_menu_bar.value : self.event_edit_hang_muc,
            # KeyGUI.phan_viec_edit_on_menu_bar.value : self.event_edit_phan_viec,
            
            KeyGUI.norm_search_btn.value : self.event_search_norm_btn,
            KeyGUI.norm_id_create_work.value : self.event_add_work_on_norm_tree,
            KeyGUI.norm_edit.value : self.event_edit_norm_btn,
            
            KeyGUI.work_search_btn.value : self.event_search_work_btn,
            KeyGUI.work_create_btn.value : self.event_add_work_btn,
            KeyGUI.work_edit_btn.value : self.event_edit_work_btn,
            KeyGUI.work_copy_btn.value : self.event_copy_work_btn,
            KeyGUI.work_delete_btn.value : self.event_delete_work_btn,
            # KeyGUI.work_visualization_btn.value : self.event_visual_work_btn,
            
            
            KeyGUI.norm_tree.value + ' double click': self.event_edit_norm_btn,
            KeyGUI.work_tree.value + ' double click': self.event_edit_work_btn,
            
            KeyGUI.norm_add_on_menu_bar.value : self.event_add_norm_on_menu_bar,
            KeyGUI.group_tab.value : self.event_change_tab,
            

            
        }

        
    def activate_event(self, event, values):
        self.event_action[event](event, values)

    def event_add_hang_muc(self, event, values):
       self.Render(Views.hang_muc_create_view)        

    def event_add_phan_viec(self, event, values):
        self.Render(Views.phan_viec_create_view)       
  
    def event_add_work_on_norm_tree(self, event, values):
        norm_id = values[KeyGUI.norm_tree.value]
        if not norm_id:
            return
        for id in norm_id:
            self._work_create_by_norm(id)

    def event_add_norm_on_menu_bar(self, event, values):
        self.Render(Views.create_norm_from_excel_view)

    def event_add_work_btn(self, event, values):
        hang_muc = self.Repository.get_item('hang_muc')
        if not self.Repository.get_item('phan_viec'):
            self.create_phan_viec(Models.phan_viec('phần việc khác',0))            
        self.Render(Views.work_create_view,
                    hang_muc = hang_muc,
                    phan_viec = self.Repository.get_item('phan_viec'),
                    worker = self.Repository.get_item('worker'),
                    material = self.Repository.get_item('material'),
                    machine = self.Repository.get_item('machine'))
   
    def event_add_lmtn_btn(self, event, values):
        pass

    def event_add_ntcv_btn(self, event, values):
        pass

    def event_add_ntvl_btn(self, event, values):
        pass

    def event_add_nktc_btn(self, event, values):
        pass

    def event_copy_work_btn(self, event, values):
        work_ids = values[KeyGUI.work_tree]
        if not work_ids:
            return
        for id in work_ids:
            self._work_copy(id)
            
      
    def event_change_tab(self, event, values):
        what = values[KeyGUI.group_tab.value]
        active_list = {'work': self.work_list,
                       'norm': self.norm_list,
                       'lmtn': self.lmtn_list,
                       'ntvl': self.ntvl_list,
                       'ntcv': self.ntcv_list,
                       'nktc': self.nktc_list,}                       
        for w, a in active_list.items():
           if w in what:
               a()                     

    def event_change_tab_norm(self, event, values):                        
       self.norm_list()

    def event_change_tab_lmtn(self, event, values):                        
       self.lmtn_list()

    def event_change_tab_ntvl(self, event, values):                        
       self.ntvl_list()
   
    def event_change_tab_ntcv(self, event, values):                        
       self.ntcv_list()
   
    def event_change_tab_nktc(self, event, values):                        
       self.nktc_list()

    def event_delete_work_btn(self, event, values):
        work_id = values[KeyGUI.work_tree]
        if not work_id: return
        for id in work_id:
            self._work_delete(id)
    
    def event_edit_work_btn(self, event, values):
        work_id = values[KeyGUI.work_tree.value]
        if not work_id: return
        if len(work_id) >1:
            sg.PopupOK('Chỉ chọn 1 công việc để sửa!!')
            return
        self.work_edit(work_id[0])

    def event_edit_norm_btn(self, event, values):
        norm_id = values[KeyGUI.norm_tree.value]
        if not norm_id: return
        if len(norm_id) >1:
            sg.PopupOK('Chỉ chọn 1 công việc để sửa!!')
            return
        self.norm_edit(norm_id[0])
        
    def event_search_norm_btn(self, event, values):
        key = values[KeyGUI.norm_search_input]
        if not key:
            return
        self.norm_list(key)

    def event_search_work_btn(self, event, values):
        key = values[KeyGUI.work_search_input]
        if not key:
            return
        self.work_list(key)

    def event_visualization_work_btn(self, event, values):
        pass

    def _norm_count(self,count=None):
        num = count if count else self.Repository.count_item('norm')
        self.Update(key= KeyGUI.norm_count_text.value, values=num)   

    def norm_list(self,key=None):
        if not key:
            if not self.Repository.get_item('norm'):
                return
            self._norm_list(self.Repository.get_item('norm'))
            return
                      
        self._norm_list(self.Repository.get_item('norm', match_mode=1, logic='or', to_lower=True, id=key, name=key[0]))
        print(f'norm list with key {key} is showed !')
            
    def _norm_list(self,norms:list):
        treedata = sg.TreeData()
        if not norms:
            self.Update(key= KeyGUI.norm_tree.value,values=treedata)
            self._norm_count(0)
        for item in norms:
            treedata.Insert('',item.id,item.name,[item.id,item.unit])
            
        self.Update(key= KeyGUI.norm_tree.value,values=treedata)
        self._norm_count(len(norms))
                 
    def norm_create_from_excel(self,path):
        values = ex.read_excel(path)
        count = 0
        for row in values:
            if ex.is_norm(row[1]) and not self.Repository.get_item('norm',id=row[1]):
                count +=1
                self.Repository.insert_item('norm',Models.norm(*row[1:4]))

            if ex.is_norm(row[0]) and ex.is_worker(row[1]):
                if not self.Repository.get_item('worker') or not self.Repository.get_item('worker',id=row[1]):
                    self.Repository.insert_item('worker',Models.worker(*row[1:4]))
                self.Repository.insert_item('worker_norm',Models.worker_norm(row[0],row[1],row[-1]))
                
            elif ex.is_norm(row[0]) and ex.is_machine(row[1]) or ex.is_dif_machine(row[1]):
                if not self.Repository.get_item('machine') or not self.Repository.get_item('machine',id=row[1]):
                    self.Repository.insert_item('machine',Models.machine(*row[1:4]))
                self.Repository.insert_item('machine_norm',Models.machine_norm(row[0],row[1],row[-1]))

            elif ex.is_norm(row[0]) and ex.is_material(row[1]) or ex.is_dif_material(row[1]):
                if not self.Repository.get_item('material') or not self.Repository.get_item('material',id=row[1]):
                    self.Repository.insert_item('material',Models.material(*row[1:4]))
                self.Repository.insert_item('material_norm',Models.material_norm(row[0],row[1],row[-1]))
                
        return count    

    def norm_edit(self,norm_id,model=None):
        if not self.Repository.get_item('norm',id= norm_id):
            print(f'norm {norm_id} is not existed')
            return
        if not model:
            self.Render(Views.norm_edit_view,
                        norm=self.Repository.get_item('norm', id= norm_id)[0],
                        worker_norm= self.Repository.get_item('worker_norm',norm_id= norm_id),
                        machine_norm= self.Repository.get_item('machine_norm',norm_id= norm_id),
                        material_norm= self.Repository.get_item('material_norm',norm_id= norm_id),
                        worker= self.Repository.get_worker_by_norm_id(norm_id),
                        machine= self.Repository.get_machine_by_norm_id(norm_id),
                        material= self.Repository.get_material_by_norm_id(norm_id),
                        workers=self.Repository.get_item('worker'),
                        materials=self.Repository.get_item('material'),
                        machines=self.Repository.get_item('machine'))
            return
        if self.Repository.update_norm(norm_id, model):
            print(f'norm {norm_id} is updated')

    def _work_list(self,works:list):
        treedata = sg.TreeData()
        for item in works:
            treedata.Insert('',item.id,item.name,[item.id,item.unit,item.amount,item.work_day,item.start,item.end])
            
        self.Update(key=KeyGUI.work_tree.value,values=treedata)
        self._work_count(len(works))

    def _work_count(self,count=None):
        num = count if count else self.Repository.count_item('work')
        self.Update(key= KeyGUI.work_count_text.value,values=num)
        
    def work_list(self,key=None):
        if not key:
            if not self.Repository.get_item('work'):
                return
            self._work_list(self.Repository.get_item('work'))
            return
        self._work_list(self.Repository.get_item('work', match_mode=1, logic='or', to_lower=True, id=key, name=key))
        print(f'work list with key {key} is showed !')

    def delete(self,what:str,**kwargs):
        if what in ['worker_work','machine_work','material_work']:
            if not kwargs['id']:
                models = self.Repository.get_item('worker_work', work_id = kwargs['work_id'])
                if models:
                    for item in models:
                        self.Repository.delete_item('worker_work',item)                
            else:
                model = self.Repository.get_item('worker_work',work_id= kwargs['work_id'], id= kwargs['id'])
                if model:
                    self.Repository.delete_item('worker_work',model[0])
                    
        # if what == 'norm':
        #     if not 'values' in kwargs:
        #         self.norm_(kwargs['id'])
        #     norm_ids = self._analyze_tree_select('norm', kwargs['values'])
        #     if norm_ids:
        #         for id in norm_ids:
        #             self._norm_delete(id)  
                                                         
        if 'model' in kwargs:
            self.Repository.delete_item(what,model= kwargs['model'])
        
     
    def _work_delete(self,work_id):
        model = self.Repository.get_item('work',id= work_id)
        worker_work = self.Repository.get_item('worker_work', work_id = work_id)
        machine_work = self.Repository.get_item('machine_work', work_id = work_id)
        material_work = self.Repository.get_item('material_work', work_id = work_id)        
        if not model:
            return
        model = model[0]
        if worker_work:
            for x in worker_work:
                self.Repository.delete_item('worker_work',model)
        if machine_work:
            for x in machine_work:
                self.Repository.insert_item('machine_work', model) 
        if material_work:
            for x in material_work:
                self.Repository.insert_item('material_work', model)         
        self.Repository.delete_item('work',model)

    def _work_copy(self,id):
        model = self.Repository.get_item('work',id = id)
        if not model:
            return
        model = model[0]
        copy_model = Models.work(model.name,model.unit,model.amount,model.hm_id,model.pv_id)
        self._create(model=copy_model)
        
        worker_work = self.Repository.get_item('worker_work',work_id=id)
        if worker_work:
            for item in worker_work:
                self._create(model= Models.worker_work(copy_model.id,item.id,item.amount))
                
        machine_work = self.Repository.get_item('machine_work',work_id=id)
        if machine_work:
            for item in machine_work:
                self._create(model= Models.machine_work(copy_model.id,item.id,item.amount)) 
                
        material_work = self.Repository.get_item('material_work',work_id=id)
        if material_work:
            for item in material_work:
                self._create(model= Models.material_work(copy_model.id,item.id,item.amount))    

    def _work_create_by_norm(self,norm_id):
        norm = self.Repository.get_item('norm', id= norm_id)[0]
        worker_norm = self.Repository.get_item('worker_norm', norm_id = norm_id)
        machine_norm = self.Repository.get_item('machine_norm', norm_id = norm_id)
        material_norm = self.Repository.get_item('material_norm', norm_id = norm_id)
        work = Models.work(norm.name, 
                            norm.unit,
                            amount = 1,
                            hm_id= self.Repository.get_item('hang_muc')[-1].id,
                            pv_id= self.Repository.get_item('phan_viec')[-1].id,)
        self.Repository.insert_item('work',work)
        if worker_norm:
            for x in worker_norm:
                self.Repository.insert_item('worker_work',Models.worker_work(work.id,x.id,x.amount))
        if machine_norm:
            for x in machine_norm:
                self.Repository.insert_item('machine_work',Models.machine_work(work.id,x.id,x.amount)) 
        if material_norm:
            for x in material_norm:
                self.Repository.insert_item('material_work',Models.material_work(work.id,x.id,x.amount))  
        print('work id={} is created'.format(work.id))
        print('trinh tien quan',work.hm_id, work.pv_id)     

    def work_edit(self,work_id=None,model=None):
        if not model:
            if not self.Repository.get_item('work',id= work_id):
                print(f'work {work_id} is not existed')
                return
            work = self.Repository.get_item('work', id =work_id)[0]
            self.Render(Views.work_edit_view,
                        hang_mucs= self.Repository.get_item('hang_muc'),
                        hang_muc= self.Repository.get_item('hang_muc',id = work.hm_id)[0],
                        phan_viec= self.Repository.get_item('phan_viec',id = work.pv_id)[0],
                        phan_viecs= self.Repository.get_item('phan_viec'),
                        work= work,
                        workers= self.Repository.get_item('worker'),
                        machines= self.Repository.get_item('machine'),
                        materials= self.Repository.get_item('material'),
                        worker_work= self.Repository.get_item('worker_work',work_id = work.id),
                        machine_work= self.Repository.get_item('machine_work',work_id = work.id),
                        material_work= self.Repository.get_item('material_work',work_id = work.id))
            return
        self.Repository.update_work(work_id,model)        

    def _lmtn_count(self,count=None):
        num = count if count else self.Repository.count_item('lmtn')
        self.Update(key=KeyGUI.lmtn_count_text.value,values=num)
        
    def lmtn_list(self,key=None):
        if not self.Repository.count_item('lmtn'):
            return
        if not key:
            self._lmtn_list(self.Repository.get_item('lmtn'))
            return
        self._lmtn_list(self.Repository.get_item('lmtn', key=key))
            
    def _lmtn_list(self,lmtn:list):
        treedata = sg.TreeData()
        for item in lmtn:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name,item.sltm, item.slm, item.ktm])
            
        self.Update(key= KeyGUI.lmtn_tree.value,values=treedata)
        self._lmtn_count(len(lmtn))

    def _ntcv_count(self,count=None):
        num = count if count else self.Repository.count_item('ntcv')
        self.Update(key= KeyGUI.ntcv_count_text.value,values=num)
        
    def ntcv_list(self,key=None):
        if not self.Repository.get_item('ntcv'):
            return
        if not key:
            self._list_ntcv(self.Repository.get_item('ntcv'))
            return
        self._list_ntcv(self.Repository.get_item(what= 'ntcv', key=key))
            
    def _list_ntcv(self,ntcv:list):
        treedata = sg.TreeData()
        for item in ntcv:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name])
            
        self.Update(key=KeyGUI.ntcv_tree.value,values=treedata)
        self._ntcv_count(len(ntcv))            

    def _ntvl_count(self,count=None):
        num = count if count else self.Repository.count_item('ntvl')
        self.Update(key= KeyGUI.ntvl_count_text.value,values=num)
        
    def ntvl_list(self,key=None):
        if not self.Repository.get_item('ntvl'):
            return
        if not key:
            self._ntvl_list(self.Repository.get_item('ntvl'))
            print('ntvl list showed!')
            return
        self._ntvl_list(self.Repository.get_item(what= 'ntvl', key=key))
            
    def _ntvl_list(self,ntvl:list):
        treedata = sg.TreeData()
        for item in ntvl:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name])
            
        self.Update(key= KeyGUI.ntvl_tree.value,values=treedata)
        self._ntvl_count(len(ntvl))

    def _nktc_count(self,count=None):
        num = count if count else self.Repository.count_item('nktc')
        self.Update(key= KeyGUI.nktc_count_text.value,values=num)
        
    def nktc_list(self,key=None):
        if not self.Repository.get_item('nktc'):
            return
        if not key:
            self._nktc_list(self.Repository.get_item('nktc'))
            print('nktc list showed!')
            return
        self._nktc_list(self.Repository.get_item(what= 'nktc', key=key))
            
    def _nktc_list(self,nktc:list):
        treedata = sg.TreeData()
        for item in nktc:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name])
            
        self.Update(key= KeyGUI.nktc_tree.value,values=treedata)
        self._nktc_count(len(nktc))



############################################ NTCV
    def create_ntcv(self,model=None):
        if not model:
            self.Render(Views.ntcv_create_view)
            return
        self.Repository.insert_item('ntcv',model)
        print(f'Phần việc {model.id} is created')
                
    def delete_ntcv(self,id:str):
        model = self.Repository.get_item('ntcv',id=id)
        if not model:
            print(f'ntcv {id} not found ')
        self.Repository.delete_item('ntcv',model)
        print(f'Hang muc {id} is deleted ')
            

        
############################################ LMTN
    def choose_default_lmtn(self, dateNT=None):
        self.Render(Views.lmtn_choose_default, dateNT = dateNT, default = self.Repository.default_lmtn)

    def create_lmtn(self,values,model=None,default_id=None,dateNT=None):
        work_id = self._analyze_tree_select('work', values)
        if not work_id:
            self.choose_default_lmtn()
        if len(work_id) > 1:
            sg.popup_ok('Please select only one work !!')
            return
        work = self.Repository.get_item('work',id=work_id[0])
        if work:
            self.choose_default_lmtn(dateNT = work[0].start)
            return
        if not model:
            if default_id:
                self.Render(Views.lmtn_create_with_default_view, default= self.Repository.get_default_lmtn_by_id(default_id), dateNT= dateNT)
                return
        self.Repository.insert_item('lmtn',model)
        print(f'Phần việc {model.id} is created')
                
    def delete_lmtn(self,id:str):
        model = self.Repository.get_item('lmtn',id= id)
        if not model:
            print(f'lmtn {id} is not found ')
            return False
        self.Repository.delete_item('lmtn', model)
        print(f'Hang muc {id} is deleted ')
            

        
        
############################################ NTVL
    def create_ntvl(self,model=None,values=None):
        if not model:
            work_id = values[KeyGUI.work_selected_input.value]
            if not work_id:
                self.Render(Views.ntvl_create_view)
                return
            work = self.Repository.get_item('work', id= work_id)[0]
            self.Render(Views.ntvl_create_view, work=work)
            return            
        self.Repository.insert_item('ntvl',model)
        print(f'ntvl {model.id} is created')
                
    def delete_ntvl(self,id:str):
        model = self.Repository.get_item('ntvl',id=id)
        if not model:
            print(f'ntvl {id} not found ')
        self.Repository.delete_item('ntvl',model)
        print(f'ntvl {id} is deleted ')
            

