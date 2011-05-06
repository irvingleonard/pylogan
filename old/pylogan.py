#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyliblogan
import xml
import xml.dom

class pylogan(object):
  def __init__(self,out_dir):
    self.syslog_file='syslog'
    self.engine=pyliblogan.squid()
    self.grapher=pyliblogan.rrdgraph(out_dir)

  #def getUsers(self):
    #self.users={}
    #for user in self.engine.getUsers():
      #self.users[user]=sara.squid_user(user)
      #self.users[user].populateFromSyslog(self.engine)
    #return self.users
  
  def graphUsers(self):
    self.grapher.graphUsers(self.engine)
    return self.grapher.graphfile
  
  def getData(self):
    userData={}
    for user in self.engine.users.keys():
      userData[user]=[str(self.engine.users[user]._getConsumption())]
    return userData
  
  def process(self):
    self.engine.source(self.syslog_file)
    self.engine.explodeData()
    self.engine.getUsers()
    return self.graphUsers()


    

the_run=pylogan('/var/www/pylogan/webroot/')
the_page=pageMaker('/var/www/pylogan/webroot/')
grf_file=the_run.process()
the_page.setData('Utilización del Proxy Squid',grf_file,the_run.getData())
the_page.writeFile()
