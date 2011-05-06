#!/usr/bin/python
# -*- coding: utf-8 -*-

class loganException(Exception):
  pass

class SyslogInputError(loganException):
  """Error in line
  """
  pass

class SyslogExplodeError(loganException):
  """
  """
  pass

class SquidDataError(loganException):
  """
  """
  pass