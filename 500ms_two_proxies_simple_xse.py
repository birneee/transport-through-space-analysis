#!/usr/bin/env python

code = open('72ms.py').read()
code = code.replace('./data/72ms/qperf', './data/500ms_two_proxies_simple_xse/qperf')
exec(code)
