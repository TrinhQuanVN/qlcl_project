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
# ############################################ worker work time
#     def delete_worker_work_time_by_work_id(self,work_id):
#         wwts = self.Repository.get_worker_work_time_by_work_id(work_id)
#         if not wwts:
#             return
#         for wwt in wwts:
#             self.Repository.delete_worker_work_time(wwt)
            
#     def create_worker_work_time_by_work_time(self,model:Models.work_time):
#         work_id = model.work_id
#         # delete worker work time cu
#         self.Repository.delete_worker_work_time_by_work_id(work_id)
#         # get worker works                
#         worker_works = self.Repository.get_worker_work_by_work_id(work_id)
#         if worker_works:
#             for ww in worker_works:
#                 amount = ww.amount / model.days if model.days > 0 else 0
#                 for i in range(model.days):
#                     self.Repository.insert_worker_work_time(Models.worker_work_time(work_id,ww.id,amount,model.start + timedelta(days=i)))  
        

#     def create_worker_work_time(self,model:Models.worker_work_time):
#         self.Repository.insert_worker_work_time(model)

# ############################################ work time
#     def delete_work_time(self,work_id):
#         model = self.Repository.get_work_time_by_work_id(work_id)
#         if not model:
#             return
#         if self.Repository.delete_work_time(model):
#             print(f'work time {work_id} is deleted')

#     def edit_wrok_time(self,work_id,model:Models.work_time=None):
#         if not model:
#             work_time = self.Repository.get_work_time_by_work_id(work_id)
#             self.Render(Views.work_time_update_view,work_time=work_time)
#             return
#         if self.Repository.update_work_time(work_id,model):
#             print(f'work time {work_id} is updated')
    
#     def draw_work_time(self,start=None,end=None):
#         if not start and not end:
#             self._draw_work_time_all()
#             return
#         self._draw_work_time(start,end)

#     def _draw_work_time_all(self):
#         wts = self.Repository.get_work_time_not_null()
#         if wts:
#             start = min([item.start for item in wts])
#             end = max([item.end for item in wts])
#             if start and end:
#                 self._draw_work_time(start,end)

#     def _draw_work_time(self,start:datetime,end:datetime):
#         class coordinate:
#             def __init__(self,x,y) -> None:
#                 self.x = x
#                 self.y = y
#             def add_x(self,x):
#                 self.x += x

#             def __sub__(self,other):
#                 return self.__class__(*[self.x-other.x,self.y-other.y])
                
#             def add_y(self,y):
#                 self.y += y
#             @property
#             def coordinate(self):
#                 return (self.x,self.y)
            
#             def __add__(self, other):
#                 return self.__class__(*[self.x+other.x,self.y+other.y])
            
#             def __repr__(self) -> str:
#                 return 'coordinate ({},{})'.format(self.x,self.y)
            
#         def draw_line(graph,point_from:coordinate,point_to:coordinate,color='white',width=1):
#             graph.draw_line(point_from=point_from.coordinate,point_to=point_to.coordinate,color=color,width=width)

#         def draw_rectangle(graph,top_left:coordinate,bottom_right:coordinate,line_color='blue',line_width=1,fill_color=None):
#             graph.draw_rectangle(top_left=top_left.coordinate,bottom_right=bottom_right.coordinate,line_color=line_color,line_width=1,fill_color=fill_color)
            
#         def draw_text(graph,text,location:coordinate,color='white',font=('Any',9),angle=0,text_location=sg.TEXT_LOCATION_RIGHT):
#             graph.draw_text(text=text,location=location.coordinate,color=color,font=font,angle=angle,text_location=text_location)
                        
#         wts = self.Repository.get_work_time_by_start_end(start,end) # công việc trong khoảng start end
#         work_count = len(wts)

#         day_count = (end - start).days + 1 # số ngày
        
#         dates = [start + timedelta(days=i) for i in range(day_count)] # danh sách ngày làm việc trong khoảng start end
#         X,Y = GRAPH_SIZE # chieu cao, chieu rong cua canavas
        
#         DISTANCE_KHUNG_DEN_TRUC = 10
#         DISTANCE_VIEN_KHUNG = 5
#         DISTANCE_GIUA_2_KHUNG = 10
                
#         HEIGHT_KHUNG_1 = 120
#         HEIGHT_KHUNG_2 = Y - HEIGHT_KHUNG_1 - DISTANCE_KHUNG_DEN_TRUC * 2 - DISTANCE_GIUA_2_KHUNG
#         WIDTH_KHUNG = X - DISTANCE_VIEN_KHUNG * 2

#         min_y_between = 10 # khoảng cách nhỏ nhất giữa 2 công việc trục y đồ thị 2 
#         min_x_between = 15 # khoảng cách nhỏ nhất giữa 2 ngày trục x đồ thị 2 

#         WIDTH_CHU_VIET = 10
#         HEIGHT_CHU_VIET = 20

#         MIN_NHAN_CONG_BIEU_DIEN = 10 # gia tri be nhat tren truc y cua do thi 1

#         max_x = WIDTH_KHUNG - DISTANCE_KHUNG_DEN_TRUC - WIDTH_CHU_VIET
#         max_y_1 = HEIGHT_KHUNG_1 - DISTANCE_KHUNG_DEN_TRUC - HEIGHT_CHU_VIET
#         max_y_2 = HEIGHT_KHUNG_2 - DISTANCE_KHUNG_DEN_TRUC - HEIGHT_CHU_VIET

#         goc_toa_do_1 = coordinate(DISTANCE_VIEN_KHUNG+WIDTH_CHU_VIET,DISTANCE_VIEN_KHUNG+HEIGHT_CHU_VIET)
#         goc_toa_do_2 = coordinate(DISTANCE_VIEN_KHUNG+WIDTH_CHU_VIET,DISTANCE_VIEN_KHUNG + HEIGHT_KHUNG_1+DISTANCE_GIUA_2_KHUNG+HEIGHT_CHU_VIET)
#         graph = self.window['-GRAPH-']
#         # xóa
#         graph.erase()
#         # vẽ khung đồ thị 1
#         top_left=coordinate(DISTANCE_VIEN_KHUNG,HEIGHT_KHUNG_1+DISTANCE_VIEN_KHUNG)
#         bottom_right=coordinate(WIDTH_KHUNG+DISTANCE_VIEN_KHUNG,DISTANCE_VIEN_KHUNG)
#         draw_rectangle(graph,top_left,bottom_right)
#         # vẽ khung đồ thị 2
#         top_left=coordinate(DISTANCE_VIEN_KHUNG,Y-DISTANCE_VIEN_KHUNG)
#         bottom_right=coordinate(WIDTH_KHUNG+DISTANCE_VIEN_KHUNG,Y-DISTANCE_VIEN_KHUNG-HEIGHT_KHUNG_2)
#         draw_rectangle(graph,top_left,bottom_right)
        
#         # vẽ trục tọa độ đồ thị 1
#         draw_line(graph,goc_toa_do_1,goc_toa_do_1 + coordinate(max_x,0))
#         draw_line(graph,goc_toa_do_1,goc_toa_do_1 + coordinate(0,max_y_1))
        
#         # vẽ trục tọa độ đồ thị 2
#         draw_line(graph,goc_toa_do_2,goc_toa_do_2 + coordinate(max_x,0))
#         draw_line(graph,goc_toa_do_2,goc_toa_do_2 + coordinate(0,max_y_2))
        
#         # vẽ đồ thị thứ 2
#         x_between = min([min_x_between, max_x/day_count]) if dates else min_x_between # khoảng cách giữa các ngày
#         y_between = min([min_y_between, max_y_2/work_count]) if wts else min_y_between # khoảng cách giữa các id công việc

#         coordinate_x_2 = [(goc_toa_do_2 + coordinate(x_between*(i+1),0)) for i in range(day_count)] # danh sách tọa độ trục x do thi 2 -> ngày bắt đầu từ start kết thúc end
#         coordinate_y_2 = [(goc_toa_do_2 +coordinate(0,y_between*(i+1))) for i in range(work_count)] # danh sách tọa độ trục y do thi 2-> công việc thực hiện trong khoảng start và end       
        
#         coordinate_x_1 = [(goc_toa_do_1 + coordinate(x_between*(i+1),0)) for i in range(day_count)] # danh sách tọa độ trục x do thi 1 -> ngày bắt đầu từ start kết thúc end
        
#         if wts:
#             dict_coordinate_work = dict(zip(wts,coordinate_y_2))
#             for key, value in dict_coordinate_work.items():
#                 text = key.work_id
#                 location= value
#                 draw_text(graph,text,location)
#             for item in wts:
#                 # draw line so ngay lam viec
#                 point_from = dict_coordinate_work[item] + coordinate(((item.start-start).days)*x_between,0)
#                 point_to = dict_coordinate_work[item] + coordinate(((item.end-start).days+1)*x_between,0)
#                 print(point_from,point_to)
#                 draw_line(graph,point_from=point_from,point_to=point_to,color='green',width=2)
#                 # hien thi nhan cong tren dong
#                 text = self.Repository.get_worker_work_by_work_id(item.work_id)
#                 if not text or item.days == 0:
#                     text = 0
#                 else:
#                     text = round(text[0].amount / item.days,1)
#                 location = point_from + coordinate((point_to-point_from).x/2,0)
#                 draw_text(graph,text=text,location=location,color='yellow',text_location=sg.TEXT_LOCATION_BOTTOM)
        
#         if dates:
#             dict_coordinate_date_2 = dict(zip(coordinate_x_2,dates))
#             dict_coordinate_date_1 = dict(zip(coordinate_x_1,dates))
            
#             for key, value in dict_coordinate_date_2.items():
#                 text = value.strftime(r'%d-%m')
#                 location= key
#                 draw_text(graph,text,location,angle=90)

#             for key, value in dict_coordinate_date_1.items():
#                 text = value.strftime(r'%d-%m')
#                 location= key
#                 draw_text(graph,text,location,angle=90)
                                
#         # vẽ đồ thị thứ 1
#         def draw_reg_worker(coordinate_date:coordinate,height):
#             pass

#         worker_per_day = []
#         for date in dates:
#             worker_work_times = self.Repository.get_worker_work_time_by_date(date)
#             if not worker_work_times:
#                 worker_per_day.append(0)
#                 continue
#             worker_per_day.append(sum([item.amount for item in worker_work_times]))
#         print(worker_per_day)
#         max_worker = max(worker_per_day)
#         scale = max_worker // max_y_1 if max_worker // max_y_1 >=1 else 1

#         a = [x for x in range(1,max_y_1 // MIN_NHAN_CONG_BIEU_DIEN)] # danh sách các điểm trục y của đồ thị 1
#         coordinate_y_1 = [(goc_toa_do_1 +coordinate(0,i*MIN_NHAN_CONG_BIEU_DIEN)) for i in a] # danh sách tọa độ trục y do thi 1-> bieu dien khoang nhan cong      
#         nc_bieu_dien = [MIN_NHAN_CONG_BIEU_DIEN*scale*i for i in range(len(a))] # nhan cong bieu dien
#         dict_nhan_cong_bieu_dien = dict(zip(nc_bieu_dien,coordinate_y_1))
#         if worker_per_day:
#             for key, value in dict_nhan_cong_bieu_dien.items():
#                 text = key
#                 location= value
#                 draw_text(graph,text,location)            
                
#     def create_work_time(self,model:Models.work_time):
#         self.Repository.insert_work_time(model)
        
#     def list_work_time(self,start:datetime=None,end:datetime=None):
#         if not start and not end:
#             self._list_work_time(self.Repository.work_time)
#             return
#         self._list_work_time(self.Repository.get_work_time_by_start_end(start,end))

# #     def _list_work_time(self,work_time):
#         dtree = sg.TreeData()
#         for item in work_time:
#             start = ex.display_date_time(item.start) if item.start else ''
#             end = ex.display_date_time(item.end) if item.end else ''
#             dtree.insert('',item.work_id,item.work_id,[start,end])
#         self.window['-TREE TIME-'].update(dtree)

############################################ norm
    def _norm_create_copy(self,norm_id):
        model = self.Repository.get_item('norm', id= norm_id)
        if not model:
            return
        model = model[0]
        copy_model = Models.norm(f'copy_{norm_id}', model.name, model.unit)
        self.create_norm(copy_model)
            
        worker_norm = self.Repository.get_item('worker_norm',norm_id=id)
        if worker_norm:
            for item in worker_norm:
                self.create_worker_norm(Models.worker_norm(copy_model.id,item.id,item.amount))
                
        machine_norm = self.Repository.get_item('machine_norm',norm_id=id)
        if machine_norm:
            for item in machine_norm:
                self.create_machine_norm(Models.machine_norm(copy_model.id,item.id,item.amount)) 
                
        material_norm = self.Repository.get_item('material_norm',norm_id=id)
        if material_norm:
            for item in material_norm:
                self.create_material_norm(Models.material_norm(copy_model.id,item.id,item.amount))
       
    def create_copy_norm(self,values):
        norm_ids = self._analyze_tree_select('norm', values)
        if not norm_ids:
            return
        for id in norm_ids:
                self._norm_create_copy(id)
        self.list_norm()

    def _norm_delete(self,norm_id):
        model = self.Repository.get_item('norm',id= norm_id)
        normer_norm = self.Repository.get_item('normer_norm', norm_id = norm_id)
        machine_norm = self.Repository.get_item('machine_norm', norm_id = norm_id)
        material_norm = self.Repository.get_item('material_norm', norm_id = norm_id)        
        if not model:
            return
        model = model[0]
        if normer_norm:
            for x in normer_norm:
                self.Repository.delete_item('normer_norm',model)
        if machine_norm:
            for x in machine_norm:
                self.Repository.insert_item('machine_norm', model) 
        if material_norm:
            for x in material_norm:
                self.Repository.insert_item('material_norm', model)         
        if self.Repository.delete_item('norm',model):
            print(f'norm {model.id} is deleted')
                                   
    def delete_norm(self,values):
        norm_ids = self._analyze_tree_select('norm', values)
        if not norm_ids:
            return
        for id in norm_ids:
            self._norm_delete(id)

    def edit_norm(self,values,model=None):
        norm_ids = self._analyze_tree_select('norm', values)
        if not norm_ids:
            return
        if len(norm_ids) >1:
            sg.popup_ok('Please selecte one norm at time to edit!!')
            return
        if not self.Repository.get_item('norm',id= norm_ids[0]):
            print(f'norm {norm_ids[0]} is not existed')
            return
        if not model:
            self.Render(Views.norm_edit_view,
                        norm=self.Repository.get_item('norm', id= norm_ids[0])[0],
                        worker_norm= self.Repository.get_item('worker_norm',norm_id= norm_ids[0]),
                        machine_norm= self.Repository.get_item('machine_norm',norm_id= norm_ids[0]),
                        material_norm= self.Repository.get_item('material_norm',norm_id= norm_ids[0]),
                        worker= self.Repository.get_worker_by_norm_id(norm_ids[0]),
                        machine= self.Repository.get_machine_by_norm_id(norm_ids[0]),
                        material= self.Repository.get_material_by_norm_id(norm_ids[0]),
                        workers=self.Repository.get_item('worker'),
                        materials=self.Repository.get_item('material'),
                        machines=self.Repository.get_item('machine'))
            return
        if self.Repository.update_norm(norm_ids[0], model):
            print(f'norm {norm_ids[0]} is updated')
    
    def create_norm(self,values=None,model=None):
        if not model:
            self.Render(Views.norm_create_view,
                        worker=self.Repository.get_item('worker'),
                        machine=self.Repository.get_item('machine'),
                        material=self.Repository.get_item('material'))
            return
        self.Repository.insert_item('norm',model)
        print(f'norm {model.id} is created')
     
    def count_norm(self,count=None):
        num = count if count else self.Repository.count_item('norm')
        self.Update(key= KeyGUI.norm_count_text.value, values=num)
        
    def list_norm(self,values=None):
        if not values:
            if not self.Repository.get_item('norm'):
                return
            self._list_norm(self.Repository.get_item('norm'))
            return
                      
        key = values[KeyGUI.norm_search_input.value]
        print('key is {}'.format(key))
        if key:
            self._list_norm(self.Repository.get_item('norm', match_mode=1, logic='or', to_lower=True, id=key, name=key[0]))
            print(f'norm list with key {key} is showed !')
            
    def _list_norm(self,norms:list):
        treedata = sg.TreeData()
        if not norms:
            self.Update(key= KeyGUI.norm_tree.value,values=treedata)
            self.count_norm(0)
        for item in norms:
            treedata.Insert('',item.id,item.name,[item.id,item.unit])
            
        self.Update(key= KeyGUI.norm_tree.value,values=treedata)
        self.count_norm(len(norms))
                 
    def create_from_excel(self,values=None,path=None):
        if not path:
            self.Render(Views.create_norm_from_excel_view)
            return
        count = self._read_excel_get_norm(path)
        print(f'{count} norms have been created successfully')
            
    def _read_excel_get_norm(self,path):
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

############################################ work
    def _analyze_tree_select(self,tree:str, values):
        if tree == 'norm':
            ids = values[KeyGUI.norm_tree.value]
            if not ids:
                return
            return [x for x in ids if ex.is_norm(x)]
        elif tree == 'work':
            ids = values[KeyGUI.work_tree.value]
            if not ids:
                return
            return [x for x in ids if ex.is_work(x)]
                    
    def _work_create_copy(self,id):
        model = self.Repository.get_item('work',id = id)
        if not model:
            return
        model = model[0]
        copy_id = 'W{}'.format(next(Models.work.id_iter))
        copy_model = Models.work(model.name,model.unit,model.amount,model.hm_id,copy_id)
        self.create_work(model=copy_model)
        
        worker_work = self.Repository.get_item('worker_work',work_id=id)
        if worker_work:
            for item in worker_work:
                self.create_worker_work(Models.worker_work(copy_model.id,item.id,item.amount))
                
        machine_work = self.Repository.get_item('machine_work',work_id=id)
        if machine_work:
            for item in machine_work:
                self.create_machine_work(Models.machine_work(copy_model.id,item.id,item.amount)) 
                
        material_work = self.Repository.get_item('material_work',work_id=id)
        if material_work:
            for item in material_work:
                self.create_material_work(Models.material_work(copy_model.id,item.id,item.amount))
       
    def _create_work_by_norm(self,norm_id):
        norm = self.Repository.get_item('norm', id= norm_id)[0]
        worker_norm = self.Repository.get_item('worker_norm', norm_id = norm_id)
        machine_norm = self.Repository.get_item('machine_norm', norm_id = norm_id)
        material_norm = self.Repository.get_item('material_norm', norm_id = norm_id)
        work = Models.work(norm.name, 
                            norm.unit,
                            amount = 1,
                            hm_id= self.Repository.get_item('hang_muc')[-1],
                            pv_id= self.Repository.get_item('phan_viec')[-1],)
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
                      
    def create_work(self,values=None,model=None):
        if not model:
            hang_muc = self.Repository.get_item('hang_muc')
            if not self.Repository.get_item('phan_viec'):
                self.create_phan_viec(Models.phan_viec('phần việc khác',0))            
            if not values:
                self.Render(Views.work_create_view,
                            hang_muc = hang_muc,
                            phan_viec = self.Repository.get_item('phan_viec'),
                            worker = self.Repository.get_item('worker'),
                            material = self.Repository.get_item('material'),
                            machine = self.Repository.get_item('machine'))
                return
            norm_ids = [x for x in values[KeyGUI.norm_tree.value] if ex.is_norm(x)]
            for id in norm_ids:
                self._create_work_by_norm(id)
            return
        self.Repository.insert_item('work',model)
        print(f'work {model.id} is created')
        
        self.list_work()

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
        if self.Repository.delete_item('work',model):
            print(f'work {model.id} is deleted')

    def delete_work(self,values):
        work_ids = values[KeyGUI.work_tree.value]
        if not work_ids:
            return
        for id in work_ids:
            self._work_delete(id)

    def create_copy_work(self,values):
        work_ids = self._analyze_tree_select('work', values)
        if not work_ids:
            return
        for id in work_ids:
                self._work_create_copy(id)
        self.list_work()

    # def edit_work(self,values=None,model=None):
    #     work_ids = self._analyze_tree_select('work', values)
    #     if not work_ids:
    #         return
    #     if len(work_ids) >1:
    #         sg.popup_ok('Please selecte one work at time to edit!!')
    #         return
    #     if not self.Repository.get_item('work',id= work_ids[0]):
    #         print(f'work {work_ids[0]} is not existed')
    #         return
    #     if not model:
    #         hang_mucs = self.Repository.get_item('hang_muc')
    #         phan_viecs = self.Repository.get_item('phan_viecs')
            
    #         work = self.Repository.get_item('work', id =work_ids[0])
    #         hang_muc = self.Repository.get_item('hang_muc',id = work.hm_id)
    #         phan_viec = self.Repository.get_item('phan_viec',id = work.pv_id)
            
            
    #         worker_work = self.Repository.get_item('worker_work',work_id = work.id)
    #         machine_work = self.Repository.get_item('machine_work',work_id = work.id)
    #         material_work = self.Repository.get_item('material_work',work_id = work.id)
            
    #         worker = self.Repository.get_worker_by_work_id(id)
    #         machine = self.Repository.get_machine_by_work_id(id)
    #         material = self.Repository.get_material_by_work_id(id)
    #         self.Render(Views.work_edit_view,
    #                     hang_mucs=hang_mucs,
    #                     hang_muc=hang_muc,
    #                     work=work,
    #                     worker_work=worker_work,
    #                     machine_work=machine_work,
    #                     material_work=material_work,
    #                     worker=worker,
    #                     machine=machine,
    #                     material=material,
    #                     workers=self.Repository.worker,
    #                     materials=self.Repository.material,
    #                     machines=self.Repository.machine)
    #         return
    #     if self.Repository.update_work(id,model):
    #         print(f'work {id} is updated')
    #     else:
    #         print(f'work {id} is not updated')
    
    def count_work(self,count=None):
        num = count if count else self.Repository.count_item('work')
        self.Update(key= KeyGUI.work_count_text.value,values=num)
        
    def list_work(self,values=None):
        if not values:
            if not self.Repository.get_item('work'):
                return
            self._list_work(self.Repository.get_item('work'))
            return
                      
        key = values[KeyGUI.work_search_input.value]
        if key:
            self._list_work(self.Repository.get_item('work', match_mode=1, logic='or', to_lower=True, id=key, name=key[0]))
            print(f'work list with key {key} is showed !')
            
    def _list_work(self,works:list):
        treedata = sg.TreeData()
        for item in works:
            treedata.Insert('',item.id,item.name,[item.id,item.unit,item.amount,item.work_day,item.start,item.end])
            
        self.Update(key=KeyGUI.work_tree.value,values=treedata)
        self.count_work(len(works))

 
############################################ worker work
    def create_worker_work(self,model):
        self.Repository.insert_item('worker_work',model)
        print(f'workerwork is created') 

    def update_worker_work(self,work_id,id,model=None):
        if not model:
            Views.work().Render(workers=self.Repository.get_item('worker'),
                                worker_work=self.Repository.get_item('worker_work',work_id=work_id,id=id)[0])
            return
        if self.Repository.update_worker_work(work_id,id,model):
            print(f'worker {model.id} of work {model.work_id} is updated')
    
    def delete_worker_work(self,work_id,id):
        model = Enumerable(self.Repository.get_item('worker_work',work_id=work_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_item('worker_work',model)
        
    def delete_worker_work_by_work_id(self,work_id:str):
        models = self.Repository.get_item('worker_work',work_id=work_id)
        if models:
            for model in models:
                if self.Repository.delete_item('worker_work',model):
                    print(f'worker {model.id} of work {model.work_id} is deleted ')
    
    def create_worker_work(self,model):
        self.Repository.insert_item('worker_work',model)
        print(f'workerwork is created')
############################################ machine work
    def create_machine_work(self,model):
        self.Repository.insert_item('machine_work',model)
        print(f'machinework is created') 

    def update_machine_work(self,work_id,id,model=None):
        if not model:
            Views.work().Render(machines=self.Repository.get_item('machine'),
                                machine_work=self.Repository.get_item('machine_work',work_id=work_id,id=id)[0])
            return
        if self.Repository.update_machine_work(work_id,id,model):
            print(f'machine {model.id} of work {model.work_id} is updated')
    
    def delete_machine_work(self,work_id,id):
        model = Enumerable(self.Repository.get_item('machine_work',work_id=work_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_item('machine_work',model)
        
    def delete_machine_work_by_work_id(self,work_id:str):
        models = self.Repository.get_item('machine_work',work_id=work_id)
        if models:
            for model in models:
                if self.Repository.delete_item('machine_work',model):
                    print(f'machine {model.id} of work {model.work_id} is deleted ')
    
    def create_machine_work(self,model):
        self.Repository.insert_item('machine_work',model)
        print(f'machinework is created')
############################################ material work
    def create_material_work(self,model):
        self.Repository.insert_item('material_work',model)
        print(f'materialwork is created') 

    def update_material_work(self,work_id,id,model=None):
        if not model:
            Views.work().Render(materials=self.Repository.get_item('material'),
                                material_work=self.Repository.get_item('material_work',work_id=work_id,id=id)[0])
            return
        if self.Repository.update_material_work(work_id,id,model):
            print(f'material {model.id} of work {model.work_id} is updated')
    
    def delete_material_work(self,work_id,id):
        model = Enumerable(self.Repository.get_item('material_work',work_id=work_id)).where(lambda x: x.id.lower() == id.lower())[0]
        self.Repository.delete_item('material_work',model)
        
    def delete_material_work_by_work_id(self,work_id:str):
        models = self.Repository.get_item('material_work',work_id=work_id)
        if models:
            for model in models:
                if self.Repository.delete_item('material_work',model):
                    print(f'material {model.id} of work {model.work_id} is deleted ')
    
    def create_material_work(self,model):
        self.Repository.insert_item('material_work',model)
        print(f'materialwork is created')
        
 
############################################ worker norm
    def create_worker_norm(self,model):
        self.Repository.insert_item('worker_norm',model)
        print(f'worker_norm is created')

    def update_worker_norm(self,norm_id,id,model=None):
        if not model:
            Views.worker_norm_update_view().Render(workers=self.Repository.get_item('worker'), 
                                                     worker_norm=self.Repository.get_item('worker_norm',norm_id=norm_id,id=id))
            return
        # if self.Repository.update_worker_norm(norm_id,id,model):
        if self.Repository.update('worker_norm', model, norm_id=norm_id, id=id):
            print(f'worker {model.id} of norm {model.norm_id} is updated')
    
    def delete_worker_norm(self,norm_id,id):
        model = self.Repository.get_item('worker_norm',norm_id=norm_id,id=id)
        if not model:
            return
        # model = Enumerable(self.Repository.get_worker_norm_by_norm_id(norm_id)).where(lambda x: x.id.lower() == id.lower())[0]
        # self.Repository.delete_worker_norm(model)
        self.Repository.delete_item('worker_norm',model[0])
        
    def delete_by_norm_id(self,norm_id:str):
        models = self.Repository.get_item('worker_norm',norm_id=norm_id)
        if models:
            for model in models:
                if self.Repository.delete_item('worker_norm',model):
                    print(f'worker {model.id} of norm {model.norm_id} is deleted ')


############################################ machine norm 
    def create_machine_norm(self,model):
        self.Repository.insert_item('machine_norm',model)
        print(f'machine_norm is created')

    def update_machine_norm(self,norm_id,id,model=None):
        if not model:
            Views.machine_norm_update_view().Render(machines=self.Repository.get_item('machine'), 
                                                     machine_norm=self.Repository.get_item('machine_norm',norm_id=norm_id,id=id))
            return
        # if self.Repository.update_machine_norm(norm_id,id,model):
        if self.Repository.update('machine_norm', model, norm_id=norm_id, id=id):
            print(f'machine {model.id} of norm {model.norm_id} is updated')
    
    def delete_machine_norm(self,norm_id,id):
        model = self.Repository.get_item('machine_norm',norm_id=norm_id,id=id)
        if not model:
            return
        # model = Enumerable(self.Repository.get_machine_norm_by_norm_id(norm_id)).where(lambda x: x.id.lower() == id.lower())[0]
        # self.Repository.delete_machine_norm(model)
        self.Repository.delete_item('machine_norm',model[0])
        
    def delete_by_norm_id(self,norm_id:str):
        models = self.Repository.get_item('machine_norm',norm_id=norm_id)
        if models:
            for model in models:
                if self.Repository.delete_item('machine_norm',model):
                    print(f'machine {model.id} of norm {model.norm_id} is deleted ')
        
############################################ material norm 
    def create_material_norm(self,model):
        self.Repository.insert_item('material_norm',model)
        print(f'material_norm is created')

    def update_material_norm(self,norm_id,id,model=None):
        if not model:
            Views.material_norm_update_view().Render(materials=self.Repository.get_item('material'), 
                                                     material_norm=self.Repository.get_item('material_norm',norm_id=norm_id,id=id))
            return
        # if self.Repository.update_material_norm(norm_id,id,model):
        if self.Repository.update('material_norm', model, norm_id=norm_id, id=id):
            print(f'material {model.id} of norm {model.norm_id} is updated')
    
    def delete_material_norm(self,norm_id,id):
        model = self.Repository.get_item('material_norm',norm_id=norm_id,id=id)
        if not model:
            return
        # model = Enumerable(self.Repository.get_material_norm_by_norm_id(norm_id)).where(lambda x: x.id.lower() == id.lower())[0]
        # self.Repository.delete_material_norm(model)
        self.Repository.delete_item('material_norm',model[0])
        
    def delete_by_norm_id(self,norm_id:str):
        models = self.Repository.get_item('material_norm',norm_id=norm_id)
        if models:
            for model in models:
                if self.Repository.delete_item('material_norm',model):
                    print(f'material {model.id} of norm {model.norm_id} is deleted ')
        
############################################ worker 
    def delete_worker(self,id:str):
        model = self.Repository.get_item('worker', id=id)
        if not model:
            return
        self.Repository.delete_item(id)
        print(f'worker {id} is deleted ')
    
    def create_worker(self,model=None):
        if not model:
            self.Render(Views.work_create_view())
            return
        self.Repository.insert_item('worker',model)
        print(f'worker {model.id} is created')
        
    # def list_worker(self,key=None):
    #     if self.Repository.worker:
    #         if not key:
    #             data = [item.to_list() for item in self.Repository.worker]
    #             self.Update(key='-TABLE WORKER-',values=data)
    #             return
    #         data = [item.to_list() for item in self.Repository.get_worker_by_key(key)]  
    #         self.Update(key='-TABLE WORKER-',values=data)
    #         self.count_worker(len(data))
            
    # def count_worker(self,count=None):
    #     num = count if count else self.Repository.count_item('worker')
    #     self.Update(key= KeyGUI.worker_count_text,values=num)
############################################ machine
    def delete_machine(self,id:str):
        model = self.Repository.get_item('machine', id=id)
        if not model:
            return
        self.Repository.delete_item(id)
        print(f'machine {id} is deleted ')
    
    def create_machine(self,model=None):
        if not model:
            self.Render(Views.machineCreateView())
            return
        self.Repository.insert_item('machine',model)
        print(f'machine {model.id} is created')
        
    # def list_machine(self,key=None):
    #     if self.Repository.machine:
    #         if not key:
    #             data = [item.to_list() for item in self.Repository.machine]
    #             self.Update(key='-TABLE MACHINE-',values=data)
    #             return
    #         data = [item.to_list() for item in self.Repository.get_machine_by_key(key=key)]  
    #         self.Update(key='-TABLE MACHINE-',values=data)
    #         self.count_machine(len(data))
            
    # def count_machine(self,count=None):
    #     num = count if count else self.Repository.count_item('machine')
    #     self.Update(key='-MACHINE COUNT TEXT-',values=num) 
############################################ material 
    def delete_material(self,id:str):
        model = self.Repository.get_item('material', id=id)
        if not model:
            return
        self.Repository.delete_item(id)
        print(f'material {id} is deleted ')
    
    def create_material(self,model=None):
        if not model:
            self.Render(Views.material_create_view())
            return
        self.Repository.insert_item('material',model)
        print(f'material {model.id} is created')
        
    # def list_material(self,key=None):
    #     if self.Repository.material:
    #         if not key:
    #             data = [item.to_list() for item in self.Repository.material]
    #             self.Update(key='-TABLE MATERIAL-',values=data)
    #             return
    #         data = [item.to_list() for item in self.Repository.get_material_by_key(key=key)]  
    #         self.Update(key='-TABLE MATERIAL-',values=data)
    #         self.count_material(len(data))
            
    # def count_material(self,count=None):
    #     num = count if count else self.Repository.count_item('material')
    #     self.Update(key='-MATERIAL COUNT TEXT-',values=num)       
############################################ hang muc 
    def create_hang_muc(self,model=None):
        if not model:
            self.Render(Views.hang_muc_create_view)
            return
        self.Repository.insert_item('hang_muc',model)
        print(f'hang_muc {model.id} is created')
                
    def delete_hang_muc(self,id:str):
        model = self.Repository.get_item('hang_muc',id=id)
        if not model:
            print(f'hang_muc {id} not found ')
        self.Repository.delete_item('hang_muc',model)
        print(f'hang_muc {id} is deleted ')
            
############################################ Phan viec 
    def create_phan_viec(self,model=None):
        if not model:
            self.Render(Views.phan_viec_create_view)
            return
        self.Repository.insert_item('phan_viec',model)
        print(f'Phần việc {model.id} is created')
                
    def delete_phan_viec(self,id:str):
        model = self.Repository.get_item('phan_viec',id=id)
        if not model:
            print(f'phan_viec {id} not found ')
        self.Repository.delete_item('phan_viec',model)
        print(f'phan_viec {id} is deleted ')
            
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
            
    def count_ntcv(self,count=None):
        num = count if count else self.Repository.count_item('ntcv')
        self.Update(key= KeyGUI.ntcv_count_text.value,values=num)
        
    def list_ntcv(self,key=None):
        if not self.Repository.get_item('ntcv'):
            return
        if not key:
            self._list_ntcv(self.Repository.get_item('ntcv'))
            self.count_ntcv()
            print('ntcv list showed!')
            return
        self._list_ntcv(self.Repository.get_item(what= 'ntcv', key=key))
        print(f'ntcv list with key {key} is showed !')
            
    def _list_ntcv(self,ntcv:list):
        treedata = sg.TreeData()
        for item in ntcv:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name])
            
        self.Update(key=KeyGUI.ntcv_tree.value,values=treedata)
        self.count_ntcv(len(ntcv))
        
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
            
    def count_lmtn(self,count=None):
        num = count if count else self.Repository.count_item('lmtn')
        self.Update(key=KeyGUI.lmtn_count_text.value,values=num)
        
    def list_lmtn(self,key=None):
        if not self.Repository.count_item('lmtn'):
            return
        if not key:
            self._list_lmtn(self.Repository.get_item('lmtn'))
            self.count_lmtn()
            print('lmtn list showed!')
            return
        self._list_lmtn(self.Repository.get_item('lmtn', key=key))
        print(f'lmtn list with key {key} is showed !')
            
    def _list_lmtn(self,lmtn:list):
        treedata = sg.TreeData()
        for item in lmtn:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name,item.sltm, item.slm, item.ktm])
            
        self.Update(key= KeyGUI.lmtn_tree.value,values=treedata)
        self.count_lmtn(len(lmtn))
        
        
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
            
    def count_ntvl(self,count=None):
        num = count if count else self.Repository.count_item('ntvl')
        self.Update(key= KeyGUI.ntvl_count_text.value,values=num)
        
    def list_ntvl(self,key=None):
        if not self.Repository.get_item('ntvl'):
            return
        if not key:
            self._list_ntvl(self.Repository.get_item('ntvl'))
            self.count_ntvl()
            print('ntvl list showed!')
            return
        self._list_ntvl(self.Repository.get_item(what= 'ntvl', key=key))
        print(f'ntvl list with key {key} is showed !')
            
    def _list_ntvl(self,ntvl:list):
        treedata = sg.TreeData()
        for item in ntvl:
            treedata.Insert('',item.id,item.id,[item.dateNT,item.dateYC,item.name])
            
        self.Update(key= KeyGUI.ntvl_tree.value,values=treedata)
        self.count_ntvl(len(ntvl))
