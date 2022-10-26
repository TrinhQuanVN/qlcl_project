import Extension
import datetime
import numpy as np
from py_linq import Enumerable
import re
from itertools import count
import Extension as ex

def main():
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
    
    a = ex.try_parse_string_to_float('a')
    print(a)
        
if __name__ == "__main__":
    main() 