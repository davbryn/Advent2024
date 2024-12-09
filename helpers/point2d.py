class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, val):
        if isinstance(val, (int)):
            return Point2D(self.x * val, self.y * val)
        return NotImplemented

    
    
    def rotate_90(self):
        x = self.x
        self.x = -self.y
        self.y = x
        
    @staticmethod
    def distance(pointA, pointB):
        return Point2D(pointA.x - pointB.x, pointA.y - pointB.y)
         
    def __repr__(self):
        return f"Point2D(x={self.x}, y={self.y})"