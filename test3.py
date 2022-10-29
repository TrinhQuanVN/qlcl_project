from enum import Enum
from unittest import result
from DataAccess import data_access
import Extension
import datetime
import numpy as np
from py_linq import Enumerable
import re
from itertools import count
import Extension as ex
import Models
def a():
    def display_date_time(date_time:datetime.datetime):
        format = '%d/%M/%y'
        return date_time.strftime(format)
    
    time = datetime.datetime(2022,11,20)
    times = [time + datetime.timedelta(days=i) for i in range(10)]
    # print(datetime.datetime.date(time+datetime.timedelta(days=1)))
    # print(time.strftime(r'%d-%m-%y'))
    # print(display_date_time(time))
    str = r'01/02/22'
    d = datetime.datetime.strptime(str,r'%d/%m/%y')
    np.random.seed(0)
    a = np.random.randint(1,10,10)
    b = np.random.random()
    date_pattern = r"^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}"
    a = re.search(date_pattern, '2/12/22') 
    
    a = count()
    b = next(a)
    # print(type(b))
    
    a = Models.ntcv(0,'ntcv0',datetime.datetime(2022,11,1))
    b = Models.ntcv(0,'ntcv0',datetime.datetime(2022,11,1))
    # for i in range(10):
    #     a = Models.ntcv(i,f'ntcv{i}',datetime.datetime(2022,11,1))
    #     print(a.dateNT, a.dateYC)
    # print(not 0)
    
    a = [{'a':1, 'b': 1, 'c': 1},{'a':2, 'b': 3, 'c': 4}]
    c = [{'a':1, 'b': 1, 'c': 1},{'a':9, 'b': 9, 'c': 9}]
    _a = Enumerable(a)
    _c = Enumerable(c)
    b = _a.join(_c, lambda x: x , lambda x: x, lambda x:x)

    print(b.to_list())
    
    marks1 = Enumerable([{ 'course' : 'Chemistry', 'mark': 90 }, {'course': 'Biology', 'mark': 85 }])
    marks2 = Enumerable([{ 'course': 'Chemistry', 'mark': 65}, {'course': 'Computer Science', 'mark': 96 }])
    common_courses = marks1.intersect(marks2, lambda c: c['course'])
    # print(common_courses.to_list())




def get_item(data, match_mode=0, logic:str=True, to_lower=False, **kwargs):
    """get item from repository

    Args:
        what (str): what list of data to get
        match_mode (_type_, optional): 0:exact match, 1:key in value. Defaults to 0.
        logic (str, optional): if true search with and operator. Defaults to True.
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
    
    # def inner_join(left:Enumerable,right:Enumerable, outer_key, inner_key):
    #     return left.join(right, outer_key, inner_key, lambda x: x)

    # def recursive_where(n):
    #     if n == 0:
    #         return where(data, list(kwargs.items())[n][0], list(kwargs.items())[n][1], to_lower, match_mode)
    #     else:
    #         return recursive_where(n-1)
                   
    if not kwargs:
        return data
    elif len(kwargs) == 1:
        key, value = list(kwargs.items())[0]
        return where(data, key, value, to_lower, match_mode).to_list()
    else:

            
        if logic: # operator 'and'
            result = data
            for key,value in kwargs.items():
                result = where(Enumerable(result),key,value,to_lower,match_mode)
            return result.to_list()
            # return recursive_where(len(kwargs))
        else:
            enumrables = []
            for key, value in kwargs.items():
                enumrables.append(where(Enumerable(data), key, value,to_lower, match_mode))            
            result = enumrables[0].to_list()
            for enum in enumrables[1:]:
                if enum.to_list():
                    result += enum.to_list() 
            return set(result)

def main():
    class x:
        def __init__(self,a,b,c) -> None:
            self.a = a
            self.b = b
            self.c = c
        
        def items(self) -> dict:
            return {'a': self.a, 'b': self.b, 'c':self.c}
        
        def __repr__(self) -> str:
            return f'a={self.a} & b={self.b} & c={self.c}'
            
    data = [x(1,2,3), x(1,5,6), x(9,2,3)]
    a = get_item(data,a=1,b=2, logic=False)
    
    print(a)
    

    hm = Models.phan_viec('hang muc 1',1)
    hm.update({'name':'hang muc an lon'})
    print(hm.name)
    
    a = data_access()
    a.items['worker'].append('a')
    print(a.items)
        
        
if __name__ == "__main__":
    main() 