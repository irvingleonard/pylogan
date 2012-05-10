#!/usr/bin/python
# -*- coding: utf-8 -*-

class Event(object):
  """Time Event Class
  
  To populate the timeline
  """ 
  def __init__(self,time=None):
    self.time = time

class Line(object):
  """
  Class for the final timeline
  The objetive of this module is to build a timeline from text log files
  """
  def __init__(self):
    self.timeline = {}
  
  def addEvent(self,event):
    #todo: add timestamp int check
    time=event.time*100
    if time in self.timeline.keys():
      self.timeline[time]=[event]
    else:
      self.timeline[time].append(event)
      