"""

Лабораторная работа #4
Вариант 9

"""
import math
f = lambda x: math.log(x) - (1/(5*x + 2))
df = lambda x: 5/math.pow((5*x + 2),2) + 1/x
epsi = 0.0001
a = float(input('Левая граница равна: '))
b = float(input('Правая граница равна: '))
def Solution(a, b, f, df,epsi):
    try:
        x_mid=(a+b)/2
        xn=f(x_mid)
        xn1=xn-f(xn)/df(xn)
        while abs(xn1-xn)>epsi:
            xn=xn1
            xn1=xn-f(xn)/df(xn)
            print('xn = ',xn,'xn1 = ',xn1,' f(xn) = ',f(xn),' f`(xn) = ',df(xn))
        return xn1
    except ValueError:
        print ("Ошибка, введены неправильные значения!")
print('Ответ: ',Solution(a , b ,f ,df, epsi))
