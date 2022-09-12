import datetime
from itertools import count
import pandas as pd
class worker:
    def __init__(self,id:str,name:str,unit:str) -> None:
        self.id = id
        if ' - ' in name and name.index(' - ') == 0:
            self.name = name[2:].strip()
        else:
            self.name = name.strip()
        self.unit = unit
    
    def to_list(self):
        return [self.id,self.name,self.unit]
    
    def to_save_list(self):
        return [self.__class__.__name__,self.id,self.name,self.unit]
    
    def __repr__(self) -> str:
        return self.name

class machine(worker):
    def __init__(self, id, name, unit) -> None:
        super().__init__(id, name, unit)
        
class material(worker):
    def __init__(self, id, name, unit) -> None:
        super().__init__(id, name, unit)
        
class norm(worker):
    def __init__(self, id, name, unit) -> None:
        super().__init__(id, name, unit)

class worker_norm:
    def __init__(self,norm_id,id,amount) -> None:
        self.norm_id = norm_id
        self.id = id
        self._amount = float(amount)
        
    @property
    def amount(self):
        return round(self._amount,2)
    
    @amount.setter
    def amount(self,amount):
        self._amount = amount
        
    def to_list(self):
        return [self.norm_id,self.id,self.amount]        

    def to_save_list(self):
        return [self.__class__.__name__,self.norm_id,self.id,self.amount]

class machine_norm(worker_norm):
    def __init__(self, norm_id, id, amount) -> None:
        super().__init__(norm_id, id, amount)
        
class material_norm(worker_norm):
    def __init__(self, norm_id, id, amount) -> None:
        super().__init__(norm_id, id, amount)
          
class work:
    id_iter = count()
    def __init__(self,name,unit,amount,hm_id,id=None) -> None:
        self.id = f'W{next(self.id_iter)}' if not id else id
        self.name = name
        self.unit = unit
        self.amount = float(amount)
        self.hm_id = hm_id

    def to_save_list(self):
        return [self.__class__.__name__,self.name,self.unit,self.amount,self.hm_id,self.id]
   
class worker_work:
    def __init__(self,work_id,id,amount) -> None:
        self.work_id = work_id
        self.id = id
        self._amount = float(amount)
        
    @property
    def amount(self):
        return round(self._amount,2)
    
    @amount.setter
    def amount(self,amount):
        self._amount = amount
    
    
    def to_list(self):
        return [self.work_id,self.id,self.amount]   

    def to_save_list(self):
        return [self.__class__.__name__,self.work_id,self.id,self.amount]
        
class machine_work(worker_work):
    def __init__(self, work_id, id, amount) -> None:
        super().__init__(work_id, id, amount)
       
class material_work(worker_work):
    def __init__(self, work_id, id, amount) -> None:
        super().__init__(work_id, id, amount)
    
class hang_muc:
    id_iter = count()
    def __init__(self,name,id=None) -> None:
        self.id = f'HM{next(self.id_iter)}' if not id else id
        self.name = name
        
    def __str__(self) -> str:
        return self.id
        
    def __repr__(self) -> str:
        return self.name

    def to_save_list(self):
        return [self.__class__.__name__,self.name,self.id]
    
class work_time:
    def __init__(self,work_id:str,start:datetime.datetime,end:datetime.datetime) -> None:
        self.work_id = work_id
        self.start = start
        self.end = end
        
    def npd(self):
        return (self.end - self.start).days + 1
    
    def to_list(self):
        return [self.work_id,self.start,self.end]

    def to_save_list(self):
        return [self.__class__.__name__,self.work_id,self.start,self.end]