#! /usr/bin/env python3.5
# -*- coding: utf-8 -*-

import os, sys
__py_dir__ = os.path.split(os.path.realpath(__file__))[0]
__top_dir__ = os.path.dirname(__py_dir__)
sys.path.insert(0, os.path.join(__top_dir__, '3rd'))
sys.path.insert(0, os.path.join(__top_dir__, 'src'))

import config
config.Debug      = True
config.DebugFlask = True

import json, time
from case.sample import Cases

def main():
    for v in Cases.GenString():
        _ts = time.time()
        data = v
        _te = time.time()
        data = json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4)
        print(data)
        print('Assumed: {}ms'.format(round((_te - _ts) * 1000)))
        print('---')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt as ki:
        pass
