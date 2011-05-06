# -*- coding: utf-8 -*-
 
  


#class squid_user(object):
  #def __init__(self,username):
    #self._username=username
  
  #def populateFromSyslog(self,syslog_obj):
    #if not isinstance(syslog_obj, syslog):
      #return False
    #self.lines=[]
    #self.start_timestamp=syslog_obj.start_timestamp
    #self.end_timestamp=syslog_obj.end_timestamp
    #for line in syslog_obj.lines:
      #if line.user==self._username:
	#self.lines.append(line)
    #return self.lines
  
  #def useTimeline(self,time_line):
    #self.timeline=time_line
    #self.timeline.fromUser(self)
    #del(self.lines)
    #self.timeline.completeData()
  
  #def sumTimeline(self):
    #for key in self.timeline.time.keys():
      #if isinstance(self.timeline.time[key], list):
	#the_sum=0
	#for line in self.timeline.time[key]:
	  #the_sum+=int(line.size)
	#self.timeline.time[key]=the_sum
  
  #def _getConsumption(self):
    #self.consumption=0
    #self.sumTimeline()
    #for time_stamp in self.timeline.time.keys():
      #self.consumption+=self.timeline.time[time_stamp]
    #return self.consumption
    
  #def __getSites(self):
    #pass

  def __InsertLine(self,line):
    """
    """
    if not self.start_timestamp:
      self.start_timestamp=line.timestamp
    self.end_timestamp=line.timestamp
    self.lines.append(line)
    return True