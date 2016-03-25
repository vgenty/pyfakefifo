import abc

from lib.trigfifo import  TrigFifo
from lib.snfifo   import  SNFifo

class FakeFifoFactory(object): #It's just a dictionary
    __metaclass__ = abc.ABCMeta

    def __init__(self,name='fakefifofactory'):
        self.name = name
        self.storage = {}

    
    def __getitem__(self, key): # should just return me an object, right?

        if key in self.storage:
            return self.storage[key]
        
        self.storage[key] = self.__add_new_class__(key)

        return self.storage[key]

    def __str__(self):
        return str(self.storage)
    
    @abc.abstractmethod
    def __add_new_class__(self,key):
        """Add new class member to dictionary"""    
    
    
class PyFakeFifo(FakeFifoFactory):
    def __init__(self,name='PyFakeFifoFactory'):
        super().__init__(name)
        self.streams = ['trig','sn']
        
        
    def __add_new_class__(key) :
        stream   = key[0]
        rootfile = key[1]

        assert stream in self.streams, "Given stream {} is not valid.".format(stream)

        if stream == 'trig':
            return TrigFifo(rootfile)

        if stream == 'sn':
            return SNFifo(rootfile)

        raise Exception("Failed adding new class")


    
