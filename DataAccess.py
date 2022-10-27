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
    phan_viec = []
    
    ntcv = []
    lmtn = []

    default_lmtn = [Models.lmtn('Bê tông M250, đá 1x2, PCB40, phụ gia R7',
                                sltm= 1, slm= 3, ktm= '15x15x15cm',
                                yc= 'Xác định cường độ mác bê tông R7,R28 có phụ gia R7',
                                id='df0'),
                    
                    Models.lmtn('Bê tông M250, đá 1x2, PCB40',
                                sltm= 1, slm= 3, ktm= '15x15x15cm',
                                yc= 'Xác định cường độ mác bê tông R7,R28',
                                id='df1'),
                    
                    Models.lmtn('Bê tông M200, đá 1x2, PCB30',
                                sltm= 1, slm= 3, ktm= '15x15x15cm',
                                yc= 'Xác định cường độ mác bê tông R7,R28',
                                id='df2'),  
                    
                    Models.lmtn('Bê tông M150, đá 4x6, PCB30',
                                sltm= 1, slm= 3, ktm= '15x15x15cm',
                                yc= 'Xác định cường độ mác bê tông R7,R28',
                                id='df3'),                    

                    Models.lmtn('Vữa xi măng M100, PCB30',
                                sltm= 1, slm= 3, ktm= '7.07x7.07x7.07cm',
                                yc= 'Xác định cường độ vữa XM R7,R28',
                                id='df4'),

                    Models.lmtn('Vữa xi măng M75, PCB30',
                                sltm= 1, slm= 3, ktm= '7.07x7.07x7.07cm',
                                yc= 'Xác định cường độ vữa XM R7,R28',
                                id='df5'),
                                                           
                    ]

    
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

                    if Models.phan_viec.__name__ in row:
                        self.phan_viec.append(Models.phan_viec(*row[1:]))
                        
                    if Models.ntcv.__name__ in row:
                        self.ntcv.append(Models.ntcv(*row[1:]))
                        
                    if Models.lmtn.__name__ in row:
                        self.lmtn.append(Models.lmtn(*row[1:]))                                             
                        
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

                if self.phan_viec:
                    for item in self.phan_viec:
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

                if self.ntcv:
                    for item in self.ntcv:
                        write.writerows([item.to_save_list()]) 
                        
                if self.lmtn:
                    for item in self.lmtn:
                        write.writerows([item.to_save_list()])                        
                        
    
                        
                                                                            
        