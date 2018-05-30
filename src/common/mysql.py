# -*- coding: utf-8 -*-

import pymysql
import config
import time

# Check weather alive every 60s
ServerAliveInterval = 60

conns = {
    #'': {
    #    'conn': None,
    #    'alive': None,
    #}
}

def New(host, port, user, passwd, name):
    return pymysql.Connect(
        host=host,
        port=port,
        user=user,
        passwd=passwd,
        db=name,
        charset='utf8mb4'
    )

def KeepThis(name, conn):
    global conns
    conns[name] = {
        'conn': conn,
        'alive': time.time(),
    }
    return conn

def GetThis(name):
    global conns
    if name not in conns:
        return None

    conn = conns[name]
    if time.time() - conn['alive'] > ServerAliveInterval:
        conn.ping(reconnect=True)
    return conn

def Keep():
    cfg = config.Get('mysql')
    conn = New(cfg['host'], cfg['port'], cfg['user'], cfg['passwd'], cfg['name'])
    return KeepThis('', conn)

def Get():
    conn = GetThis('')
    if conn:
        return conn
    return Keep()

#def KeepABC():
#    cfg = config.Get('abc')
#    conn = New(cfg['host'], cfg['port'], cfg['user'], cfg['passwd'], cfg['name'])
#    return KeepThis('abc', conn)
#
#def GetABC():
#    conn = GetThis('abc')
#    if conn:
#        return conn
#    return Keep()
