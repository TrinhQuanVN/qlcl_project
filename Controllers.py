from datetime import date, datetime
import re
import pandas as pd
import itertools
import Views
import Repository
import Models
import PySimpleGUI as sg
import Extension as ex
from py_linq import Enumerable
from GUI import GRAPH_SIZE


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

############################################ work time
    def edit_wrok_time(self,work_id,model:Models.work_time=None):
        if not model:
            work_time = self.Repository.get_work_time_by_work_id(work_id)
            self.Render(Views.work_time_update_view,work_time=work_time)
            return
        if self.Repository.update_work_time(work_id,model):
            print(f'work time {work_id} is updated')
    
    def draw_work_time(self,start=None,end=None):
        if not start and not end:
            self._draw_work_time()
            return
        self._draw_work_time(start,end)

    def _draw_work_time(self,start:datetime=None,end:datetime=None):
        class coordinate:
            def __init__(self,x,y) -> None:
                self.x = x
                self.y = y
            def add_x(self,x):
                self.x += x
                
            def add_y(self,y):
                self.y += y
            @property
            def coordinate(self):
                return (self.x,self.y)
            
            def __add__(self, other):
                return self.__class__(*[self.x+other.x,self.y+other.y])
            
            def __repr__(self) -> set:
                return (self.x,self.y)
            
        def draw_line(graph,point_from:coordinate,point_to:coordinate,color='white',width=1):
            graph.draw_line(point_from=point_from.coordinate,point_to=point_to.coordinate,color=color,width=width)

        def draw_rectangle(graph,top_left:coordinate,bottom_right:coordinate,line_color='blue',line_width=1,fill_color=None):
            graph.draw_rectangle(top_left=top_left.coordinate,bottom_right=bottom_right.coordinate,line_color=line_color,line_width=1,fill_color=fill_color)
            
        def draw_text(graph,text,location:coordinate,color='white',font=('Any',9),angle=0,text_location=sg.TEXT_LOCATION_RIGHT):
            graph.draw_text(text=text,location=location.coordinate,color=color,font=font,angle=angle,text_location=text_location)
                        

        wts = self.Repository.get_work_time_by_start_end(start,end) if start and end else self.Repository.work_time
        wts_time_not_null = Enumerable(wts).where(lambda x: x.start and x.end).to_list()
        work_count = len(wts)
        if wts and wts_time_not_null:
            day_count = (end - start).days + 1 if start and end else (max([wt.end for wt in wts_time_not_null]) - min([wt.start for wt in wts_time_not_null])).days + 1
        else:
            day_count = 1
        min_cao_between = 10
        min_rong_between = 15
        
        max_x,max_y = GRAPH_SIZE
        DISTANCE_KHUNG_DEN_TRUC = 10
        DISTANCE_VIEN_KHUNG = 5
        DISTANCE_GIUA_2_KHUNG = 10
        
        WIDTH_CHU_VIET = 20
        HEIGHT_CHU_VIET = 20
        RONG_KHUNG_1 = max_x - DISTANCE_VIEN_KHUNG*2
        RONG_KHUNG_2 = max_x - DISTANCE_VIEN_KHUNG*2
        CAO_KHUNG_1 = 120
        CAO_KHUNG_2 = max_y - DISTANCE_VIEN_KHUNG*2 - DISTANCE_GIUA_2_KHUNG
        
        goc_toa_do_1 = coordinate(DISTANCE_VIEN_KHUNG+WIDTH_CHU_VIET,DISTANCE_VIEN_KHUNG+HEIGHT_CHU_VIET)
        goc_toa_do_2 = coordinate(DISTANCE_VIEN_KHUNG+WIDTH_CHU_VIET,DISTANCE_VIEN_KHUNG+CAO_KHUNG_1+DISTANCE_GIUA_2_KHUNG+HEIGHT_CHU_VIET)
        graph = self.window['-GRAPH-']
        # xóa
        graph.erase()
        # vẽ khung đồ thị 1
        top_left=coordinate(DISTANCE_VIEN_KHUNG,CAO_KHUNG_1+DISTANCE_VIEN_KHUNG)
        bottom_right=coordinate(max_x-DISTANCE_VIEN_KHUNG,DISTANCE_VIEN_KHUNG)
        draw_rectangle(graph,top_left,bottom_right)
        # vẽ khung đồ thị 2
        top_left=coordinate(DISTANCE_VIEN_KHUNG,max_y-DISTANCE_VIEN_KHUNG)
        bottom_right=coordinate(max_x-DISTANCE_VIEN_KHUNG,CAO_KHUNG_1+DISTANCE_GIUA_2_KHUNG+DISTANCE_VIEN_KHUNG)
        draw_rectangle(graph,top_left,bottom_right)
        
        # vẽ trục tọa độ đồ thị 1
        point_to1 = coordinate(max_x-DISTANCE_VIEN_KHUNG-5,DISTANCE_VIEN_KHUNG+HEIGHT_CHU_VIET)
        point_to2 = coordinate(DISTANCE_VIEN_KHUNG+WIDTH_CHU_VIET,DISTANCE_VIEN_KHUNG+CAO_KHUNG_1-5)
        draw_line(graph,goc_toa_do_1,point_to1)
        draw_line(graph,goc_toa_do_1,point_to2)
        
        # vẽ trục tọa độ đồ thị 2
        point_to1 = coordinate(max_x-DISTANCE_VIEN_KHUNG-5,DISTANCE_VIEN_KHUNG+CAO_KHUNG_1+HEIGHT_CHU_VIET+DISTANCE_GIUA_2_KHUNG)
        point_to2 = coordinate(DISTANCE_VIEN_KHUNG+HEIGHT_CHU_VIET,max_y-DISTANCE_VIEN_KHUNG-5)
        draw_line(graph,goc_toa_do_2,point_to1)
        draw_line(graph,goc_toa_do_2,point_to2)
        
        if wts:
            cao_between = min_cao_between if min_cao_between > CAO_KHUNG_2/work_count else CAO_KHUNG_2/work_count
            rong_between = min_rong_between if min_rong_between > RONG_KHUNG_2/day_count else RONG_KHUNG_2/day_count
            
            for num, wt in enumerate(wts):
                text = wt.work_id
                location=(goc_toa_do_2+coordinate(0,(num+1)*cao_between))
                draw_text(graph,text,location)
                
    def create_work_time(self,model:Models.work_time):
        self.Repository.insert_work_time(model)
        
    def inital_work_time(self):
        if not self.Repository.work_count == self.Repository.work_time_count:
            work_id_not_in_work_time_yet = self.Repository._linq_work.where(lambda x: x.id not in [x.work_id for x in self.Repository.work_time]).to_list()
            for id in [x.id for x in work_id_not_in_work_time_yet]:
                self.create_work_time(Models.work_time(id,None,None))
                
    def list_work_time(self,start:datetime=None,end:datetime=None):
        if not start and not end:
            self._list_work_time(self.Repository.work_time)
            return
        self._list_work_time(self.Repository.get_work_time_by_start_end(start,end))

    def _list_work_time(self,work_time):
        dtree = sg.TreeData()
        for item in work_time:
            start = ex.display_date_time(item.start) if item.start else ''
            end = ex.display_date_time(item.end) if item.end else ''
            dtree.insert('',item.work_id,item.work_id,[start,end])
        self.window['-TREE TIME-'].update(dtree)
############################################ work
    def create_copy_work(self,id):
        model = self.Repository.get_work_by_id(id)
        stt = self.Repository._linq_work.where(lambda x: len(x.id) >8 and x.id[:8].lower() == id.lower()).to_list()
        copy_id = model.id + f"_copy{len(stt)}"
        copy_model = Models.work(model.name,model.unit,model.amount,model.hm_id,copy_id)
        self.create_work(model=copy_model)
        
        worker_work = self.Repository.get_worker_work_by_work_id(id)
        if worker_work:
            for item in worker_work:
                self.create_worker_work(Models.worker_work(copy_model.id,item.id,item.amount))
                
        machine_work = self.Repository.get_machine_work_by_work_id(id)
        if machine_work:
            for item in machine_work:
                self.create_machine_work(Models.machine_work(copy_model.id,item.id,item.amount)) 
                
        material_work = self.Repository.get_material_work_by_work_id(id)
        if material_work:
            for item in material_work:
                self.create_material_work(Models.material_work(copy_model.id,item.id,item.amount))
                
        self.list_work()
                                   
    def delete_work(self,id):
        model = self.Repository.get_work_by_id(id)
        if model:
            if self.Repository.delete_work(model):
                print(f'work {model.id} is deleted')
        
    def edit_work(self,id,model=None):
        if not self.Repository.is_work_exist(id):
            print('work {id} is not existed')
            return
        if not model:
            hang_mucs = self.Repository.hang_muc
            work = self.Repository.get_work_by_id(id)
            hang_muc = self.Repository.get_hang_muc_by_id(work.hm_id)
            
            worker_work = self.Repository.get_worker_work_by_work_id(id)
            machine_work = self.Repository.get_machine_work_by_work_id(id)
            material_work = self.Repository.get_material_work_by_work_id(id)
            
            worker = self.Repository.get_worker_by_work_id(id)
            machine = self.Repository.get_machine_by_work_id(id)
            material = self.Repository.get_material_by_work_id(id)
            self.Render(Views.work_edit_view,
                        hang_mucs=hang_mucs,hang_muc=hang_muc,
                        work=work,
                        worker_work=worker_work,machine_work=machine_work,material_work=material_work,
                        worker=worker, machine=machine, material=material,
                        workers=self.Repository.worker,materials=self.Repository.material,machines=self.Repository.machine)
            return
        if self.Repository.update_work(id,model):
            print(f'work {id} is updated')
        else:
            print(f'work {id} is not updated')
    
    def create_work(self,norm_id=None,model=None):
        if not model:
            hang_muc = self.Repository.hang_muc
            if not norm_id:
                self.Render(Views.work_create_view,hang_muc=hang_muc,worker=self.Repository.worker,material=self.Repository.material,machine=self.Repository.machine)
                return
            else:
                norm = self.Repository.get_norm_by_id(norm_id)
                worker_norm = self.Repository.get_worker_norm_by_norm_id(norm_id)
                machine_norm = self.Repository.get_machine_norm_by_norm_id(norm_id)
                material_norm = self.Repository.get_material_norm_by_norm_id(norm_id)
                
                worker = self.Repository.get_worker_by_norm_id(norm_id)
                machine = self.Repository.get_machine_by_norm_id(norm_id)
                material = self.Repository.get_material_by_norm_id(norm_id)                
                self.Render(Views.work_create_with_norm_id_view,
                    hang_muc=hang_muc,
                    id=id,
                    worker=worker,machine=machine,material=material,
                    norm=norm,worker_norm=worker_norm,machine_norm=machine_norm,material_norm=material_norm,
                    workers=self.Repository.worker,materials=self.Repository.material,machines=self.Repository.machine)
                return                
        self.Repository.insert_work(model)
        print(f'work {model.id} is created')
     
    def count_work(self,count=None):
        num = count if count else self.Repository.work_count
        self.Update(key='-WORK COUNT TEXT-',values=num)
        
    def list_work(self,key=None):
        if not key:
            self._list_work(self.Repository.work,self.Repository.hang_muc)
            print('work list showed!')
            return
        self._list_work(self.Repository.get_work_by_key(key))
        print(f'work list with key {key} is showed !')
            
    def _list_work(self,works:list,hang_muc:list):
        treedata = sg.TreeData()
        for item in hang_muc:
            treedata.Insert('',item.id,item.name,[item.id])
            
        for item in works:
            treedata.Insert(item.hm_id,item.id,item.name,[item.id,item.unit,item.amount])
            
            worker_works = self.Repository.get_worker_work_by_work_id(item.id)
            if worker_works:
                for x in worker_works:
                    y = self.Repository.get_worker_by_id(x.id)
                    treedata.Insert(x.work_id,x.id,y.name,[y.id,y.unit,x.amount])
                    
            machine_works = self.Repository.get_machine_work_by_work_id(item.id)
            if machine_works:
                for x in machine_works:
                    y = self.Repository.get_machine_by_id(x.id)
                    treedata.Insert(x.work_id,x.id,y.name,[y.id,y.unit,x.amount])                    

            material_works = self.Repository.get_material_work_by_work_id(item.id)
            if material_works:
                for x in material_works:
                    y = self.Repository.get_material_by_id(x.id)
                    treedata.Insert(x.work_id,x.id,y.name,[y.id,y.unit,x.amount])
                    
        self.Update(key='-TREE WORK-',values=treedata)
        self.count_work(len(works))

 
############################################ worker work
    def create_worker_work(self,model):
        self.Repository.insert_worker_work(model)
        print(f'workerwork is created') 
        
    def update_worker_work(self,work_id,id,model=None):
        if not model:
            Views.work().Render(workers=self.Repository.worker,worker_work=self.Repository.get_worker_work(work_id,id))
            return
        if self.Repository.update_worker_work(work_id,id,model):
            print(f'worker {model.id} of work {model.work_id} is updated')
    
    def delete_worker_work(self,work_id,id):
        model = Enumerable(self.Repository.get_worker_work_by_work_id(work_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_worker_work(model)
        
    def delete_worker_work_by_work_id(self,work_id:str):
        models = self.Repository.get_worker_work_by_work_id(work_id)
        if models:
            for model in models:
                if self.Repository.delete_worker_work(model):
                    print(f'worker {model.id} of work {model.work_id} is deleted ')
    
    def create_worker_work(self,model):
        self.Repository.insert_worker_work(model)
        print(f'workerwork is created')
############################################ machine work
    def create_machine_work(self,model):
        self.Repository.insert_machine_work(model)
        print(f'machinework is created') 

    def update_machine_work(self,work_id,id,model=None):
        if not model:
            Views.work().Render(machines=self.Repository.machine,machine_work=self.Repository.get_machine_work(work_id,id))
            return
        if self.Repository.update_machine_work(work_id,id,model):
            print(f'machine {model.id} of work {model.work_id} is updated')
    
    def delete_machine_work(self,work_id,id):
        model = Enumerable(self.Repository.get_machine_work_by_work_id(work_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_machine_work(model)
        
    def delete_machine_work_by_work_id(self,work_id:str):
        models = self.Repository.get_machine_work_by_work_id(work_id)
        if models:
            for model in models:
                if self.Repository.delete_machine_work(model):
                    print(f'machine {model.id} of work {model.work_id} is deleted ')
    
    def create_machine_work(self,model):
        self.Repository.insert_machine_work(model)
        print(f'machinework is created')        

############################################ material work
    def create_material_work(self,model):
        self.Repository.insert_material_work(model)
        print(f'materialwork is created') 

    def update_material_work(self,work_id,id,model=None):
        if not model:
            Views.work().Render(materials=self.Repository.material,material_work=self.Repository.get_material_work(work_id,id))
            return
        if self.Repository.update_material_work(work_id,id,model):
            print(f'material {model.id} of work {model.work_id} is updated')
    
    def delete_material_work(self,work_id,id):
        model = Enumerable(self.Repository.get_material_work_by_work_id(work_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_material_work(model)
        
    def delete_material_work_by_work_id(self,work_id:str):
        models = self.Repository.get_material_work_by_work_id(work_id)
        if models:
            for model in models:
                if self.Repository.delete_material_work(model):
                    print(f'material {model.id} of work {model.work_id} is deleted ')
    
    def create_material_work(self,model):
        self.Repository.insert_material_work(model)
        print(f'materialwork is created')
        
############################################ norm
    def create_copy_norm(self,id):
        model = self.Repository.get_norm_by_id(id)
        stt = self.Repository._linq_norm.where(lambda x: len(x.id) >8 and x.id[:8].lower() == id.lower()).to_list()
        print(stt)
        copy_id = model.id + f"_copy{len(stt)}"
        copy_model = Models.norm(copy_id,model.name,model.unit)
        self.create_norm(copy_model)
        
        worker_norm = self.Repository.get_worker_norm_by_norm_id(id)
        if worker_norm:
            for item in worker_norm:
                self.create_worker_norm(Models.worker_norm(copy_model.id,item.id,item.amount))
                
        machine_norm = self.Repository.get_machine_norm_by_norm_id(id)
        if machine_norm:
            for item in machine_norm:
                self.create_machine_norm(Models.machine_norm(copy_model.id,item.id,item.amount)) 
                
        material_norm = self.Repository.get_material_norm_by_norm_id(id)
        if material_norm:
            for item in material_norm:
                self.create_material_norm(Models.material_norm(copy_model.id,item.id,item.amount))
                
        self.list_norm()
                                   
    def delete_norm(self,id):
        model = self.Repository.get_norm_by_id(id)
        if model:
            if self.Repository.delete_norm(model):
                print(f'norm {model.id} is deleted')
        
    def edit_norm(self,id,model=None):
        if not self.Repository.is_norm_exist(id):
            print('norm {id} is not existed')
            return
        if not model:
            norm = self.Repository.get_norm_by_id(id)
            worker_norm = self.Repository.get_worker_norm_by_norm_id(id)
            machine_norm = self.Repository.get_machine_norm_by_norm_id(id)
            material_norm = self.Repository.get_material_norm_by_norm_id(id)
            
            worker = self.Repository.get_worker_by_norm_id(id)
            machine = self.Repository.get_machine_by_norm_id(id)
            material = self.Repository.get_material_by_norm_id(id)
            self.Render(Views.norm_edit_view,norm=norm,
                                        worker_norm=worker_norm,machine_norm=machine_norm,material_norm=material_norm,
                                        worker=worker, machine=machine, material=material,
                                        workers=self.Repository.worker,materials=self.Repository.material,machines=self.Repository.machine)
            return
        if self.Repository.update_norm(id,model):
            print(f'norm {id} is updated')
        else:
            print(f'norm {id} is not updated')
    
    def create_norm(self,model=None):
        if not model:
            self.Render(Views.norm_create_view,worker=self.Repository.worker,material=self.Repository.material,machine=self.Repository.machine)
            return
        self.Repository.insert_norm(model)
        print(f'norm {model.id} is created')
     
    def count_norm(self,count=None):
        num = count if count else self.Repository.norm_count
        self.Update(key='-NORM COUNT TEXT-',values=num)
        
    def list_norm(self,key=None):
        if self.Repository.norm:
            if not key:
                self._list_norm(self.Repository.norm)
                print('norm list showed!')
                return
            self._list_norm(self.Repository.get_norm_by_key(key=key))
            print(f'norm list with key {key} is showed !')
            
    def _list_norm(self,norms:list):
        treedata = sg.TreeData()
        if not norms:
            self.Update(key='-TREE NORM-',values=treedata)
            self.count_norm(0)
        for item in norms:
            treedata.Insert('',item.id,item.name,[item.id,item.unit])
            
            worker_norms = self.Repository.get_worker_norm_by_norm_id(item.id)
            if worker_norms:
                for x in worker_norms:
                    y = self.Repository.get_worker_by_id(x.id)
                    treedata.Insert(x.norm_id,x.id,y.name,[y.id,y.unit,x.amount])
                    
            machine_norms = self.Repository.get_machine_norm_by_norm_id(item.id)
            if machine_norms:
                for x in machine_norms:
                    y = self.Repository.get_machine_by_id(x.id)
                    treedata.Insert(x.norm_id,x.id,y.name,[y.id,y.unit,x.amount])                    

            material_norms = self.Repository.get_material_norm_by_norm_id(item.id)
            if material_norms:
                for x in material_norms:
                    y = self.Repository.get_material_by_id(x.id)
                    treedata.Insert(x.norm_id,x.id,y.name,[y.id,y.unit,x.amount])
                    
        self.Update(key='-TREE NORM-',values=treedata)
        self.count_norm(len(norms))
                 
    def create_from_excel(self,path=None):
        if not path:
            self.Render(Views.create_norm_from_excel_view)
            return
        count = self._read_excel_get_norm(path)
        print(f'{count} norms have been created successfully')
            
    def _read_excel_get_norm(self,path):
        values = ex.read_excel(path)
        count = 0
        for row in values:
            if ex.is_norm(row[1]) and not self.Repository.is_norm_exist(row[1]):
                count +=1
                self.Repository.insert_norm(Models.norm(*row[1:4]))

            if ex.is_norm(row[0]) and ex.is_worker(row[1]):
                if not self.Repository.worker or not self.Repository.get_worker_by_id(row[1]):
                    self.Repository.insert_worker(Models.worker(*row[1:4]))
                self.Repository.insert_worker_norm(Models.worker_norm(row[0],row[1],row[-1]))
                
            elif ex.is_norm(row[0]) and ex.is_machine(row[1]) or ex.is_dif_machine(row[1]):
                if not self.Repository.machine or not self.Repository.get_machine_by_id(row[1]):
                    self.Repository.insert_machine(Models.machine(*row[1:4]))
                self.Repository.insert_machine_norm(Models.machine_norm(row[0],row[1],row[-1]))

            elif ex.is_norm(row[0]) and ex.is_material(row[1]) or ex.is_dif_material(row[1]):
                if not self.Repository.material or not self.Repository.get_material_by_id(row[1]):
                    self.Repository.insert_material(Models.material(*row[1:4]))
                self.Repository.insert_material_norm(Models.material_norm(row[0],row[1],row[-1]))
                
        return count
  
############################################ worker norm
    def create_worker_norm(self,model):
        self.Repository.insert_worker_norm(model)
        print(f'worker_norm is created')

    def update_worker_norm(self,norm_id,id,model=None):
        if not model:
            Views.worker_norm_update_view().Render(workers=self.Repository.worker,worker_norm=self.Repository.get_worker_norm(norm_id,id))
            return
        if self.Repository.update_worker_norm(norm_id,id,model):
            print(f'worker {model.id} of norm {model.norm_id} is updated')
    
    def delete_worker_norm(self,norm_id,id):
        model = Enumerable(self.Repository.get_worker_norm_by_norm_id(norm_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_worker_norm(model)
        
    def delete_by_norm_id(self,norm_id:str):
        models = self.Repository.get_worker_norm_by_norm_id(norm_id)
        if models:
            for model in models:
                if self.Repository.delete_worker_norm(model):
                    print(f'worker {model.id} of norm {model.norm_id} is deleted ')
    


############################################ machine norm 
    def create_machine_norm(self,model):
        self.Repository.insert_machine_norm(model)
        print(f'machine_norm is created')

    def update_machine_norm(self,norm_id,id,model=None):
        if not model:
            Views.machine_norm_update_view().Render(machines=self.Repository.machine,machine_norm=self.Repository.get_machine_norm(norm_id,id))
            return
        if self.Repository.update_machine_norm(norm_id,id,model):
            print(f'machine {model.id} of norm {model.norm_id} is updated')
    
    def delete_machine_norm(self,norm_id,id):
        model = Enumerable(self.Repository.get_machine_norm_by_norm_id(norm_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_machine_norm(model)
        
    def delete_by_norm_id(self,norm_id:str):
        models = self.Repository.get_machine_norm_by_norm_id(norm_id)
        if models:
            for model in models:
                if self.Repository.delete_machine_norm(model):
                    print(f'machine {model.id} of norm {model.norm_id} is deleted ')

############################################ material norm 
    def create_material_norm(self,model):
        self.Repository.insert_material_norm(model)
        print(f'material_norm is created')

    def update_material_norm(self,norm_id,id,model=None):
        if not model:
            Views.material_norm_update_view().Render(materials=self.Repository.material,material_norm=self.Repository.get_material_norm(norm_id,id))
            return
        if self.Repository.update_material_norm(norm_id,id,model):
            print(f'material {model.id} of norm {model.norm_id} is updated')
    
    def delete_material_norm(self,norm_id,id):
        model = Enumerable(self.Repository.get_material_norm_by_norm_id(norm_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_material_norm(model)
        
    def delete_by_norm_id(self,norm_id:str):
        models = self.Repository.get_material_norm_by_norm_id(norm_id)
        if models:
            for model in models:
                if self.Repository.delete_material_norm(model):
                    print(f'material {model.id} of norm {model.norm_id} is deleted ')
        
############################################ worker 
    def delete_worker(self,id:str):
        if self.Repository.delete_worker(id):
            print(f'worker {id} is deleted ')
    
    def create_worker(self,model=None):
        if not model:
            self.Render(Views.work_create_view())
            return
        self.Repository.insert_worker(model)
        print(f'worker {model.id} is created')
        
    def list_worker(self,key=None):
        if self.Repository.worker:
            if not key:
                data = [item.to_list() for item in self.Repository.worker]
                self.Update(key='-TABLE WORKER-',values=data)
                return
            data = [item.to_list() for item in self.Repository.get_worker_by_key(key)]  
            self.Update(key='-TABLE WORKER-',values=data)
            self.count_worker(len(data))
            
    def count_worker(self,count=None):
        num = count if count else self.Repository.worker_count
        self.Update(key='-WORKER COUNT TEXT-',values=num)
############################################ machine
    def delete_machine(self,id:str):
        if self.Repository.delete_machine(id):
            print(f'machine {id} is deleted ')
    
    def create_machine(self,model=None):
        if not model:
            self.Render(Views.machineCreateView())
            return
        self.Repository.insert_machine(model)
        print(f'machine {model.id} is created')
        
    def list_machine(self,key=None):
        if self.Repository.machine:
            if not key:
                data = [item.to_list() for item in self.Repository.machine]
                self.Update(key='-TABLE MACHINE-',values=data)
                return
            data = [item.to_list() for item in self.Repository.get_machine_by_key(key=key)]  
            self.Update(key='-TABLE MACHINE-',values=data)
            self.count_machine(len(data))
            
    def count_machine(self,count=None):
        num = count if count else self.Repository.machine_count
        self.Update(key='-MACHINE COUNT TEXT-',values=num) 
############################################ material 
    def delete_material(self,id:str):
        if self.Repository.delete_material(id):
            print(f'material {id} is deleted ')
    
    def create_material(self,model=None):
        if not model:
            self.Render(Views.material_create_view())
            return
        self.Repository.insert_material(model)
        print(f'material {model.id} is created')
        
    def list_material(self,key=None):
        if self.Repository.material:
            if not key:
                data = [item.to_list() for item in self.Repository.material]
                self.Update(key='-TABLE MATERIAL-',values=data)
                return
            data = [item.to_list() for item in self.Repository.get_material_by_key(key=key)]  
            self.Update(key='-TABLE MATERIAL-',values=data)
            self.count_material(len(data))
            
    def count_material(self,count=None):
        num = count if count else self.Repository.material_count
        self.Update(key='-MATERIAL COUNT TEXT-',values=num)       
############################################ hang muc 
    def create_hang_muc(self,model=None):
        if not model:
            self.Render(Views.hang_muc_create_view)
            return
        self.Repository.insert_hang_muc(model)
        print(f'hang muc {model.id} is created')
                
    def delete_hang_muc(self,id:str):
        if self.Repository.delete_hang_muc(id):
            print(f'Hang muc {id} is deleted ')
