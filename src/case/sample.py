# -*- coding: utf-8 -*-

from case.polymer import Polymer

TimeWords = Polymer(
    ['今天', '明天', '后天'],
    Polymer.Range(8, 13),
    '点',
)

DriveWords = Polymer(
    ['开车', '步行', '坐地铁'],
    '去',
)

EventWords = Polymer(
    ['吃饭', '上班', '开会'],
)

Cases = Polymer(TimeWords, DriveWords.OR(), EventWords)
