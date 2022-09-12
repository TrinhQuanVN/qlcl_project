import enum

class Mapping(dict):

    def __setitem__(self, key, item):
        self.__dict__[key] = item

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        return repr(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __delitem__(self, key):
        del self.__dict__[key]

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def has_key(self, k):
        return k in self.__dict__

    def update(self, *args, **kwargs):
        return self.__dict__.update(*args, **kwargs)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def pop(self, *args):
        return self.__dict__.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__dict__, dict_)

    def __contains__(self, item):
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance

class Parameter(Mapping):
    def __init__(self,parameter:str) -> None:
        self.Analyze(parameter)
    
    def Analyze(self,parameter:str):
        if not '=' in parameter:
            raise Exception(f'Parameter {parameter} is not correct form')
        
        pairs = parameter.split('&') if '&' in parameter else None
        if not pairs:
            key,value = [item.strip() for item in parameter.split('=')]
            self.update({key:value})
        else:
            for pair in pairs:
                key,value = [item.strip() for item in pair.split('=')]
                self.update({key:value})
    
class Route(SingletonClass):
    routeTable = {}
    def __init__(self) -> None:
        super().__init__()
        
    @classmethod
    def GetRoutes(cls):
        return ', '.join(cls.routeTable.keys())
        
    @classmethod
    def Register(cls,route,action):
        if route in cls.routeTable:
            raise Exception(f'Route {route} is registered!!')
        else:
            cls.routeTable.update({route:action})
            
    @classmethod
    def Foward(cls,request:str):
        req = cls.Request(request)
        if not req.route in cls.routeTable:
            print('ROUTE NOT FOUND')
            return
        else:
            if not req.parameter:
                cls.routeTable.get(req.route)()
            else:
                cls.routeTable.get(req.route)(req.parameter)
            
    class Request:
        def __init__(self,request:str) -> None:
            self.route = ''
            self.parameter = None
            self.Analyze(request)
            
        def Analyze(self,request:str):
            if '?' not in request:
                self.route = request.strip()
                return
            
            route, parameter = [item.strip() for item in request.split('?')]
            self.route = route
            self.parameter = Parameter(parameter) if parameter else None
            
class MessageType(enum.Enum):
    Success = 1
    Information = 2
    Error = 3
    Confirmation = 4
    
class Message:
    Type = MessageType.Success
    Label = ''
    Text = 'Your action has completed successfully'
    BackRoute = ''
    
class MessageView:
    Model = Message()
    def __init__(self,model) -> None:
        self.Model = model
        
    def Render(self):
        if self.Model.Type == MessageType.Success:
            print(self.Model.Label.upper() if self.Model.Label else 'SUCCESS')
        elif self.Model.Type == MessageType.Error:
            print(self.Model.Label.upper() if self.Model.Label else 'ERROR')
        elif self.Model.Type == MessageType.Information:
            print(self.Model.Label.upper() if self.Model.Label else 'INFORMATION')
        elif self.Model.Type == MessageType.Confirmation:
            print(self.Model.Label.upper() if self.Model.Label else 'CONFIRMATION')
            
        if not self.Model.Type == MessageType.Confirmation:
            print(self.Model.Text)
        else:
            print(self.Model.Text,end=" ")
            answer = input().lower().strip()
            if answer in ['y','yes']:
                Route.Foward(self.Model.BackRoute)

class Extension:
    
    @classmethod
    def ToBool(cls,astr:str):
        return True if astr.lower().strip() in ['y','yes','true'] else False
    
    @classmethod
    def ToInt(cls,astr:str):
        return int(astr) if astr.isdigit() else None
            
      
    
