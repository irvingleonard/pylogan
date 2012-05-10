#!/usr/bin/python 
# -*- coding: utf-8 -*-

import re
from logan_errors import *


res=[('squid_general',r'^\s*(squid\s*\[\d+\]):\s*[\d\.]+\s+\d+\s+(\d+\.\d+\.\d+\.\d+)\s+(\w*/\d{3})\s(\d*)\s(GET|POST|CONNECT|HEAD)\s(.*)\s(\w*)\s\w*/\d*\.\d*\.\d*\.\d*.*',['sourceIp','squidEvent','size','method','url','user'])
]

class Timeline(object):
  """Structural class for related data
  
  Used for ...
  """
  def __init__(self,start_timestamp,end_timestamp,genre=False,descriptor=False,descriptorValue=False):
    self.begining=int(start_timestamp)
    self.end=int(end_timestamp)
    self.genre=genre
    self.descriptor=descriptor
    self.descriptorValue=descriptorValue
    self.time={}
    
  def AddValue(self,time_stamp,value):
    time_stamp=int(time_stamp)
    if time_stamp not in self.time.keys():
      self.time[time_stamp]=value
    else:
      self.time[time_stamp]+=value
    return self.time[time_stamp]


def GetUsers(lines):
  """
  """
  start_timestamp=lines[0].timestamp
  end_timestamp=lines[len(lines)-1].timestamp
  users={}
  for line in lines:
    if line.user not in users.keys():
      users[line.user]=Timeline(start_timestamp,end_timestamp,'SquidUser','User',line.user)
    users[line.user].AddValue(line.timestamp,int(line.size))
  return users

def GetDomains(lines):
  """
  """
  start_timestamp=lines[0].timestamp
  end_timestamp=lines[len(lines)-1].timestamp
  domains={}
  domain_re=re.compile(r'(?:\w{3,5}://)?(\S*?)((:((443)|(5222))(?=$))|(/.*))')
  for line in lines:
    domain_result=re.match(domain_re,line.url)
    domain=domain_result.group(1)
    if domain not in domains.keys():
      domains[domain]=Timeline(start_timestamp,end_timestamp,'SquidDomain','Domain',domain)
    domains[domain].AddValue(line.timestamp,int(line.size))
  return domains

def GetNavigations(lines):
  """
  
  """
  start_timestamp=lines[0].timestamp
  end_timestamp=lines[len(lines)-1].timestamp
  navigations={}
  domain_re=re.compile(r'(?:\w{3,5}://)?(\S*?)((:((443)|(5222))(?=$))|(/.*))')
  for line in lines:
    domain_result=re.match(domain_re,line.url)
    if domain_result:
      if line.user+'@'+line.sourceIp+' >> '+domain_result.group(1) not in navigations.keys():
	navigations[line.user+'@'+line.sourceIp+' >> '+domain_result.group(1)]=Timeline(start_timestamp,end_timestamp,'SquidNavigation','Navigation',line.user+line.sourceIp+domain_result.group(1))
      navigations[line.user+'@'+line.sourceIp+' >> '+domain_result.group(1)].AddValue(line.timestamp,int(line.size))
    else:
      print line.url, line.squidEvent
  return navigations

def TopDomains(lines,cant=10):
  """
  """
  domains=GetDomains(lines)
  domains_sum=SumSizes(domains)
  domai=[]
  for domain in domains_sum.keys():
    domai.append((domains_sum[domain],domain))
  domai.sort()
  domai.reverse()
  domai=domai[0:cant-1]
  top_domains={}
  for trf_size, domain in domai:
    top_domains[domain]=domains[domain]
  return top_domains

def TopNavigations(lines,cant=10):
  """
  """
  navigations=GetNavigations(lines)
  navigations_sum=SumSizes(navigations)
  navi=[]
  for navigation in navigations_sum.keys():
    navi.append((navigations_sum[navigation],navigation))
  navi.sort()
  navi.reverse()
  navi=navi[0:cant-1]
  top_navigations={}
  for trf_size, navigation in navi:
    top_navigations[navigation]=navigations[navigation]
  return top_navigations


def EscapeNames(data,esc_char='_'):
  """
  """
  pattern=re.compile(r'(192.168.)|([^\w]+)')
  new_data={}
  for key in data.keys():
    new_data[re.sub(pattern,esc_char,key)[:19]]=data[key]
  return new_data

def CompleteData(data,complete_value=0):
  """
  """
  for time_stamp in range(data.begining,data.end+1):
    if time_stamp not in data.time:
      data.time[time_stamp]=complete_value
  return data

def SumSizes(data):
  """
  """
  sizes={}
  for desc in data.keys():
    sizes[desc]=0
    for time_stamp in data[desc].time.keys():
      sizes[desc]+=data[desc].time[time_stamp]
  return sizes

def SanitizeSizes(data):
  sizes = data.items()
  sizes.sort(key=lambda sizes:sizes[1], reverse=True)
  
  newsizes=[]
  for elem in sizes:
    newsizes.append((elem[0],__ConvertSizes(elem[1])))
  
  return newsizes

def __ConvertSizes(bytes):
    """Convert bytes to KB and  MB

    """
    if bytes >= 1048576:
      return str(round(bytes/1024.0/1024.0, 2)) + ' MB'
    elif bytes >= 1024:
      return str(round(bytes/1024.0, 2)) + ' KB'
    elif bytes < 1024:
      return str(bytes) + ' Bytes'


class Squid():
  """
  """
  def __init__(self):
    self.frmt_consume=r'^\s*(squid\s*\[\d+\]):\s*[\d\.]+\s+\d+\s+(\d+\.\d+\.\d+\.\d+)\s+(\w*/\d{3})\s(\d*)\s(GET|POST|CONNECT|HEAD)\s(.*)\s(\w*)\s\w*/\d*\.\d*\.\d*\.\d*.*'
    
    self.formats=[
		  ('consume',re.compile(self.frmt_consume)),
		  ]
    self.data=None
    self.dbg=False

  def UseSyslog(self,syslog_object):
    """
    """
    try:
      self.data=syslog_object.ExplodeLines(self.formats)
    except SyslogExplodeError:
      if self.dbg: raise
    

  def Consumption(self):
    """
    """
    new_data=[]
    try:
      for the_thing, data in self.data:
	if the_thing == 'consume':
	  new_data.append(data)
    except TypeError:
      if self.dbg: raise
    return new_data

def DoIt():
  pass

if __name__ == "__main__":
  dbg=True
  #eval 'print "hello"'
  import sys
  import pylogan.syslog
  live=pylogan.syslog
  live.SourceFile(sys.argv[1])
  live.ExplodeLines()
  #print live.ExplodeLines(res)
  for line in live.PopulateLines(res):
    print line.AsTextLine()
  
