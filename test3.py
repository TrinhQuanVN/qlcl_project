import Extension
import datetime

from py_linq import Enumerable

def main():
    def display_date_time(date_time:datetime.datetime):
        format = '%d/%M/%y'
        return date_time.strftime(format)
    
    time = datetime.datetime(2022,11,20)
    print(display_date_time(time))
if __name__ == "__main__":
    main() 