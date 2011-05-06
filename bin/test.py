#!/usr/bin/python
# -*- coding: utf-8 -*-

import pylogext.time

timeline= pylogext.time.Line()
test=pylogext.time.Event('1234554')
timeline.addEvent(test)
print timeline