from time import time
from rich.console import Console
console= Console()
def send_msg(msg):
    if(isinstance(msg,base_msg)):
        console.print(msg,style=msg.style)
    else:
        print(msg)
class base_msg:
    def __init__(self, data :str):
        self._data=data
    @property
    def style(self):
        return '' #no special styling
    def data(self):
        return self._data
    def __str__ (self):
        return self._data
    def __len__ (self):
        return len(self._data)
    def __eq__ (self,other):
        return str(self) == str(other)
    def __add__(self,other):
        if (isinstance(other,base_msg)):
            newdata=str(self)+str(other)
        elif(isinstance(other,str)): #checks if other is a string
            newdata=str(self)+other
        else:
            print("doesn't support this type")
        
class logmsg(base_msg):
    def __init__(self, data: str):
        super().__init__(data)
        self._timestamp=int(time())
    @property
    def style (self):
        return 'on yellow' # set background color to yellow
    def __str__ (self):
        return(f"[{self._timestamp}] {self.data()}")
    
class warnmsg(logmsg):
    @property
    def style(self):
        return 'white on red' #white text on red background
    def __str__(self):
        return (f"[WARN!][{self._timestamp}] {self.data()}")
    
if __name__ == '__main__':
    m1 = base_msg('Normal message')
    m2 = logmsg('Log')
    m3 = warnmsg('Warning')
    send_msg(m1)
    send_msg(m2)
    send_msg(m3)
