# -*- coding: utf-8 -*-


"""Wareki (和暦) : Japanese style way of counting years

Author: 古川貴之


和暦の表現方法

>>> Wareki(Gengo('平成'), 32)
Wareki(Gengo('平成'), 32)

>>> S(39)
Wareki(Gengo('昭和'), 39)

>>> str(H(32))
'平成32年'


西暦を和暦に変換する

>>> Wareki.from_ad(2020)
Wareki(Gengo('平成'), 32)


和暦を西暦に変換する

>>> H(32).to_ad()
2020

# 次のように、int()に渡すこともできます。
>>> int(H(32))
2020
"""

import datetime as _datetime

_gengo_table = (
    {
        "name": "明治",
        "started": _datetime.date(1868, 1, 1),
        "ended": _datetime.date(1912, 7, 29)
    },
    {
        "name": "大正",
        "started": _datetime.date(1912, 7, 30),
        "ended": _datetime.date(1926, 12, 24)
    },
    {
        "name": "昭和",
        "started": _datetime.date(1926, 12, 25),
        "ended": _datetime.date(1989, 1, 7)
    },
    {
        "name": "平成",
        "started": _datetime.date(1989, 1, 8),
        "ended": None
    }
)


class Gengo:
    '''元号

    >>> Gengo('平成')(32)
    Wareki(Gengo('平成'), 32)

    TODO: 明治より前の元号をサポート。
    '''

    def __init__(self, name):
        self._name = name
        for i in _gengo_table:
            if i['name'] == name:
                self._started = i['started']
                self._ended = i["ended"]
                break
        else:
            raise ValueError()

    @classmethod
    def from_date(cls, dt):
        for i in reversed(_gengo_table):
            started = i["started"]
            if dt > started:
                gengo = cls(i["name"])
                break
        else:
            raise ValueError()
        return gengo

    @property
    def name(self):
        return self._name

    @property
    def started(self):
        return self._started

    @property
    def ended(self):
        return self._ended

    @classmethod
    def get_current(cls):
        return cls(_gengo_table[-1]['name'])

    def __str__(self):
        return self.name

    def __repr__(self):
        s = __class__.__name__ + "('" + self.name + "')"
        return s

    def __eq__(self, other):
        return self.name == other.name

    def __contains__(self, date):
        left = self.started <= date
        if self == __class__.get_current():
            right = True
        else:
            right = date <= self.ended
        return left and right

    def __call__(self, year):
        """和暦を返す"""
        return Wareki(self, year)

# アルファベット
M = Gengo('明治')
T = Gengo('大正')
S = Gengo('昭和')
H = Gengo('平成')

def _ad2gengo(year):
    return Gengo.from_date(_datetime.date(year, 12, 31))

class Wareki:
    """和暦を元号と年で表現するクラス"""
    def __init__(self, gengo, year):
        """Constructor.
        """
        self._gengo = gengo
        self._year = year

    @classmethod
    def from_ad(cls, year):
        gengo = _ad2gengo(year)
        obj = cls(
            gengo,
            year - gengo.started.year + 1
        )
        return obj

    @property
    def gengo(self):
        '''元号'''
        return self._gengo

    @property
    def year(self):
        return self._year

    def __repr__(self):
        s = '{}({}, {})'.format(
            __class__.__name__, repr(self.gengo), self.year
        )
        return s

    def __str__(self):
        gengo = str(self.gengo)
        #year = '元' if self.year == 1 else self.year
        year = self.year
        s = '{}{}年'.format(gengo, year)
        return s

    def to_ad(self):
        return self.gengo.started.year + self.year - 1

    __int__ = to_ad



class WarekiDate(_datetime.date):
    """和暦を用いた日付表現"""
    @classmethod
    def from_ad(cls, date):
        obj = cls(
            Wareki.from_ad(date.year),
            date.month,
            date.day
        )
        return obj

    @property
    def wareki(self):
        return Wareki.from_ad(self.year)

    def __str__(self):
        return '{}{}月{}日'.format(self.wareki, self.month, self.day)

    def __repr__(self):
        s = '{}({}, {}, {})'.format(
            __class__.__name__,
            repr(self.wareki), self.month, self.day
        )
        return s

    def to_date(self):
        return _datetime.date(self.wareki, self.month, self.day)


if __name__ == '__main__':
    pass
