class V2:
    """
    Реализованы магические методы 
    - для сложения (либо с V2, либо со скаляром)
    - для вычитания (либо V2, либо скаляр)
    - для умножения только на скаляр
    - для деления только на скаляр
    """

    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return (self.x**2+self.y**2)**(1/2)

    def __str__(self):
        return "x: {}, y: {}, norm: {}".format(self.x, self.y, round(self.norm(), 2))

    def __add__(self, other):
        if type(other) == V2 or issubclass(type(other), V2):
            return V2(self.x + other.x, self.y + other.y)
        else:
            return V2(self.x + other, self.y + other)
        
    def __sub__(self, other):
        if type(other) == V2 or issubclass(type(other), V2):
            return V2(self.x - other.x, self.y - other.y)
        else:
            return V2(self.x - other, self.y - other)
        
    def __mul__(self, other):
        return V2(self.x*other, self.y*other)
    
    def __div__(self, other):
        return V2(self.x/other, self.y/other)