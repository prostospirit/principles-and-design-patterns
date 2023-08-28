# Liskov's notion of a behavioural subtype defines a notion of substitutability for objects;
# that is, if S is a subtype of T, then objects of type T in a program may be replaced
# with objects of type S without altering any of the desirable properties of that program (e.g. correctness).

class Rectangle:
    def __init__(self, width, height):
        self._height = height
        self._width = width

    @property
    def area(self):
        return self._width * self._height

    def __str__(self):
        return f'Width: {self.width}, height: {self.height}'

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value


class Square(Rectangle):
    """Implied that square is a private case of rectangle"""
    def __init__(self, size):
        Rectangle.__init__(self, size, size)

    @Rectangle.width.setter  # These setters affects base Rectangle setters behavior
    def width(self, value):
        self._width = self._height = value

    @Rectangle.height.setter
    def height(self, value):
        self._width = self._height = value


def calculate_something(figure: Rectangle):
    """
    This func shows how it breaks the LSP principle, because if we have an interface that takes a base class,
    we should also be able to pass in child classes with the same correct effect.
    """
    width = figure.width
    figure.height = 10  # unpleasant side effect
    expected = int(width * 10)
    print(f'Expected an area of {expected}, got {figure.area}')


# usage example
if __name__ == '__main__':
    rectangle = Rectangle(2, 3)
    calculate_something(rectangle)

    square = Square(5)
    calculate_something(square)
