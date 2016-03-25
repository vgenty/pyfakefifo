from fifo import Fifo

class SNFifo(Fifo):

    def __load_event__(self,ev_fifo,evt_num):
        event = {}
        
        event['frame_number'] = ev_fifo.event_frame_number()
        event['n_words']      = ev_fifo.nwords()
        event['trig_tick']    = ev_fifo.fem_trig_sample_number_RAW() 
   
        for i in xrange(64):
            event[self._ch(i)] = []
        
        # previous channel, previous time
        ptime,pch = 0,0;
        
        # time offset counter
        toffset = 0

        for i in xrange(ev_fifo.size()):
            ch_fifo = ev_fifo[i]
            time    = ch_fifo.readout_sample_number_RAW()
            ch      = ch_fifo.channel_number()
            
            if ch_fifo.size() and time > 0xfff:
                time = 0
                
            assert time <= 0xfff, "Time is 12 bit value, this one is invalid: {}".format(time)
            
            if ptime > time and pch == ch:
                toffset += 1
        
            if pch != ch:
                toffset = 0
                
            ptime = time
            pch   = ch
 
            for t in xrange(ch_fifo.size()):
                event[self._ch(ch)].append( (time+t+toffset*0xfff,ch_fifo[t]) )
        
        #convert channels to numpy arrays
        for i in xrange(64):
            event[self._ch(i)] = np.array(event[self._ch(i)])

        return event
