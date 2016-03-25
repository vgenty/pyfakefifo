
# coding: utf-8

# In[1]:

get_ipython().magic(u'gui qt')
import pyqtgraph as pg


# In[176]:



# In[177]:

tf = TrigFifo("test123_pt_trig.root")
sf = SNFifo("test123_pt_snova.root")


# In[193]:

e126 = sf.get_event(126)


# In[194]:

get_ipython().magic(u'matplotlib inline')
import matplotlib
import matplotlib.pyplot as plt


# In[196]:

plt.plot(e126['ch10'][:,0],e126['ch10'][:,1])
plt.show()


# In[186]:

e13['ch0']


# In[ ]:



