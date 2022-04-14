
import math

class Point:
    def __init__(self,x_init=0,y_init=0):
        self.x = x_init
        self.y = y_init

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def move(self, dx, dy):
        '''
        Arguments
        ---------
        dx, dy : delta change values
            The amounts you using to move the point by

        Returns
        -------
        Point
            Returns a new point that has been move by dx,dy
            Example: p = p.move (6, 7) 
        '''
        self.x = self.x + dx
        self.y = self.y + dy

    @staticmethod
    def fromlist (alist):
        '''
        Arguments
        ---------
        alist : list
            A list containing two elements

        Returns
        -------
        Point
            Returns a point version of the list
            Example: p = Point.fromlist ([2.4, 5.6]) 
        '''
        return Point (alist[0], alist[1])
    
    def tolist (self):
        '''
        Returns
        -------
        list
            Return a point as a list structure
            Example: alist = p.tolist()
        '''
        return [self.x, self.y]

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)
    
    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

#p1 = Point(10, 3)
#p2 = Point(1, 0)