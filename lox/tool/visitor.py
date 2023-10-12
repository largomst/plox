from abc import ABC, abstractmethod


class Pastry(ABC):
    @abstractmethod
    def accept(self, visitor: PastryVisitor):
        pass


class Beignet(Pastry):
    def accept(self, visitor: PastryVisitor):
        visitor.visitBeignet(self)


class Cruller(Pastry):
    def accept(self, visitor: PastryVisitor):
        visitor.visitCruller(self)


class PastryVisitor(ABC):
    @abstractmethod
    def visitBeignet(self, beignet: Beignet):
        pass

    @abstractmethod
    def visitCruller(self, cruller: Cruller):
        pass
