"""

Лаборатонрая работа #7
Вариант 9

"""

import numpy as np
import matplotlib.pyplot as plt

mas_x = np.array([1.0000, 1.1000, 1.2320, 1.4796,  1.9383,  1.9577, 2.0380], dtype=float)
mas_y = np.array([0.1011, 0.1183, 0.1421, 0.1893, 0.2816, 0.2856,  0.3021], dtype=float)


def polinome(mas_x, mas_y, t):
 z = 0
 for j in range(len(mas_y)):
  p1 = 1;
  p2 = 1
  for i in range(len(mas_x)):
   if i == j:
    p1 = p1 * 1;
    p2 = p2 * 1
   else:
    p1 = p1 * (t - mas_x[i])
    p2 = p2 * (mas_x[j] - mas_x[i])
  z = z + mas_y[j] * p1 / p2
 return z

print(polinome(mas_x, mas_y, 1.3))
x_new = np.linspace(np.min(mas_x), np.max(mas_x), 100)
y_new = [polinome(mas_x, mas_y, i) for i in x_new]
plt.plot(mas_x, mas_y, 'o', x_new, y_new)
plt.grid(True)
plt.show()
