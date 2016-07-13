from . import pd
from . import np
from . import rt
from . import ll

import abc

DEBUG = False

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
        self._chain = rt.TChain("tpcfifo_tpcfifo_tree")
        self._chain.AddFile(rootfile)
        self._nevents = self._chain.GetEntries()
        
    ###Abstracts
    
    @abc.abstractmethod
    def __load_event__(self,ev_fifo,evt_num):
        """Load event meaningfully"""
    
    #### Class methods

    def get_event(self,event_num) :
        print "self pointer is ",self
        
        # I already loaded this event, return it
        if DEBUG:
            print "Checking get_event condition on event_num",event_num
            
        if pd.isnull(self._events.ix[event_num]['n_words']) is False:
            if DEBUG:
                print "event_num: ",event_num," and I already loaded this event, returning ",self._events.ix[event_num]
                
            return self._events.ix[event_num]
        
        # Get event from TChain
        if DEBUG:
            print "Getting the event from TChain"
        self._chain.GetEntry(event_num) 


        ev_fifo = self._chain.tpcfifo_tpcfifo_branch
        evt_num = ev_fifo.event_number() 

        if DEBUG:
            print "Setting self._chain.tpcfifo_tpcfifo_branch ",ev_fifo
            print "Event number from TTree is ",evt_num
            
        # assert evt_num == event_num, "Offset in recieved event and requested event. {} vs {}".format(evt_num,event_num)            
        # Fill out event as you please
        if DEBUG:
            print "Loading event with ",self.__load_event__," with ev_fifo ",ev_fifo," and evt_num ",evt_num
            
        self._events.ix[event_num] = self.__load_event__(ev_fifo,evt_num)

        # Return slice on dataframe
        if DEBUG:
            print "Returning a slice on the dataframe with self._events.ix[",evt_num,"]"
            
        return self._events.ix[event_num]
