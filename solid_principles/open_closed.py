# OCP = open for extension, closed for modification
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Product:
    postfix = 'product'

    def __init__(self, name, color, size):
        self.name: str = name
        self.color: int = color
        self.size: int = size

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return ' '.join([self.name, self.postfix])


class ProductFilter:
    """
    This is bad example of filtering class
    - state space explosion
    - 3 criteria
    - c s w cs sw cw csw = 7 methods for comparing various filters (color, size, weight)
    """

    @staticmethod
    def filter_by_color(products, color):
        for product in products:
            if product.color == color:
                yield product

    @staticmethod
    def filter_by_size(products, size):
        for product in products:
            if product.size == size:
                yield product

    def filter_by_size_and_color(self, products, size, color):
        for product in products:
            if product.color == color and product.size == size:
                yield product


class Specification:
    def is_satisfied(self, item):
        pass

    # and operator makes life easier
    def __and__(self, other_spec) -> 'AndSpecification':
        return AndSpecification(self, other_spec)


class Filter:
    def filter(self, items, spec):
        pass


class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, item) -> bool:
        return item.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, item) -> bool:
        return item.size == self.size


# This specification display more understandable but less scalable and flexible logic
# class AndSpecificationSimple(Specification):
#     def __init__(self, spec1, spec2):
#         self.spec2 = spec2
#         self.spec1 = spec1
#
#     def is_satisfied(self, item) -> bool:
#         return self.spec1.is_satisfied(item) and \
#                self.spec2.is_satisfied(item)


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args: list = args

    def is_satisfied(self, item) -> bool:
        return all(map(lambda spec: spec.is_satisfied(item), self.args))


class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


# usage example
if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('House', Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    ###########################################################
    # pf = ProductFilter()
    # print('Green products (old):')
    # for p in pf.filter_by_color(products, Color.GREEN):
    #     print(f' - {p.name} is green')
    ###########################################################
    # ^ BEFORE (example for a bad ProductFilter with the need to add logic for each filter variation)

    # v AFTER (we have more scalable and flexible filter
    # and we dont need update old logic for creating more filters)
    ###########################################################
    bf = BetterFilter()

    print('Green products (new):')
    green_spec = ColorSpecification(Color.GREEN)
    for p in bf.filter(products, green_spec):
        print(f' - {p.name} is green')

    print('Large products (new):')
    large_spec = SizeSpecification(Size.LARGE)
    for p in bf.filter(products, large_spec):
        print(f' - {p.name} is large')

    print('Large blue items (new):')
    # large_blue_spec = AndSpecification(large, ColorSpecification(Color.BLUE))
    large_blue_spec = large_spec & ColorSpecification(Color.BLUE)
    for p in bf.filter(products, large_blue_spec):
        print(f' - {p.name} is large and blue')
    ###########################################################
