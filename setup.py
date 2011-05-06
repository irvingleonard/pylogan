#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='pylogan',
      version='0.2.2',
      description='Modular Log Analayzer',
      author='Irving Leonard',
      author_email='irvingleonard@gmail.com',
      url='https://launchpad.net/pylogan',
      platforms=['POSIX'],
      license='BSD',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications',
          'Topic :: Internet :: Log Analysis',
          'Topic :: System :: Logging',
          'Topic :: System :: Monitoring',
          'Topic :: System :: Systems Administration',
          ],
      provides=['pylogan'],
      requires=['string','re','time','random','pyrrd','xml',],
      packages=['pylogan',],
      scripts=['pylogan_bin.py',],
      data_files=[
	  ('/var/www/pylogan/webroot/', ['webroot/pylogan.css',]),
	  ('share/pylogan/', ['README',]),
	  ('share/pylogan/', ['changelog',]),
	  ('/etc/cron.d', ['cron.d/pylogan',]),
	  ],
     )