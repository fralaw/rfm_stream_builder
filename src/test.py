import datetime

from Rfm import Rfm
from Example import Example

ogg = Rfm(3, 4, 5)
ogg2 = Example(5)
ogg3 = Rfm(1, 2, 3)

ogg2.addExample(ogg)
ogg2.addExample(ogg3)
for x in range(len(ogg2.getDesc())):
    ogg2.getDesc()[x].toScore()
