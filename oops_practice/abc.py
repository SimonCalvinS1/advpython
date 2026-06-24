from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, length, width):
        print("Rectangle class")
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

class Circle(Shape):
    def __init__(self, radius):
        print("Circle class")
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

class Triangle(Shape):
    def __init__(self, base, height):
        print("Triangle class")
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

class Square(Shape):
    def __init__(self, side):
        print("Square class")
        self.side = side

    def area(self):
        return self.side * self.side

print(Shape.mro())
print(Rectangle.mro())
print(Circle.mro())
print(Triangle.mro())
print(Square.mro())

shapes = [
    Rectangle(4, 5),
    Circle(3),
    Triangle(4, 5),
    Square(4)
]

for shape in shapes:
    print(shape.area())