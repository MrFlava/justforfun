"""

Лабораторная работа #5
Вариант 9

"""
import math
f  = lambda x: math.pow(x,4) + 2*math.pow(x, 2) - math.exp(2*x -1)
df = lambda x: 4*math.pow(x,3) + 4*x - 2*math.exp(2*x-1)
if __name__ == '__main__':
    epsi = 0.0001
    intervals = [[-0.5, 0.0], [0.0, 0,5], [0.5, 1.0], [1.5, 2.5]]
    for interval in intervals:
        x1 = interval[0]
        x2 = interval[1]
        while True:
            x1 = x1-f(x1)/df(x1)
            x2 = x1-((x2-x1)*f(x1)/(f(x2)-f(x1)))
            if abs(x2-x1) < epsi:
                break
        print('x = {0}'.format((x1+x2)/2),'f(x) = ', f((x1+x2)/2), 'df(x) = ',df((x1 + x2)/2))
