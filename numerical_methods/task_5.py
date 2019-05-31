"""

Лаборатонрая работа #11
Вариант 9

Нахождение значения интеграла по формуле
Симпсона с заданной точностью

"""
import math

n = 1
a = 0.4
b = 1.2
eps = 0.0001
f = lambda x: math.cos(0.63 + 0.5 * x) / (0.4 + math.pow((math.pow(x, 2) + 9), 0.5))

def simpsons_rule(f, a, b, n):
    sum = 0.0
    h = (b - a) / n
    k1 = 0
    k2 = 0
    k2 = f(a + h)
    for i in range(2, n):
        k2 += f(a + (i + 1) * h)
        k1 += f(a + i * h)
    sum = f(a) + f(b) + 4 * k2 + 2 * k1
    sum *= h / 3
    return sum

a_1 = simpsons_rule(f, a, b, n)

while True:
    l = a_1
    n = 2 * n
    a_1 = simpsons_rule(f, a, b, n)
    if math.fabs(a_1 - l) > eps:
        break
print("Метод Симпсона = ", a_1)
