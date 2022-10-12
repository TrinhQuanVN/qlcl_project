import csv
import Models

class data_access:
    machine = []
    material = []
    worker = []
    norm = []
    
    machine_norm = []
    material_norm = []
    worker_norm = []
 
    machine_work = []
    material_work = []
    worker_work = []
       
    work = []
    work_time = []
    worker_work_time = []
    hang_muc = []
    
    def __init__(self,path) -> None:
        self.path = path
        
    def load(self):
        if self.path:
            with open(self.path,'r',newline='',encoding='utf-8') as file:
                reader = csv.reader(file,delimiter='&')
                for row in reader:
                    if Models.worker.__name__ in row:
                        self.worker.append(Models.worker(*row[1:]))
                        
                    if Models.machine.__name__ in row:
                        self.machine.append(Models.machine(*row[1:]))
                        
                    if Models.material.__name__ in row:
                        self.material.append(Models.material(*row[1:]))
                        
                    if Models.norm.__name__ in row:
                        self.norm.append(Models.norm(*row[1:]))
                        
                    if Models.worker_norm.__name__ in row:
                        self.worker_norm.append(Models.worker_norm(*row[1:]))
                        
                    if Models.machine_norm.__name__ in row:
                        self.machine_norm.append(Models.machine_norm(*row[1:]))
                        
                    if Models.material_norm.__name__ in row:
                        self.material_norm.append(Models.material_norm(*row[1:]))
                        
                    if Models.work.__name__ in row:
                        self.work.append(Models.work(*row[1:]))
                        
                    if Models.worker_work.__name__ in row:
                        self.worker_work.append(Models.worker_work(*row[1:]))
                        
                    if Models.machine_work.__name__ in row:
                        self.machine_work.append(Models.machine_work(*row[1:]))
                        
                    if Models.material_work.__name__ in row:
                        self.material_work.append(Models.material_work(*row[1:]))
                        
                    if Models.hang_muc.__name__ in row:
                        self.hang_muc.append(Models.hang_muc(*row[1:]))
                        
                    if Models.work_time.__name__ in row:
                        self.work_time.append(Models.work_time(*row[1:]))                                                                                                       
    def save_change(self):
        if self.path:
            with open(self.path,'w',newline='',encoding='utf-8') as file:
                write = csv.writer(file,delimiter='&')
                
                if self.worker:
                    for item in self.worker:
                        write.writerows([item.to_save_list()])       
                                                                                                                                  
                if self.machine:
                    for item in self.machine:
                        write.writerows([item.to_save_list()]) 
                        
                if self.material:
                    for item in self.material:
                        write.writerows([item.to_save_list()])                 

                if self.worker_norm:
                    for item in self.worker_norm:
                        write.writerows([item.to_save_list()]) 
                        
                if self.machine_norm:
                    for item in self.machine_norm:
                        write.writerows([item.to_save_list()]) 
                        
                if self.material_norm:
                    for item in self.material_norm:
                        write.writerows([item.to_save_list()])                

                if self.norm:
                    for item in self.norm:
                        write.writerows([item.to_save_list()])
                
                if self.hang_muc:
                    for item in self.hang_muc:
                        write.writerows([item.to_save_list()])
                        
                if self.work:
                    for item in self.work:
                        write.writerows([item.to_save_list()]) 
                                        
                if self.worker_work:
                    for item in self.worker_work:
                        write.writerows([item.to_save_list()])
                          
                if self.machine_work:
                    for item in self.machine_work:
                        write.writerows([item.to_save_list()]) 
                         
                if self.material_work:
                    for item in self.material_work:
                        write.writerows([item.to_save_list()])

                if self.work_time:
                    for item in self.work_time:
                        write.writerows([item.to_save_list()])                        
 
                        
    
                        
                                                                            
        