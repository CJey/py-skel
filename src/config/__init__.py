# -*- coding: utf-8 -*-

import sys, os
import yaml

config = {}

Debug = False
DebugFlask = False

def Default():
    __py_dir__ = os.path.split(os.path.realpath(__file__))[0]
    __top_dir__ = os.path.dirname(os.path.dirname(__py_dir__))
    cfg = os.path.join(__top_dir__, "config.yaml")

    for i, v in enumerate(sys.argv):
        if v == '--config':
            if i == len(sys.argv) - 1:
                print('No configuration file found after --config flag')
                sys.exit(1)
            cfg = sys.argv[i+1]
            sys.argv.pop(i)
            sys.argv.pop(i)
            break

    return UseFile(cfg)

def Use(cfg):
    global config
    global Debug, DebugFlask
    config = cfg

    if 'debug' in config:
        if 'generic' in config['debug']:
            Debug = config['debug']['generic'] == True
        if 'flask' in config['debug']:
            DebugFlask = config['debug']['flask'] == True

    return config

def UseFile(fpath):
    return Use(ParseFile(fpath))

def ParseFile(fpath):
    try:
        f = open(fpath, 'r')
    except Exception as e:
        print('Cannot read config file: %s' % fpath)
        print(e)
        sys.exit(1)
    try:
        return yaml.load(f)
    except Exception as e:
        print('Invalid yaml file format: %s' % fpath)
        print(e)
        sys.exit(1)

def Get(key=None):
    global config
    if key == None:
        return config
    if key in config:
        return config[key]
    return {}

Default()
