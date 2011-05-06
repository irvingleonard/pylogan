#!/usr/bin/python
# -*- coding: utf-8 -*-


import string
import re
import time
import copy
from pylogan_exception import *


class SyslogLine(object):
  """Structural class for every line
  
  It happend to be a struct to accomodate a line data after exploding the string
  """
  def __init__(self,line_timestamp,src_host,process_data):
    self.timestamp=line_timestamp
    self.host=src_host
    self.data=process_data


class Syslog(object):
  """Base class for syslog input
  
  Contains attributes and methods that belongs to syslog, it isolates the "process data" for later processing
  """
  def __init__(self,log_year=2010):
    self._year=log_year
    
    self.syslog_format= r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+([\w\d\.]+)\s+(.*)'
    
    self.syslog_compiled_format=re.compile(self.syslog_format)
    self.start_timestamp=False
    self.end_timestamp=False
    self.lines=[]
    self.dbg=False
   
  def SourceFile(self,logfile):
    """The syslog file to use
    
    Just open the file for reading
    """
    #self.file = open(logfile)
    self.file_path=logfile
    
  def ParseLine(self,the_line):
    """Build a SyslogLine object for the_line
    
    It explodes the line and builds a SyslogLine object that returns
    """
    line_result=re.match(self.syslog_compiled_format,the_line)
    if line_result:
      line_timestamp=time.mktime(time.strptime('%d %s' % (self._year, line_result.group(1)),'%Y %b %d %H:%M:%S'))
      line_obj=SyslogLine(line_timestamp,line_result.group(2),string.strip(line_result.group(3)))
      return line_obj
    else:
      raise SyslogInputError("Line doesn't match with syslog format: <line>{0}</line>".format(the_line))

  def PopulateLines(self):
    """Reads and parses all the lines in the file
    
    It uses the already opened file to read every line and parses it into SyslogLines storing it in self.lines
    """
    last_line=None
    with open(self.file_path) as self.file:
      for line in self.file:
	try:
	  line_result=self.ParseLine(line)
	except SyslogInputError:
	  if self.dbg: raise
	else:
	  if not self.start_timestamp:
	    self.start_timestamp=line_result.timestamp
	  self.lines.append(line_result)
	  last_line=line_result
    try:
      self.end_timestamp=last_line.timestamp
    except AttributeError:
      raise SyslogInputError("There where no parseable lines at \"{0}\"".format(self.file_path))
    else:
      return self.lines
    
  def ExplodeLine(self,line,re_list):
    """Get squid related data from SyslogLine.data
    
    Using re module gets the traffic data from already built SyslogLines
    """
    for re_name, the_re in re_list:
      the_match=re.match(the_re,line)
      if the_match:
	return (re_name, the_match)
    raise SyslogExplodeError("Line doesn't match with any of {0} REs: {1}".format(re_list,line))
    #squid_line=re.match(self.compiled_squid_format,the_line.data)
    #if squid_line:
      #isnumbered=re.match(self.squid_get_format,squid_line.group(2))
      #if isnumbered:
	#print squid_line.group(2)
      #the_line.sourceIp=result.group(1)
      #the_line.squidEvent=result.group(2)
      #the_line.size=result.group(3)
      #the_line.method=result.group(4)
      #the_line.url=result.group(5)
      #the_line.user=result.group(6)
      #del(the_line.data)
      #return the_line
      #return result.group(1)
    #else:
      #return False
  def ExplodeLines(self,re_list):
    """
    """
    all_data=[]
    for line in self.lines:
      try:
	data=self.ExplodeLine(line.data,re_list)
      except SyslogExplodeError:
	if self.dbg: raise
      else:
	all_data.append(data)
    if len(all_data): return all_data
    else: raise SyslogExplodeError("There were no explodable lines in {0}".format(self.file_path))

class Squid(Syslog):
  """Input class for line processing
  
  It's the base class for manipulating the data related to squid stored in the syslog file
  """
  def __init__(self):
    super(Squid,self).__init__()
    
    
    
    self.compiled_squid_format=re.compile(self.squid_format)
    
  def ExplodeData(self):
    """Parses all SyslogLines in self.lines
    
    Used to process the squid data after the use of PopulateLines
    """
    last_index=len(self.lines)
    for line_index in range(last_index-1,-1,-1):
      self.lines[line_index]=self.ParseSquid(self.lines[line_index])
      if not self.lines[line_index]:
	del(self.lines[line_index])
    return self.lines
    
  def ParseSquid(self,the_line):
    """Get squid related data from SyslogLine.data
    
    Using re module gets the traffic data from already built SyslogLines
    """
    squid_line=re.match(self.compiled_squid_format,the_line.data)
    if squid_line:
      isnumbered=re.match(self.squid_get_format,squid_line.group(2))
      if isnumbered:
	print squid_line.group(2)
      #the_line.sourceIp=result.group(1)
      #the_line.squidEvent=result.group(2)
      #the_line.size=result.group(3)
      #the_line.method=result.group(4)
      #the_line.url=result.group(5)
      #the_line.user=result.group(6)
      #del(the_line.data)
      #return the_line
      #return result.group(1)
    else:
      return False
      
  def Lines(self):
    """'The' method to use
    
    This is the only method needed in the regular use, it calls the PopulateLines to parse de syslog file and later ExplodeData to get the squid info from that lines
    """
    self.PopulateLines('squid')
    self.ExplodeData()
    return self.lines
