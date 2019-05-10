"""

Лабораторная работа #5
Вариант 9

"""
import math
x = float(input(' Введите число x:  '))
epsi = 0.0001
f = lambda x: math.pow(x,2) + math.log10(x) - 1.25
df = lambda x: 2*x  +  1/(x*math.log(10))
while math.fabs(f(x)) > epsi:
    print(x,df(x),f(x))
    break
