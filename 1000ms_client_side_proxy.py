#!/usr/bin/env python

code = open('72ms.py').read()
code = code.replace('./data/72ms/qperf', './data/1000ms_client_side_proxy/qperf')
exec(code)
