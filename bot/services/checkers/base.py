from abc import ABC, abstractmethod

class BaseChecker(ABC):

    @abstractmethod
    def check(self, value):
        pass