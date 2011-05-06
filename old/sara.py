#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import time
import re
import os

from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph



class sarapostfix:

  def __init__(self,year):
    #No hago ni cohete
    self.file = ''
    self.__year = year
    self.data = {}
    self.fill_no_from = '<sin from>'
    self.fill_no_recipients = '<sin recipients>'
    self.fill_no_size = '0'

  def source(self,logfile):
    self.file = open(logfile)

  def setData(self,data):
    if data['id'] in self.data: 
      for key in data.keys():
	self.data[data['id']][key]=data[key]
    else:
      self.data[data['id']]=data

  def completeData(self):
    for key in self.data.keys():
      data = {'id':key}
      if 'from' not in self.data[key]:
	data['from'] = self.fill_no_from
      if 'recipients' not in self.data[key]:
	data['recipients'] = self.fill_no_recipients
      if 'size' not in self.data[key]:
	data['size'] = self.fill_no_size
      self.setData(data)

  def insertQuery(self,correo):
    #print correo
    correo['datetime']=str(correo['datetime'])
    correo['size']=str(correo['size'])
    elquery="INSERT INTO mail(id,from_addr,to_addr,size,timestamp) VALUES ('" + correo['id']+correo['datetime'] + "','" + correo['from'] + "','"+correo['recipients']+"','"+correo['size']+"','"+correo['datetime']+"');"
    return elquery

  def getData(self,line):
    line= self.file.readline()
    while not line == '':
      log_data=self.explodeSyslog(line)
      if string.find(log_data['log_process'],'amavis') >= 0 :
	diccio=self.explodeAmavis(log_data['log_process_data'])
	print diccio
	#self.setData(diccio)
      elif string.find(log_data['log_process'],'postfix') >= 0 :
	diccio=self.explodePostfix(log_data['log_process_data'])
	print diccio
	#self.setData(diccio)
      line= self.file.readline()
    return self.data


  #def getData(self):
    #line= self.file.readline()
    #while not line == '':
      #if string.find(line,'from=') >= 0 and string.find(line,'size=') >= 0:
	#diccio=self.explodeFrom(line)
	#self.setData(diccio)
      #elif string.find(line,'to=') > 0 and string.find(string.lower(line),'status=sent') > 0 and string.find(line,'relay=') >= 0 and string.find(line,'delay=') >= 0:
        #diccio=self.explodeTo(line)
	#self.setData(diccio)
      #line= self.file.readline()
    #return self.data

  def explodeSyslog(self,line):
    log_syslog=string.split(line)[0:5]
    data={}
    data['log_timestamp'] = time.mktime(time.strptime('%d %s' % (self.__year, string.join(log_syslog[0:3])),'%Y %b %d %H:%M:%S'))
    data['log_node'] = log_syslog[3]
    data['log_process'] = log_syslog[4]
    data['log_process_data'] = string.join(string.split(line)[5:])
    return data

  def explodeAmavis(self,line):
    data = {}
    data['amavis_action']=string.strip(string.split(line)[1],' ,')
    if (data['amavis_action']!='Passed') and (data['amavis_action']!='Blocked'):
      return False
    if string.find(line,'Message-ID:')>=0:
      data['message_id']=string.strip(line[string.find(line,'Message-ID:')+11:string.find(line,',',string.find(line,'Message-ID:'))]," <>,")
    data['mail_id']=string.strip(line[string.find(line,'mail_id:')+8:string.find(line,',',string.find(line,'mail_id:'))]," <>,")
    data['from_addr']=string.strip(string.split(string.strip(string.split(line,'->')[0],' '),' ')[-1],' <>')
    to_addrs_raw=string.split(string.strip(string.split(string.strip(string.split(line,'->')[1],' '),' ')[0],' ,'), ',')
    data['to_addrs']=[]
    for to_addr in to_addrs_raw:
      data['to_addrs'].append(string.strip(to_addr,' <>'))
    data['amavis_clasif']=string.strip(string.split(line)[2],' ,')
    return data

  def explodeFrom(self,line):
    from_addr = string.strip(line[string.find(line,'from=')+5:string.find(line,'size=')]," <>,")
    size = long(string.split(line[string.find(line,'size=')+5:])[0][:-1])
    datetimestr = string.join(string.split(line)[0:3])
    dtotro = time.mktime(time.strptime('%d %s' % (self.__year,datetimestr),'%Y %b %d %H:%M:%S'))
    #dt = datetime.fromtimestamp(time.mktime(time.strptime('%d %s' % (self.__year,datetimestr),'%Y %b %d %H:%M:%S')))
    #id = "%s%s" % (string.split(line)[5], dt.strftime('%b%d'))
    id = "%s" % (string.split(line)[5])
    #            id = "%s%s" % (string.split(line)[5], dt.strftime('%b%d%H:%M:'))
    #            line_parts = string.split(line)
    #            id = line_parts[5]+line_parts[0]+line_parts[1]+line_parts[2][:-2]
    #data = {'id' : id, 'size' : size, 'from' : from_addr, 'datetime' : dt}
    data = {'id' : id, 'size' : size, 'datetime' : dtotro}
    #data = {'id' : id, 'size' : size, 'datetime' : dt}
    if len(from_addr) > 0:
      data['from'] = from_addr
    return data

  def explodeTo(self,line):
    recipients_addrs = string.strip(line[string.find(line,'to=')+3:string.find(line,'relay=')],'<>,')
    #recipients_addrs = string.split(line[string.find(line,'to=')+3:string.find(line,'relay=')],',')
    #recipients = []
    #for recipient in recipients_addrs:
      #recipient = string.strip(recipient,'<> ')
      #if len(recipient) > 0:
	#recipients.append(recipient)
    #relay = string.strip(string.split(line[string.find(line,'relay=')+6:])[0][:-1],'<>, ')
    #delay = int(string.split(line[string.find(line,'delay=')+6:])[0][:-1])
    #delay =string.split(line[string.find(line,'delay=')+6:])[0]
    datetimestr = string.join(string.split(line)[0:3])
    dtotro = time.mktime(time.strptime('%d %s' % (self.__year,datetimestr),'%Y %b %d %H:%M:%S'))
    #dt = datetime.fromtimestamp(time.mktime(time.strptime('%d %s' % (self.__year,datetimestr),'%Y %b %d %H:%M:%S')))
    #dt_delay = timedelta(seconds=delay)
    #dt -= dt_delay
    #id = "%s%s" % (string.split(line)[5], dt.strftime('%b%d'))
    id = "%s" % (string.split(line)[5])
    #            id = "%s%s" % (string.split(line)[5], dt.strftime('%b%d%H:%M:'))
    #            line_parts = string.split(line)
    #            id = line_parts[5]+line_parts[0]+line_parts[1]+line_parts[2][:-2]            
    #data={'id' : id,'datetime' : dtotro}
    data={'id' : id,'datetime' : dtotro,'recipients': recipients_addrs,}
    #data['recipients'] = recipients[0]
    #data['datetime'] = dtotro
    #data['recipients'] = recipients
    #data['delay'] = delay
    #data['relay'] = relay
    #data['id'] = id
    return data


class sarapreproc:
  def __init__(self):
    self.start_time=time.mktime(time.strptime("11 Mar 2010 00:00:00", "%d %b %Y %H:%M:%S"))
    self.end_time=time.mktime(time.strptime("11 Mar 2010 23:59:59", "%d %b %Y %H:%M:%S"))

  def goodData(self,data):
    gooddata=[]
    for registry in data:
      gooddata.append(string.split(string.replace(string.replace(registry['row'],')',''),'(',''),','))
    return gooddata

  def trafico(self,lista,sentido):
#Hay que revisar este método, viejo, ya no pincha
    trafic = 0
    for correo in lista:
      if correo['sentido'] == sentido:
	trafic+=correo['tamanyo']
    return trafic

  def suma(self,data):
    sumdata={}
    for regist in data:
      if int(regist[1]) in sumdata:
	sumdata[int(regist[1])]+=int(regist[0])
      else: sumdata[int(regist[1])]=int(regist[0])
    return sumdata




  def getData_Query(self):
    query = 'SELECT (size,"timestamp",id) FROM mail WHERE "timestamp" > '+str(self.start_time)+' AND "timestamp" < '+str(self.end_time)+" AND from_addr = 'fcruz@reduim.cu';"
    return query
