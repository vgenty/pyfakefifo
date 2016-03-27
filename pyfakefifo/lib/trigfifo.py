from . import pd
from . import np

from fifo import Fifo

class TrigFifo(Fifo):
        
    def __load_event__(self,ev_fifo,evt_num):
        event = {}
        event['frame_number'] = ev_fifo.event_frame_number()
        event['n_words']      = ev_fifo.nwords()
        event['trig_tick']    = ev_fifo.fem_trig_sample_number_RAW() 

        for i in xrange(ev_fifo.size()): #in trigger sample this is channel wise
            ch_fifo = ev_fifo[i]
            event[self._ch(i)] = np.array([(j,ch_fifo[j]) for j in xrange(ch_fifo.size())])

        return event
