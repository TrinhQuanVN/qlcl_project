from datetime import datetime
import Models
import DataAccess
from py_linq import Enumerable
class base_repository:
    def __init__(self,context:DataAccess.data_access) -> None:
        self.context = context
        # self.context.load()

    @property
    def whats(self):
        return self.context.items

# ############################################ work 
#     @property
#     def work(self):
#         return self.context.work
    
#     @property
#     def work_count(self):
#         return len(self.work)

#     @property
#     def _linq_work(self):
#         return Enumerable(self.context.work)
      
#     def sorted_work(self):
#         return self._linq_work.order_by(lambda x: x.id)
       
#     def get_work_by_id(self,id:str) -> Models.work:
#         if not self.work:
#             return None
#         list = self._linq_work.where(lambda x: x.id == id)
#         return list[0] if list else None

#     def get_work_by_key(self,key:str):
#         if not self.work:
#             return None
#         list = self._linq_work.where(lambda x: key.lower() in x.id.lower() or key.lower() in x.name.lower()).to_list()
#         return list
    
#     def is_work_exist(self,id):
#         return True if self.get_work_by_id(id) else False
    
#     def insert_work(self,model):
#         self.context.work.append(model)     

#     def delete_work(self,model):
#         self.context.work.remove(model)
#         return True
    
    def update_work(self,id,model:Models.work):
        old = self.get_work_by_id(id=id)
        old.name = model.name
        old.unit = model.unit
        old.amount = model.amount
        return True
# ############################################ worker work 
#     @property
#     def worker_work(self):
#         return self.context.worker_work

#     @property
#     def _linq_worker_work(self):
#         return Enumerable(self.context.worker_work)
      
#     def insert_worker_work(self,model):
#         self.context.worker_work.append(model)        

#     def get_worker_work_by_work_id(self,work_id):
#         return self._linq_worker_work.where(lambda x: x.work_id == work_id).to_list()
    
#     def get_worker_work(self,work_id,id) -> Models.worker_work:
#         return self._linq_worker_work.where(lambda x: x.work_id.lower() == work_id.lower() and x.id.lower() == id.lower()).to_list()[0]

    def update_worker_work(self,work_id,id,model):
        old = self.get_worker_work(work_id,id)
        if old:
            old.id = model.id
            old.amount = model.amount
            return True
        return False
    
    # def delete_worker_work(self,model:Models.worker_work):
    #     self.context.worker_work.remove(model)
    #     return True

# ############################################ machine work
#     @property
#     def machine_work(self):
#         return self.context.machine_work
    
#     @property
#     def _linq_machine_work(self):
#         return Enumerable(self.context.machine_work)
       
#     def insert_machine_work(self,model):
#         self.context.machine_work.append(model)

#     def get_machine_work_by_work_id(self,work_id):
#         return self._linq_machine_work.where(lambda x: x.work_id == work_id).to_list()

#     def get_machine_work(self,work_id,id) -> Models.machine_work:
#         return self._linq_machine_work.where(lambda x: x.work_id.lower() == work_id.lower() and x.id.lower() == id.lower()).to_list()[0]

    def update_machine_work(self,work_id,id,model):
        old = self.get_machine_work(work_id,id)
        if old:
            old.id = model.id
            old.amount = model.amount
            return True
        return False
    
    # def delete_machine_work(self,model):
    #     self.context.machine_work.remove(model)
    #     return True

############################################ material work
    # @property
    # def material_norm(self):
    #     return self.context.material_norm 

    # @property
    # def _linq_material_norm(self):
    #     return Enumerable(self.context.material_norm)
    
    # @property
    # def material_work(self):
    #     return self.context.material_work 

    # @property
    # def _linq_material_work(self):
    #     return Enumerable(self.context.material_work)
       
    # def insert_material_work(self,model):
    #     self.context.material_work.append(model)
        
    # def get_material_work_by_work_id(self,work_id):
    #     return self._linq_material_work.where(lambda x: x.work_id == work_id).to_list()

    # def get_material_work(self,work_id,id) -> Models.material_work:
    #     return self._linq_material_work.where(lambda x: x.work_id.lower() == work_id.lower() and x.id.lower() == id.lower()).to_list()[0]  

    def update_material_work(self,work_id,id,model):
        old = self.get_material_work(work_id,id)
        if old:
            old.id = model.id
            old.amount = model.amount
            return True
        return False
    
    # def delete_material_work(self,model):
    #     self.context.material_work.remove(model)
    #     return True

############################################ norm
    # @property
    # def norm(self):
    #     return self.context.norm
    
    # @property
    # def norm_count(self):
    #     return len(self.norm)

    # @property
    # def _linq_norm(self):
    #     return Enumerable(self.context.norm)
    
    # def sorted_norm(self):
    #     return self._linq_norm.order_by(lambda x: x.id)
       
    # def get_norm_by_id(self,id:str) -> Models.norm:
    #     if not self.norm:
    #         return None
    #     list = self._linq_norm.where(lambda x: x.id.lower() == id.lower()).to_list()
    #     return list[0] if list else None

    # def get_norm_by_key(self,key:str):
    #     if not self.norm:
    #         return None
    #     list = self._linq_norm.where(lambda x: key.lower() in x.id.lower()  or key.lower() in x.name.lower()).to_list()       
    #     return list

    # def is_norm_exist(self,id):
    #     return True if self.get_norm_by_id(id) else False

    def update_norm(self,id,model:Models.norm):
        old = self.get_norm_by_id(id=id)
        old.name = model.name
        old.unit = model.unit
        return True
   
    # def insert_norm(self,model):
    #     self.context.norm.append(model)   

    # def delete_norm(self,model):
    #     self.context.norm.remove(model)
    #     return True         



############################################ worker norm 
    # @property
    # def worker_norm(self):
    #     return self.context.worker_norm

    # @property
    # def _linq_worker_norm(self):
    #     return Enumerable(self.context.worker_norm)
     
    # def insert_worker_norm(self,model):
    #     self.context.worker_norm.append(model)        

    # def get_worker_norm_by_norm_id(self,norm_id):
    #     return self._linq_worker_norm.where(lambda x: x.norm_id.lower() == norm_id.lower()).to_list()

    # def get_worker_work_by_work_id(self,work_id):
    #     return self._linq_worker_work.where(lambda x: x.work_id == work_id).to_list()
        
    # def get_worker_norm(self,norm_id,id) -> Models.worker_norm:
    #     return self._linq_worker_norm.where(lambda x: x.norm_id.lower() == norm_id.lower() and x.id.lower() == id.lower()).to_list()[0]

    def update_worker_norm(self,norm_id,id,model):
        old = self.get_worker_norm(norm_id,id)
        if old:
            old.id = model.id
            old.amount = model.amount
            return True
        return False

    # def delete_worker_norm(self,model):
    #     self.context.worker_norm.remove(model)
    #     return True

# ############################################ machine norm
#     @property
#     def machine_norm(self):
#         return self.context.machine_norm
    
#     @property
#     def _linq_machine_norm(self):
#         return Enumerable(self.context.machine_norm)
       
#     def insert_machine_norm(self,model):
#         self.context.machine_norm.append(model)

#     def get_machine_norm_by_norm_id(self,norm_id):
#         return self._linq_machine_norm.where(lambda x: x.norm_id == norm_id).to_list()

#     def get_machine_work_by_work_id(self,work_id):
#         return self._linq_machine_work.where(lambda x: x.work_id == work_id).to_list()

#     def get_machine_norm(self,norm_id,id) -> Models.machine_norm:
#         return self._linq_machine_norm.where(lambda x: x.norm_id.lower() == norm_id.lower() and x.id.lower() == id.lower()).to_list()[0]

    def update_machine_norm(self,norm_id,id,model):
        old = self.get_machine_norm(norm_id,id)
        if old:
            old.id = model.id
            old.amount = model.amount
            return True
        return False    
    
#     def delete_machine_norm(self,model):
#         self.context.machine_norm.remove(model)
#         return True

# ############################################ material norm   
#     def insert_material_norm(self,model):
#         self.context.material_norm.append(model)

#     def get_material_work_by_work_id(self,work_id):
#         return self._linq_material_work.where(lambda x: x.work_id == work_id).to_list()
        
#     def get_material_norm_by_norm_id(self,norm_id):
#         return self._linq_material_norm.where(lambda x: x.norm_id == norm_id).to_list()

#     def get_material_norm(self,norm_id,id) -> Models.material_norm:
#         return self._linq_material_norm.where(lambda x: x.norm_id.lower() == norm_id.lower() and x.id.lower() == id.lower()).to_list()[0]

    def update_material_norm(self,norm_id,id,model):
        old = self.get_material_norm(norm_id,id)
        if old:
            old.id = model.id
            old.amount = model.amount
            return True
        return False    
    
#     def delete_material_norm(self,model):
#         self.context.material_norm.remove(model)
#         return True

# ############################################ worker 
#     @property
#     def worker(self):
#         return self.context.worker

#     @property
#     def worker_count(self):
#         return len(self.worker)

#     @property
#     def _linq_worker(self):
#         return Enumerable(self.context.worker)
  
#     def insert_worker(self,model):
#         self.context.worker.append(model)

#     def get_worker_by_norm_id(self,norm_id):
#         items = self.get_worker_norm_by_norm_id(norm_id)
#         return self._linq_worker.where(lambda x: x.id in [item.id for item in items]).to_list()
 
#     def get_worker_by_work_id(self,work_id):
#         items = self.get_worker_work_by_work_id(work_id)
#         return self._linq_worker.where(lambda x: x.id in [item.id for item in items]).to_list()
    
#     def get_worker_by_id(self,id:str):
#         if not self.worker:
#             return None
#         list = Enumerable(self.worker).where(lambda x: x.id == id)
#         return list[0] if list else None        

#     def get_worker_by_key(self,key:str):
#         if not self.worker:
#             return None
#         list = self._linq_worker.where(lambda x: key.lower() in x.id.lower() or key.lower() in x.name.lower())
#         return list

#     def delete_worker(self,model):
#         self.context.worker.remove(model)
#         return True

# ############################################ machine
#     @property
#     def machine(self):
#         return self.context.machine

#     @property
#     def machine_count(self):
#         return len(self.machine)

#     @property
#     def _linq_machine(self):
#         return Enumerable(self.context.machine)

#     def get_machine_by_work_id(self,work_id):
#         items = self.get_machine_work_by_work_id(work_id)
#         return self._linq_machine.where(lambda x: x.id in [item.id for item in items]).to_list()

#     def get_machine_by_norm_id(self,norm_id):
#         items = self.get_machine_norm_by_norm_id(norm_id)
#         return self._linq_machine.where(lambda x: x.id in [item.id for item in items]).to_list()
       
#     def get_machine_by_id(self,id:str):
#         if not self.machine:
#             return None
#         list = Enumerable(self.machine).where(lambda x: x.id == id)
#         return list[0] if list else None

#     def get_machine_by_key(self,key:str):
#         if not self.machine:
#             return None
#         list = self._linq_machine.where(lambda x: key.lower() in x.id.lower() or key.lower() in x.name.lower())
#         return list
   
#     def insert_machine(self,model):
#         self.context.machine.append(model)    

#     def delete_machine(self,model):
#         self.context.machine.remove(model)
#         return True
############################################ material  
    # @property
    # def material_count(self):
    #     return len(self.material)
       
    # @property
    # def material(self):
    #     return self.context.material
    
    # @property
    # def _linq_material(self):
    #     return Enumerable(self.context.material)
    
    # def get_material_by_work_id(self,work_id):
    #     items = self.get_material_work_by_work_id(work_id)
    #     return self._linq_material.where(lambda x: x.id in [item.id for item in items]).to_list()
    
    # def get_material_by_norm_id(self,norm_id):
    #     items = self.get_material_norm_by_norm_id(norm_id)
    #     return self._linq_material.where(lambda x: x.id in [item.id for item in items]).to_list()
    
    def save_change(self,path):
        self.context.path = path
        self.context.save_change()
        return True
        
    def save_path(self,path):
        self.context.path = path
        
    def load_file(self,path):
        self.context.path = path
        self.context.load()


    def update_ntcv(self,id,model:Models.ntcv):
        old = self.get_ntcv_by_id(id=id)
        old.name = model.name
        old.dateNT = model.dateNT
        old.dateYC = model.dateYC
        return True
    
    
    def update_lmtn(self,id,model:Models.lmtn):
        old = self.get_lmtn_by_id(id=id)
        old.name = model.name
        old.dateNT = model.dateNT
        old.dateYC = model.dateYC
        old.sltm = model.sltm
        old.slm = model.slm
        old.ktm = model.ktm
        return True
    
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



    def is_ntcv_exist(self,id):
        return True if self.get_ntcv_by_id(id) else False

    def update_ntcv(self,id,model:Models.ntcv):
        old = self.get_ntcv_by_id(id=id)
        old.name = model.name
        old.dateNT = model.dateNT
        old.dateYC = model.dateYC
        return True


    def update(self,old,new):
        pass
        

    def count_item(self,what:str):
        return len(self.whats[what])

    def get_item(self,what:str,match_mode=None,logic:str=False,to_lower=False,**kwargs):
        """get item from repository

        Args:
            what (str): what list of data to get
            match_mode (_type_, optional): 0:exact match, 1:key in value. Defaults to None.
            logic (str, optional): if true search with and operator. Defaults to None.
            to_lower (bool, optional): key and value search to lower if True. Defaults to False.

        Returns:
            _type_: a list of item
        """
        if not kwargs:
            return self.whats[what]
        # elif 'key' in kwargs:
        #     return Enumerable(self.whats[what]).where(lambda x:
        #         kwargs['key'] in x.items['key'] if not to_lower 
        #         else kwargs['key'].to_lower() in x.items['key'].to_lower()).to_list()
        else:
            key, value = kwargs.items()
            return Enumerable(self.whats[what]).where(lambda x:
                value == x.items[key] if not to_lower 
                else value.to_lower() == x.items[key].to_lower()).to_list()            
        
    def insert_item(self,what:str, model):
        """insert item to data

        Args:
            what (str): what data list name to insert
            model (_type_): model to insert
        """
        self.whats[what].insert(model)
        
    def delete_item(self,what:str,model):
        self.whats[what].remove(model)
        return True
        
        

    

        
        
