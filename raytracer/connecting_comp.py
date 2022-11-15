import numpy as np
import random

def offset():
    num = round(int(random.random() * 5 % 5) * 0.1 + 0.2, 1)
    sign = random.random()
    if(sign > 0.5):
        return num
    return -num