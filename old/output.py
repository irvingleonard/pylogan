#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import random
#import pyrrd.rrd
#import pyrrd.graph
import xml
import xml.dom


class RRDTool(object):
  """Output related to RRDTool
  
  A simple class using the PyRRD, easy and simple RRD and Graph build
  It uses a 1 second resolution (resolution of syslog)
  """
  def __init__(self,file_name,out_dir='./'):
    self.start=None
    self.heartbeat=1
    self.xff=0.5
    self.steps=1
    self.rows=None
    self.out_dir=out_dir
    #self.filename=''
    #self.graphfile=''
    self.filename=file_name+'.rrd'
    self.graphfile=file_name+'.png'
    
    self.width=700
    self.height=300
    self.line_width=10
    
    self.color={'r':random.randint(10, 99),'g':random.randint(10, 99),'b':random.randint(10, 99)}

  def AColor(self):
    """Get a random color in #RRGGBB
    
    Needed to be reimplemented, it need to use hex notation (colors in this format range from 00 to ff)
    """
    for letr in self.color.keys():
      self.color[letr]+=random.randint(10, 30)
      if self.color[letr] >= 100:
	self.color[letr]+=-100
      if self.color[letr] < 10:
	self.color[letr]+=random.randint(10, 30)
    return '#'+str(self.color['r'])+str(self.color['g'])+str(self.color['b'])

  def SaveTimelines(self,timelines):
    """Builds an RRD with the timelines
    
    The build of an RRD can be time consuming, requires a lot of I/O and CPU (for large RRDs like all domains)
    """
    self.dss=[]
    self.rras=[]
    self.start=timelines[timelines.keys()[0]].begining
    self.rows=timelines[timelines.keys()[0]].end-timelines[timelines.keys()[0]].begining
    for desc in timelines.keys():
      self.dss.append(pyrrd.rrd.DS(ds_name=desc, ds_type='ABSOLUTE', heartbeat=self.heartbeat))
    self.rras.append(pyrrd.rrd.RRA(cf='AVERAGE', xff=self.xff, steps=self.steps, rows=self.rows))
    self.rrd=pyrrd.rrd.RRD(self.out_dir+self.filename, ds=self.dss, rra=self.rras, start=self.start-1, step=1)
    self.rrd.create()
    
    for time_stamp in range(self.start,self.start+self.rows+1):
      param_tupl=()
      for desc in timelines.keys():
	param_tupl+=(timelines[desc].time[time_stamp],)
      self.rrd.bufferValue(time_stamp,*param_tupl)
      if time_stamp % 100 == 0:
	self.rrd.update()
    self.rrd.update()

  def GraphTimelines(self,timelines,tmp_rrd=False):
    """Build a graph from the timelines
    
    The 'real' method, the idea, feed the timeline and it will build an RRD and later a graph from it
    """
    if tmp_rrd:
      self.SaveTimelines(timelines)
    self.defs={}
    self.lines={}
    for desc in timelines.keys():
      self.defs[desc]=pyrrd.graph.DEF(rrdfile=self.out_dir+self.filename, vname='def'+desc, ds_name=desc, cdef='AVERAGE')
      self.lines[desc]=pyrrd.graph.LINE(width=self.line_width, def_obj=self.defs[desc], color=self.AColor(), legend=desc)
    tograph=[]
    for the_def in self.defs.keys():
      tograph.append(self.defs[the_def])
    for the_line in self.lines.keys():
      tograph.append(self.lines[the_line])
	
    g=pyrrd.graph.Graph(self.out_dir+self.graphfile, start=self.start, end=self.start+self.rows, vertical_label='bytes', imgformat='PNG', width=self.width, height=self.height)
    g.data.extend(tograph)
    g.write()
    
    if tmp_rrd:
      os.unlink(self.out_dir+self.filename)


class XHTML(object):
  """Web output, using XHTML
  
  A class to build a page with processed data
  """
  def __init__(self,out_dir='./'):
    self.filename='index.xhtml'
    self.title=None
    self.grf_file_path=False
    self.user_data=False
    self.out_dir=out_dir
    self.blocks={}
    
    self.dom_imp = xml.dom.getDOMImplementation()
    self.doctype = self.dom_imp.createDocumentType('html','-//W3C//DTD XHTML 1.0 Transitional//EN','http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd')
    self.doc = self.dom_imp.createDocument('http://www.w3.org/1999/xhtml','html',self.doctype)
    self.doc.documentElement.setAttribute('xmlns','http://www.w3.org/1999/xhtml')
    
    self.__CreateHead()
    self.__CreateBody()

  def WriteFile(self,pretty=False):
    """Writes the XHTML file in self.out_dir+self.filename
    
    Actualy writes the file, this is the final method to get the phisical output
    """
    xhtml_file=open(self.out_dir+self.filename,'w')
    if pretty:
      xhtml_file.write(self.BuildContent().toprettyxml())
    else:
      xhtml_file.write(self.BuildContent().toxml())
    xhtml_file.close()
  
  def __CreateHead(self):
    """Builds the 'default' head in self.head
    
    It also append the head to the document
    """
    self.head=self.doc.createElement('head')
    self.doc.documentElement.appendChild(self.head)
    
    meta=self.doc.createElement('meta')
    self.head.appendChild(meta)
    meta.setAttribute('HTTP-EQUIV','Refresh')
    meta.setAttribute('CONTENT','300')
    
    meta=self.doc.createElement('meta')
    self.head.appendChild(meta)
    meta.setAttribute('HTTP-EQUIV','Cache-Control')
    meta.setAttribute('CONTENT','no-cache')
    
    meta=self.doc.createElement('meta')
    self.head.appendChild(meta)
    meta.setAttribute('HTTP-EQUIV','Pragma')
    meta.setAttribute('CONTENT','no-cache')
    
    link=self.doc.createElement('link')
    self.head.appendChild(link)
    link.setAttribute('rel','stylesheet')
    link.setAttribute('href','pylogan.css')
    link.setAttribute('type','text/css')

  def __CreateBody(self):
    """Builds the 'empty' body in self.body
    
    It also append the body to the document
    """
    self.body=self.doc.createElement('body')
    self.doc.documentElement.appendChild(self.body)
  
  def SetTitle(self,title_text):
    """Set the page 'big' description
    
    It appends the <title> tag to the head and an <h1> tag to the body
    """
    self.title=title_text
    
    title=self.doc.createElement('title')
    self.head.appendChild(title)
    title.appendChild(self.doc.createTextNode(self.title))
    
    title=self.doc.createElement('h1')
    self.body.appendChild(title)
    title.appendChild(self.doc.createTextNode(self.title))
  
  def CreateBlock(self,blk_id,blk_desc):
    """Builds a <div> with blk_id ID and save in self.blocks
    
    Is 'the' method, the blocks are for the diferents reports.
    Each report (title, file, table) should use a different block.
    The blocks are not appended to the doc in this method.
    """
    block=self.doc.createElement('div')
    block.setAttribute('id',blk_id)
    self.blocks[blk_id]=block
    title=self.doc.createElement('h2')
    block.appendChild(title)
    title.appendChild(self.doc.createTextNode(blk_desc))
  
  def IncludeImage(self,blk_id,grf_file_path):
    """Adds an <img> tag to the block
    
    Used to include an RRDTool graphic in the report
    """
    graph=self.doc.createElement('img')
    self.blocks[blk_id].appendChild(graph)
    graph.setAttribute('src',grf_file_path)
    graph.setAttribute('alt',grf_file_path)

  def __CreateTable(self,data):
    """Builds a <table> from data and returns it
    
    It builds a table from a dictionary, used to actualy show the totals.
    The table is not appended anywhere, just returned
    """
    table=self.doc.createElement('table')
    tr=self.doc.createElement('tr')
    table.appendChild(tr)
    heading=data.pop(0)
    th=self.doc.createElement('th')
    th.setAttribute('align','left')
    tr.appendChild(th)
    th.appendChild(self.doc.createTextNode(heading[0]))
    th=self.doc.createElement('th')
    tr.appendChild(th)
    th.appendChild(self.doc.createTextNode(' '))
    th=self.doc.createElement('th')
    tr.appendChild(th)
    th.appendChild(self.doc.createTextNode(heading[1]))
    for arec in data:
      tr=self.doc.createElement('tr')
      table.appendChild(tr)
      td=self.doc.createElement('td')
      td.setAttribute('class','property')
      tr.appendChild(td)
      td.appendChild(self.doc.createTextNode(arec[0]))
      td=self.doc.createElement('td')
      td.setAttribute('class','separator')
      tr.appendChild(td)
      td.appendChild(self.doc.createTextNode('-'))	
      td=self.doc.createElement('td')
      td.setAttribute('class','value')
      tr.appendChild(td)
      td.appendChild(self.doc.createTextNode(arec[1]))
    return table
    
  def IncludeTable(self,blk_id,data):
    """Builds a table with data and appends it to the blk_id block
    
    It just calls the __CreateTable method and appends the returned table to the block
    """
    self.blocks[blk_id].appendChild(self.__CreateTable(data))

  def BuildContent(self):
    """Append all the blocks to the document
    
    It is used to append the blocks after they have been created.
    Better is to use the DOM but validation in python at the moment sucks, so there is no easy way to use doc.getElementById (the pretty way to work)
    """
    for blk in self.blocks.keys():
      self.body.appendChild(self.blocks[blk])
    return self.doc
  