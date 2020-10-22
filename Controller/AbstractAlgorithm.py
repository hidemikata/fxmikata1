from abc import abstractmethod

class AbstractAlgorithm(object):
    @abstractmethod
    def validation(self,data):
        pass

    @abstractmethod
    def number_of_data(self):
        pass

    @abstractmethod
    def judge(self, data):
        pass
