
import string
import re
import time
from logan_errors import *

class SyslogLine(object):
  """Structural class for every line
  
  It happend to be a struct to accomodate a line data after exploding the string
  """
  def __init__(self,line_timestamp,src_host,process_data):
    self.timestamp=line_timestamp
    self.host=src_host
    self.data=process_data
    
  def AsTextLine(self):
    text='Timestamp: '+str(self.timestamp)+"\n"
    text+="Host: "+str(self.host)+"\n"
    text+="Data: "+str(self.data)+"\n"
    text=="here: "+str(self.here)+"\n"
    return text


log_year=2010
_year=log_year

syslog_format= r'^(\w+\s+\d+\s+\d+:\d+:\d+)\s+([\w\d\.]+)\s+(.*)'

syslog_compiled_format=re.compile(syslog_format)
start_timestamp=False
end_timestamp=False
lines=[]
dbg=False

def SourceFile(logfile):
  """The syslog file to use
  
  Just open the file for reading
  """
  #self.file = open(logfile)
  global file_path
  file_path=logfile

def ParseLine(the_line):
  """Build a SyslogLine object for the_line
  
  It explodes the line and builds a SyslogLine object that returns
  """
  global syslog_compiled_format, _year
  line_result=re.match(syslog_compiled_format,the_line)
  if line_result:
    line_timestamp=time.mktime(time.strptime('%d %s' % (_year, line_result.group(1)),'%Y %b %d %H:%M:%S'))
    line_obj=SyslogLine(line_timestamp,line_result.group(2),string.strip(line_result.group(3)))
    return line_obj
  else:
    raise SyslogInputError("Line doesn't match with syslog format: <line>{0}</line>".format(the_line))

def ExplodeLines():
  """Reads and parses all the lines in the file
  
  It uses the already opened file to read every line and parses it into SyslogLines storing it in self.lines
  """
  global file_path, dbg, start_timestamp, lines, end_timestamp
  last_line=None
  with open(file_path) as filevar:
    for line in filevar:
      try:
	line_result=ParseLine(line)
      except SyslogInputError:
	if dbg: raise
      else:
	if not start_timestamp:
	  start_timestamp=line_result.timestamp
	lines.append(line_result)
	last_line=line_result
    try:
      end_timestamp=last_line.timestamp
    except AttributeError:
      raise SyslogInputError("There where no parseable lines at \"{0}\"".format(file_path))
    else:
      return lines
    
def PopulateLine(line,re_list):
  """Get squid related data from SyslogLine.data
  
  Using re module gets the traffic data from already built SyslogLines
  """
  for re_name, the_re, re_desc in re_list:
    the_match=re.match(the_re,line.data)
    if the_match:
      for index_desc in range(0,len(re_desc)):
	eval('print '+str(index_desc))
	#line.re_desc[index_desc]=the_match.group(index_desc)
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
def PopulateLines(re_list):
  """
  """
  global lines, dbg, file_path
  for cont in range(0,len(lines)):
    try:
      lines[cont]=PopulateLine(lines[cont],re_list)
    except SyslogExplodeError:
      if dbg: raise
  #if len(all_data): return lines #all_data
  #else: raise SyslogExplodeError("There were no explodable lines in {0}".format(file_path))


if __name__ == "__main__":
  dbg=True
  import sys
  SourceFile(sys.argv[1])
  for line in ExplodeLines():
    print line.AsTextLine()