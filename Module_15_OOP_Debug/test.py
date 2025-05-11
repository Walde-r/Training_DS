import numpy as np


count = 0
for line in open('Module_15_OOP_Debug/data/res_balls.txt','r',encoding='cp1251'):
    points = int(line.split()[-1])
    if points < 3:
        count += 1