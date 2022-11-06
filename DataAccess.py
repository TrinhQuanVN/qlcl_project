import csv
import Models

class data_access:
    items = {'worker' : [], 'machine' : [],'material' : [],
            'worker_norm' : [],'machine_norm' : [], 'material_norm' : [],
            'worker_work' : [], 'machine_work' : [], 'material_work' : [],
            'norm' : [], 'work' : [], 'hang_muc' : [], 'phan_viec' : [],
            'ntcv' : [], 'lmtn' : [],'ntvl' : [],}

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
                                id='df5'),]

    def __init__(self,path=None) -> None:
        self.path = path
        
    def load(self):
        if self.path:
            with open(self.path,'r',newline='',encoding='utf-8') as file:
                reader = csv.reader(file,delimiter='&')
                for row in reader:
                    self.items[row[0]].append(Models.models[row[0]](*row[1:]))
        if not self.items['hang_muc']:
            self.items['hang_muc'].append(Models.hang_muc('Hạng mục mặc định'))

        if not self.items['phan_viec']:
            self.items['phan_viec'].append(Models.phan_viec('Phần việc mặc định'))
                       
    def save_change(self):
        if self.path:
            with open(self.path,'w',newline='',encoding='utf-8') as file:
                write = csv.writer(file,delimiter='&')
                for key, item in self.items.items():
                    write.writerows([_.to_save_list() for _ in item])
    
def main():
    data = data_access()
    print(Models.lmtn.id_iter) 
    print(Models.ntcv.id_iter)    
       
    
if __name__ == "__main__":
    main()            
                                                                            
        