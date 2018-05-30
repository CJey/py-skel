# -*- coding: utf-8 -*-

import re

class Base(object):
    def __init__(self, conn):
        self.conn = conn

    # abstract method, return table name
    def Name(self):
        return 'foo'

    # abstract method, return the latest table version
    def Version(self):
        return 1

    # abstract method, return the latest table schema
    def Schema(self):
        return '''
        create table `%s` (bar int)
        ''' % (self.Name())

    # dynamic methods, must implement how to do when upgrading table from version X to Y
    #def VerX_VerY(self, cursor):
    #    return

    def getComment(self):
        sql = '''
        select table_comment from information_schema.tables
        where table_name=%s and table_schema=(select database());
        '''

        with self.conn.cursor() as cur:
            cur.execute(sql, self.Name())
            self.conn.commit()
        res = cur.fetchone()
        if res == None:
            return None
        return res[0]

    def burnVersion(self):
        comment = self.getComment()
        if comment == None:
            return
        res = re.findall(r'(^.*\b)version\s*=\s*\d+(\b.*$)', comment)
        if len(res) == 0:
            comment = ', '.join(["version = %d" % (self.Version()), comment])
        else:
            comment = res[0][0] + "version = %d" % (self.Version()) + res[0][1]

        with self.conn.cursor() as cur:
            cur.execute('alter table `' + self.Name() + '` comment = %s', (comment))
            self.conn.commit()

    def findVersion(self):
        comment = self.getComment()
        if comment == None:
            return None
        res = re.findall(r'^.*\bversion\s*=\s*(\d+)\b.*$', comment)
        if len(res) == 0:
            return -1
        return int(res[0])

    def Create(self):
        with self.conn.cursor() as cur:
            cur.execute(self.Schema())
            self.conn.commit()
        self.burnVersion()

    def Update(self, vfrom, vto):
        i = vfrom
        j = vto
        while i < vto:
            name = 'Ver%d_Ver%d' % (i, j)
            if hasattr(self, name):
                print("Upgrading table %s, ver %d --> ver %d" % (self.Name(), i, j))
                with self.conn.cursor() as cur:
                    getattr(self, name)(cur)
                    self.conn.commit()
                self.burnVersion()
                i = j
                j = vto
            else:
                j -= 1
                if j == i:
                    print("ERROR!!! Can not found upgrade path ver %d --> ver %d" % (vfrom, vto))
                    return False
        return True

    def AutoUpdate(self):
        ver = self.findVersion()
        if ver == None:
            print("Creating new table --> %s [ver %d]" % (self.Name(), self.Version()))
            self.Create()
            return
        if ver < 0:
            print("ERROR!!! No version found of table --> %s" % (self.Name()))
            return

        if ver > self.Version():
            print("Warning!!! Version of table %s is newer than us %d > %d" % (self.Name, ver, self.Version()))
            return

        ok = True
        if ver < self.Version():
            ok = self.Update(ver, self.Version())

        if ok:
            print("Latest table --> %s [ver %d]" % (self.Name(), self.Version()))

    def Drop(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("drop table `%s`" % (self.Name()))
                self.conn.commit()
            return True
        except:
            return False

    def Truncate(self):
        with self.conn.cursor() as cur:
            cur.execute("truncate table `%s`" % (self.Name()))
            self.conn.commit()
