# -*- coding: utf-8 -*-

def human_duration(secs):
    if secs < 10:
        return '{}ms'.format(round(secs*1000))
    if secs < 100:
        return '{}s'.format(round(secs))
    if secs < 6000:
        if secs < 600:
            return '{}m'.format(round(secs/60, 1))
        return '{}m'.format(round(secs/60))
    return '{}h'.format(round(secs/3600, 1))

def ratio(a, b, acc = 1):
    if b == 0:
        return 'N/A'
    return round((a/b*100), acc)
