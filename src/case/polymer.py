# -*- coding: utf-8 -*-

class Polymer():
    ID = 1

    def __init__(self, *units):
        self.units = list(units)
        self.addempty = False
        self.max = 0
        self.id = self.__class__.ID
        self.__class__.ID += 1

    def copy(self):
        p2 = Polymer()
        p2.units = self.units
        p2.addempty = self.addempty
        p2.max = self.max
        p2.id = self.id
        return p2

    def One(self):
        return self.Max(1)

    def Two(self):
        return self.Max(2)

    def Max(self, num):
        if num < 0:
            num = 0
        p2 = self.copy()
        p2.max = num
        return p2

    def OR(self):
        p2 = self.copy()
        p2.addempty = True
        return p2

    def GenString(self, num=0):
        for v in self.Gen(num):
            yield ''.join([vv[1] for vv in v])

    def GenLine(self, num=0):
        for v in self.GenString(num):
            yield (v+'\n')

    def Gen(self, num=0):
        if num <= 0:
            num = self.max
        elif self.max > 0 and num > self.max:
            num = self.max

        if not self.units:
            return (yield [(self.id, '')])

        p = self.units[0]

        cnt = 0

        if len(self.units) == 1:
            if type(p) == str:
                yield [(self.id, p)]
            elif type(p) == self.__class__:
                for v in p.Gen():
                    yield v
                    cnt += 1
                    if cnt == num:
                        break
            elif type(p) in (list, tuple):
                for v in p:
                    v = self.__class__(v)
                    v.id = self.id
                    for vv in v.Gen():
                        yield vv
                        cnt += 1
                        if cnt == num:
                            break
                    if cnt == num:
                        break
            else:
                raise ValueError('invalid unit type')
            if self.addempty:
                yield [(self.id, '')]
            return

        sub = self.__class__(*self.units[1:])
        sub.id = self.id
        if type(p) == str:
            p = [(self.id, p)]
            for v in sub.Gen():
                yield p+v
                cnt += 1
                if cnt == num:
                    break
        elif type(p) == self.__class__:
            for v in p.Gen():
                for vv in sub.Gen():
                    yield v+vv
                    cnt += 1
                    if cnt == num:
                        break
                if cnt == num:
                    break
        elif type(p) in (list, tuple):
            for v in p:
                v = self.__class__(v, sub)
                v.id = self.id
                for vv in v.Gen():
                    yield vv
                    cnt += 1
                    if cnt == num:
                        break
                if cnt == num:
                    break
        else:
            raise ValueError('invalid unit type')
        if self.addempty:
            yield [(self.id, '')]

    @classmethod
    def DigitCN(cls, start, end):
        x = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        ret = []
        for v in range(start, end):
            ret.append(''.join([x[int(vv)] for vv in str(v)]))
        return cls(ret)

    @classmethod
    def Range(cls, start, end):
        return cls([str(v) for v in range(start, end)])

    @classmethod
    def RangeCN(cls, start, end):
        if start < 0 or end > 100:
            raise ValueError('only support [0, 100)')

        zero = '零'
        ten = '十'
        x = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
        ret = []
        for v in range(start, end):
            if v == 0:
                ret.append(zero)
                continue

            a = int(v/10)
            b = v%10
            if a == 0:
                ret.append(x[b])
            elif a == 1:
                ret.append(ten+x[b])
            else:
                ret.append(x[a]+ten+x[b])

        return cls(ret)
