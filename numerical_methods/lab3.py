"""

Лабораторная работа #3
Вариант 9

"""
import math
f = lambda x: math.pow(x,2) + math.log10(x) - 1.25
a = float(input('Левая граница равна: '))
b = float(input('Правая граница равна: '))
epsi = 0.0001
def method(a, b, epsi, f):
    while math.fabs(b - a) > epsi:
        a = b -(b - a) * f(b)/(f(b)- f(a))
        b = a + (a- b) * f(a)/(f(a) - f(b))
        print  ('a = ', a, 'b = ', b, 'f(a) = ', f(a), 'f(b)', f(b))
        return b
print('Ответ: ',method(a, b, epsi, f))
