"""

Лаборатонрая работа #8
Вариант 9

"""

import numpy as np
import matplotlib.pyplot as plt

mas_x = [1, 1.15, 1.3, 1.45,  1.6,  1.75, 1.9]
mas_y = [1.0806, 1.0805, 0.9042, 0.5067, -0.1495, -1.0918,  -2.3342]
r = 1.18

def coef(mas_x, mas_y):
    n = len(mas_x)
    a = []
    for i in range(n):
        a.append(mas_y[i])
    for j in range(1,n):
        for i in range(n-1,j-1,-1):
            a[i] = float(a[i]-a[i-1])/float(mas_x[i]-mas_x[i-j])
    return  np.array(a)
print(coef(mas_x, mas_y))
def Eval(a,mas_x, r):
    n = len(a) - 1
    temp = a[n]
    for i in range(n-1, -1, -1):
        temp = temp * (r - mas_x[i]) + a[i]
    return temp
print(Eval(coef(mas_x,mas_y),mas_x, r))
x_new = np.linspace(np.min(mas_x), np.max(mas_x), 100)
y_new = [Eval(coef(mas_x,mas_y), mas_x, i) for i in x_new]
plt.plot(mas_x, mas_y, 'o', x_new, y_new)
plt.show()