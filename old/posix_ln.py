#!python 
# -*- coding: utf-8 -*-


import subprocess

def PyloganInstall():
  """Make the symbolic links to easy things
  
  The idea is linking the package to /usr/lib/python what ever and the bin (pyloagn_bin) to /usr/bin .
  Don't have the knowledge nither time to do it.
  """
  sysctl_call = subprocess.Popen(('ln','-s','pylogan','/usr/lib/python2.6/pylogan'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  stdout_text, stderr_text = sysctl_call.communicate()

  sysctl_call = subprocess.Popen(('ln','-s','pylogan_bin.py','/usr/bin/pylogan_bin.py'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  stdout_text, stderr_text = sysctl_call.communicate()
  
def PyloganUninstall():
  """Remove the package and bin from the system tree
  
  Exactly the opposite of PyloganInstall
  """
  
  sysctl_call = subprocess.Popen(('rm','/usr/lib/python2.6/pylogan'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  stdout_text, stderr_text = sysctl_call.communicate()

  sysctl_call = subprocess.Popen(('rm','/usr/bin/pylogan_bin.py'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
  stdout_text, stderr_text = sysctl_call.communicate()
  