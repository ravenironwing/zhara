class Test:
    def __init__(self):
        self._x = None #This is a hidden variable that stores the actual value of x
    @property
    def x(self): #This is the method that is called whenever you access x
        return self._x
    @x.setter #This is the method that is called whenever you set a value for x
    def x(self, value):
        self._x=value
        print("x=="+str(value))
        if self._x==7:
            print("Mwa-ha-ha!")

t=Test()

t.x=5
t.x=10
t.x="Hello!"
t.x=7
print(t.x + 25)

class Test:
    def __init__(self):
        self.x=None
    def get_x(self):
        return self.x
    def set_x(self, value):
        self.x=value
        print("x==" + str(value))
        if self.x == 7:
            print("Mwa-ha-ha!")
t=Test()
t.set_x(5)
t.set_x(10)
t.set_x("Hello")
t.set_x(7)
print(t.get_x()+25)