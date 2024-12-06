class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Point2D):
            return Point2D(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def rotate_90(self):
        x = self.x
        self.x = -self.y
        self.y = x
        

    def __repr__(self):
        return f"Point2D(x={self.x}, y={self.y})"