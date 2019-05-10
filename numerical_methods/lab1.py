"""

Лабораторная работа #1
Вариант 9

"""
import math
print("Имеется такое нелинейное  уравнение : 2*x^2 - 0.5^x -3 = 0")
a = float(input('Введите левую границу: '))
b =  float(input('Введите правую границу: '))
epsi = 0.0001
f = lambda x: 2*math.pow(x,2) - math.pow(0.5, x) - 3
def main(a, b, f):
    x = (a + b)/2
    while math.fabs(f(x)) >= epsi:
        x = (a + b)/2
        a, b = (a,x) if f(a)*f(x) < 0 else (x,b)
        print('a = ',float('{:.3f}'.format(a)),'; b = ',float('{:.3f}'.format(b)),'; x = ', float('{:.3f}'.format(x)),'; f(x) = ',float('{:.3f}'.format(f(x))))
    return (a+b)/2
print('В итоге, ответом можно считать значение: ',main(a,b,f))
