#!/usr/bin/env python

code = open('72ms.py').read()
code = code.replace('./data/72ms/qperf', './data/72ms_two_proxies_simple/qperf')
exec(code)
