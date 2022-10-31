import datetime
from itertools import count
import pandas as pd
import numpy as np



class worker:
    def __init__(self,id:str, name:str, unit:str) -> None:
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

    def items(self) -> dict:
        return {'norm_id': self.name, 'id': self.id, 'amount':self.unit}

    def update(self,model:dict):
        self.name = model['name']
        self.unit = model['unit']
    
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

    def update(self,model:dict):
        self.norm_id = model['norm_id']
        self.id = model['id']
        self.amount = model['amount']

    def items(self) -> dict:
        return {'norm_id': self.norm_id, 'id': self.id, 'amount':self.amount}
        
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
    def __init__(self,name,unit,amount,hm_id,pv_id=None,start:datetime.datetime=None,end:datetime.datetime=None,id=None) -> None:
        self.id = 'W{}'.format(next(self.id_iter)) if not id else id
        self.name = name
        self.unit = unit
        self.amount = float(amount)
        self.hm_id = hm_id
        self.pv_id = pv_id if pv_id else 0
        self._start = start
        self._end = end
        
    @property
    def _start_timestamp(self):
        return self._start.timestamp() if self._start else ''
    
    @property
    def _end_timestamp(self):
        return self._end.timestamp() if self._end else ''
    
    @property
    def start(self):
        return self._start.strftime(r'%d/%m/%y') if self._start else ''

    @property
    def end(self):
        return self._end.strftime(r'%d/%m/%y') if self._end else ''

    @property
    def work_day(self):
        if not self._start or not self._end:
            return 0
        return (self._end - self._start + datetime.timedelta(1)).days

    def update(self,model:dict):
        self.name = model['name']
        self.unit = model['unit']
        self.amount = model['amount']
        self.hm_id = model['hm_id']
        self.pv_id = model['pv_id']
        self._start = model['_start']
        self._end = model['_end']
        
    def items(self) -> dict:
        return {'id': self.id, 'name': self.name, 'unit': self.unit, 'amount':self.amount,
                'hm_id': self.hm_id, 'pv_id': self.pv_id, 'start': self.start, 'end':self.end}

    def to_save_list(self):
        return [self.__class__.__name__,self.name,self.unit,self.amount,self.hm_id,self._start_timestamp,self._end_timestamp,self.id]
   
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

    def update(self,model:dict):
        self.work_id = model['work_id']
        self.id = model['id']
        self.amount = model['amount']

    def items(self) -> dict:
        return {'work_id': self.work_id, 'id': self.id, 'amount':self.amount}
    
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
        self.id = next(self.id_iter) if not id else id
        self.name = name
        
    def __str__(self) -> str:
        return self.name
        
    def __repr__(self) -> str:
        return ' '.join(self.to_save_list())
    
    def update(self,model:dict):
        self.name = model['name']

    def items(self) -> dict:
        return {'name': self.name,'id': self.id}

    def to_save_list(self):
        return [self.__class__.__name__,self.name,self.id]

class phan_viec(hang_muc):
    id_iter = count()
    def __init__(self, name, id=None) -> None:
        super().__init__(name, id)
        self.id = next(self.id_iter) if not id else id
        
class ntcv:
    id_iter = count()
    morning = [7 + i*0.5 for i in range(7)]
    afternoon = [13.5 + i*0.5 for i in range(5)]
    all_day = morning + afternoon
    np.random.seed(1111)
    def __init__(self,name,
                 work_id=None,
                 dateNT:datetime.datetime=None,
                 dateYC:datetime.datetime=None,
                 id=None) -> None:
        self.work_id = work_id if work_id else 'ztcv'
        self.name = name
        self._dateNT = dateNT + datetime.timedelta(hours= np.random.choice(self.all_day)) if dateNT else None
        self._dateYC = None if not dateNT else self._dateNT - datetime.timedelta(days= 1) if not dateYC else dateYC
        self.id = next(self.id_iter) if not id else id
        
    @property
    def _dateNT_timestamp(self):
        return self._dateNT.timestamp() if self._dateNT else ''

    @property
    def _dateYC_timestamp(self):
        return self._dateYC.timestamp() if self._dateYC else ''
        
    @property
    def dateNT(self):
        return self._dateNT.strftime(r'%d/%m/%y %H:%M') if self._dateNT else ''

    @property
    def dateYC(self):
        return self._dateYC.strftime(r'%d/%m/%y %H:%M') if self._dateYC else ''
    
    
    def update(self,model:dict):
        self.name = model['name']
        self.dateNT = model['dateNT']
        self.dateYC = model['dateYC']
        
    def items(self) -> dict:
        return {'dateNT': self._dateNT, 'dateYC': self._dateYC,
                'name': self.name,'id': self.id}
    
    def __str__(self) -> str:
        return self.name
    
    def to_save_list(self):
        return [self.__class__.__name__,self.name,self.work_id,self._dateNT_timestamp,self._dateYC_timestamp,self.id]
    
class lmtn(ntcv):
    id_iter = count()
    np.random.seed(2222)
    def __init__(self, name, work_id=None,
                 dateNT: datetime.datetime = None,
                 dateYC: datetime.datetime = None,
                 sltm = None, slm = None, ktm = None, yc=None,
                 id = None) -> None:
        super().__init__(name, work_id, dateNT, dateYC, id)
        self.id = next(self.id_iter) if not id else id
        self.sltm = sltm
        self.slm = slm
        self.ktm = ktm
        self.yc = yc
        
    def update(self,model:dict):
        self.name = model['name']
        self.dateNT = model['dateNT']
        self.dateYC = model['dateYC']
        self.sltm = model['sltm']
        self.slm = model['slm']
        self.ktm = model['ktm']
        self.yc = model['yc']
        
    def items(self) -> dict:
        return {'name': self.name, 'id': self.id,
                'dateNT': self._dateNT, 'dateYC': self._dateYC,
                'sltm': self.sltm, 'slm': self.slm, 'ktm': self.ktm, 'yc': self.yc,}
    
    def to_save_list(self):
        return [self.__class__.__name__,
                self.name, self.work_id,
                self._dateNT_timestamp,self._dateYC_timestamp,
                self.sltm, self.slm, self.ktm,
                self.id]
        
class ntvl(ntcv):
    id_iter = count()
    np.random.seed(3333)
    def __init__(self, name, work_id=None, dateNT: datetime.datetime = None, dateYC: datetime.datetime = None, id=None) -> None:
        super().__init__(name, work_id, dateNT, dateYC, id) 
        self.id = next(self.id_iter) if not id else id
           
           
models = {'worker':worker, 'machine': machine, 'material': material,
          'worker_norm':worker_norm, 'machine_norm': machine_norm, 'material_norm': material_norm,
          'worker_work':worker_work, 'machine_work': machine_work, 'material_norm': material_work,
          'norm': norm, 'work': work, 'hang_muc': hang_muc, 'phan_viec': phan_viec,
          'lmtn': lmtn, 'ntvl': ntvl, 'ntcv': ntcv,}

def main():
    a = models['worker'](1,'a','b')
    print(a.name)

if __name__ == "__main__":
    main()