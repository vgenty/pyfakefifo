from . import pd
from . import np

import ROOT

import abc

#######FIFO base class

class Fifo(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self,rootfile):

        self._load(rootfile)
        self._events = pd.DataFrame(columns=[['frame_number',
                                              'n_words',
                                              'trig_tick']+["ch%d"%i for i in xrange(64)]],
                                    index=np.arange(0,self._nevents))
        self._name = rootfile
        
    ###Utilities
    
    def _ch(self,i):
        return "ch%d"%i

    def _load(self,rootfile) :
        self._chain = ROOT.TChain("tpcfifo_tree")        
        self._chain.AddFile(rootfile)
        self._nevents = self._chain.GetEntries()
     
    ###Abstracts
    
    @abc.abstractmethod
    def __load_event__(self,ev_fifo,evt_num):
        """Load event meaningfully"""
    
    #### Class methods

    def get_event(self,event_num) :
        
        # I already loaded this event, return it
        if pd.isnull(self._events.ix[event_num]['n_words']) is False:
            return self._events.ix[event_num]
        
        # Get event from TChain
        self._chain.GetEntry(event_num-1) 
        
        ev_fifo = self._chain.tpcfifo_branch
        evt_num = ev_fifo.event_number()
        
        assert evt_num == event_num, "Offset in recieved event and requested event. {} vs {}".format(evt_num,event_num)            
        
        # Fill out event as you please
        self._events.ix[evt_num] = self.__load_event__(ev_fifo,evt_num)

        # Return slice on dataframe
        return self._events.ix[evt_num]
