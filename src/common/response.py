# -*- coding: utf-8 -*-

def Error(code, msg, debug=None):
    ret = {
        "errcode": code,
        "errmsg": msg,
    }
    if debug != None:
        ret["_debug"] = debug
    return ret
