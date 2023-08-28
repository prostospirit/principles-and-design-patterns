# The principle of separation of interfaces says that too "thick" interfaces must be divided into smaller
# and more specific ones, so that the programming entities of small interfaces
# know only about the methods that they need to work.
from abc import abstractmethod


class Machine:
    """Bad example when all interfaces are in one class entity"""

    def print(self, document):
        raise NotImplementedError()

    def fax(self, document):
        raise NotImplementedError()

    def scan(self, document):
        raise NotImplementedError()


# it can be ok if you need only a multifunction device
class MultiFunctionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass


class OldFashionedPrinter(Machine):
    def print(self, document):
        # ok - we can declare print logic here
        print(document)

    def fax(self, document):
        """Not supported!"""
        pass  # do nothing because the old printer has no fax, but it has an interface for it

    def scan(self, document):
        """Not supported!"""
        raise NotImplementedError('Printer cannot scan!')  # also old print cant scan, but it also has an interface


# ^ BAD EXAMPLE

# v SOLUTION


class Printer:
    """Only Printer entity for print"""

    @abstractmethod
    def print(self, document): pass


class Scanner:
    """Only Scanner entity for scan"""

    @abstractmethod
    def scan(self, document): pass


# ... and same for Fax, etc.


class MyPrinter(Printer):
    def print(self, document):
        print(document)


class Photocopier(Printer, Scanner):
    def print(self, document):
        print(document)

    def scan(self, document):
        pass  # something meaningful


class MultiFunctionDevice(Printer, Scanner):  # Fax, etc
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass


class MultiFunctionMachine(MultiFunctionDevice):
    def __init__(self, printer, scanner):
        self.printer = printer
        self.scanner = scanner

    def print(self, document):
        self.printer.print(document)

    def scan(self, document):
        self.scanner.scan(document)


# usage example
if __name__ == '__main__':
    old_printer = OldFashionedPrinter()
    old_printer.fax(123)  # nothing happens
    old_printer.scan(123)  # oops!
