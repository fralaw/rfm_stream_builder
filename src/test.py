import datetime

from Rfm import Rfm
from Example import Example
from ExampleSequence import ExampleSequence

rfm_1 = Rfm(3, 4, 5)
rfm_2 = Rfm(1, 2, 3)

example = Example(datetime.date.today())


example.addExample(rfm_1)
example.addExample(rfm_2)
for x in range(len(example.getDesc())):
    example.getDesc()[x].toScore()

example.setLabelTimeStamp('yes')
print(example.getLabelTimeStamp())