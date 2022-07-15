class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def contains(self, other):
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2 < self.radius ** 2


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

circle = Circle(1,2,2)
point1 = Point(1, 2)
point2 = Point(1, 3)
point3 = Point(3, 2)
point4 = Point(3, 3)


assert(circle.contains(point1) == True)
assert(circle.contains(point2) == True)
assert(circle.contains(point3) == False)
assert(circle.contains(point4) == False)