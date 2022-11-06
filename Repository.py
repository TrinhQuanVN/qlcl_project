from datetime import datetime
from enum import Enum
import Models
import DataAccess
from py_linq import Enumerable
class base_repository:
    def __init__(self,context:DataAccess.data_access) -> None:
        self.context = context
        self.context.load()

    @property
    def whats(self):
        return self.context.items

    def update_work(self,id,model:Models.work):
        old = self.get_item('work',id=id)[0]
        old.update(model.items())
        print(f'work {old.id} is updated successfully')

    # def update_worker_work(self,work_id,id,model):
    #     old = self.get_worker_work(work_id,id)
    #     if old:
    #         old.id = model.id
    #         old.amount = model.amount
    #         return True
    #     return False
    
   
    # def update_machine_work(self,work_id,id,model):
    #     old = self.get_machine_work(work_id,id)
    #     if old:
    #         old.id = model.id
    #         old.amount = model.amount
    #         return True
    #     return False
   
    # def update_material_work(self,work_id,id,model):
    #     old = self.get_material_work(work_id,id)
    #     if old:
    #         old.id = model.id
    #         old.amount = model.amount
    #         return True
    #     return False
  
    def update_norm(self,id,model:Models.norm):
        old = self.get_norm_by_id(id=id)
        old.name = model.name
        old.unit = model.unit
        return True
 
    # def update_worker_norm(self,norm_id,id,model):
    #     old = self.get_worker_norm(norm_id,id)
    #     if old:
    #         old.id = model.id
    #         old.amount = model.amount
    #         return True
    #     return False

    # def update_machine_norm(self,norm_id,id,model):
    #     old = self.get_machine_norm(norm_id,id)
    #     if old:
    #         old.id = model.id
    #         old.amount = model.amount
    #         return True
    #     return False    

    # def update_material_norm(self,norm_id,id,model):
    #     old = self.get_material_norm(norm_id,id)
    #     if old:
    #         old.id = model.id
    #         old.amount = model.amount
    #         return True
    #     return False    
 
    def get_worker_by_norm_id(self,norm_id):
        items = self.get_item('worker_norm',norm_id=norm_id)
        return Enumerable(self.get_item('worker')).where(lambda x: x.id in [item.id for item in items]).to_list()
 
    def get_worker_by_work_id(self,work_id):
        items = self.get_item('worker_work',work_id=work_id)
        return Enumerable(self.get_item('worker')).where(lambda x: x.id in [item.id for item in items]).to_list()

    def get_machine_by_norm_id(self,norm_id):
        items = self.get_item('machine_norm',norm_id=norm_id)
        return Enumerable(self.get_item('machine')).where(lambda x: x.id in [item.id for item in items]).to_list()
 
    def get_machine_by_work_id(self,work_id):
        items = self.get_item('machine_work',work_id=work_id)
        return Enumerable(self.get_item('machine')).where(lambda x: x.id in [item.id for item in items]).to_list()

    def get_material_by_norm_id(self,norm_id):
        items = self.get_item('material_norm',norm_id=norm_id)
        return Enumerable(self.get_item('material')).where(lambda x: x.id in [item.id for item in items]).to_list()
 
    def get_material_by_work_id(self,work_id):
        items = self.get_item('material_work',work_id=work_id)
        return Enumerable(self.get_item('material')).where(lambda x: x.id in [item.id for item in items]).to_list()
    
    def save_change(self,path):
        self.context.path = path
        self.context.save_change()
        return True
        
    def save_path(self,path):
        self.context.path = path
        
    def load_file(self,path):
        self.context.path = path
        self.context.load()

    # def update_ntcv(self,id,model:Models.ntcv):
    #     old = self.get_ntcv_by_id(id=id)
    #     old.name = model.name
    #     old.dateNT = model.dateNT
    #     old.dateYC = model.dateYC
    #     return True
    
    # def update_lmtn(self,id,model:Models.lmtn):
    #     old = self.get_lmtn_by_id(id=id)
    #     old.name = model.name
    #     old.dateNT = model.dateNT
    #     old.dateYC = model.dateYC
    #     old.sltm = model.sltm
    #     old.slm = model.slm
    #     old.ktm = model.ktm
    #     return True
    
    @property
    def default_lmtn(self):
        return self.context.default_lmtn
    
    @property
    def _linq_default_lmtn(self):
        return Enumerable(self.default_lmtn)
    
    def get_default_lmtn_by_id(self,id:str) -> Models.lmtn:
        if not self.default_lmtn:
            return None
        list = self._linq_default_lmtn.where(lambda x: x.id == id).to_list()
        return list[0] if list else None

    # def update_ntcv(self,id,model:Models.ntcv):
    #     old = self.get_ntcv_by_id(id=id)
    #     old.name = model.name
    #     old.dateNT = model.dateNT
    #     old.dateYC = model.dateYC
    #     return True

    # def update(self,what,model,**kwargs):
    #     old = self.get_item(what,**kwargs)
    #     if old and len(old) == 1:
    #         old[0].update(model.items())
    #         return True
    #     return False
        
    def count_item(self,what:str):
        return len(self.whats[what])
    
    def get_item(self,what:str, match_mode=0, logic:str='and', to_lower=False, **kwargs):
        """get item from repository

        Args:
            what (str): what list of data to get
            match_mode (_type_, optional): 0:exact match, 1:key in value. Defaults to 0.
            logic (str, optional): if true search with and operator. Defaults to and.
            to_lower (bool, optional): key and value search to lower if True. Defaults to False.

        Returns:
            _type_: a list of item
        """
        def where(xs:Enumerable, key, value, to_lower, match_mode):
            if to_lower and match_mode==0:
                return xs.where(lambda x: value.to_lower() == x.items()[key].to_lower())
            elif to_lower and match_mode==1:
                return xs.where(lambda x: value.to_lower() in x.items()[key].to_lower())
            elif not to_lower and match_mode==0:
                return xs.where(lambda x: value == x.items()[key])
            elif not to_lower and match_mode==1:
                return xs.where(lambda x: value in x.items()[key])                    
        
        if not kwargs:
            return self.whats[what]
        elif len(kwargs) == 1:
            key, value = list(kwargs.items())[0]
            return where(Enumerable(self.whats[what]), key, value, to_lower, match_mode).to_list()
        else:
            if logic == 'and': # operator 'and'
                result = self.whats[what]
                for key,value in kwargs.items():
                    result = where(Enumerable(result),key,value,to_lower,match_mode)
                return result.to_list()
            else:
                enumrables = []
                for key, value in kwargs.items():
                    enumrables.append(where(Enumerable(self.whats[what]), key, value,to_lower, match_mode))            
                result = enumrables[0].to_list()
                for enum in enumrables[1:]:
                    if enum.to_list():
                        result += enum.to_list() 
                return set(result)

    def insert_item(self,what:str=None, model=None):
        """insert item to data

        Args:
            what (str): what data list name to insert
            model (_type_): model to insert
        """
        if not model: return
        if not what:
            what = model.__class__.__name__
        self.whats[what].append(model)
        print(f'a {what} whose id {model.id} is inserted successfully')
        
    def delete_item(self,what:str=None,model=None):
        if not model: return
        if not what:
            what = model.__class__.__name__
        self.whats[what].remove(model)
        print(f'a {what} whose id {model.id} is deleted successfully')
        
        

    

        
        
