"""

Лаборатонрая работа #6
Вариант 9

"""

import math
import numpy as np

Ur1 = [-5, -1.5, 2, 2]
Ur2 = [1, -4, 1, -5]
Ur3 = [-2, -3, 5, 3]
epsi = 0.0005
print("Имеем СЛАУ:")
print(' _')
print('(', Ur1[0], "x1", Ur1[1], "x2", "+", Ur1[2], "x3", "=", Ur1[3])
print('<', Ur2[0], "x1", "+", Ur2[1], "x2", Ur2[2], "x3", "=", Ur2[3])
print('(_', Ur3[0], "x1", Ur3[1], "x2", "+", Ur3[2], "x3", "=", Ur3[3])
iterations = 100
arrA = np.array([[-5.0, -1.5, 2.0],
                 [1.0, -4.0, 1.0],
                 [-2.0, -3.0, 5.0]])
arrB = np.array([2.0, -5.0, 3.0])
print('--------------------{Решение методом итерации}--------------------')

x2_0 = 0
x1_0 = 0
x3_0 = 0

x = arrB[0]
y = arrB[1]
z = arrB[2]

for l in range(iterations):

    x = (arrB[0] - arrA[0][1] * y - arrA[0][2] * z) / arrA[0][0]
    y = (arrB[1] - arrA[1][0] * x - arrA[1][2] * z) / arrA[1][1]
    z = (arrB[2] - arrA[2][0] * x - arrA[2][1] * y) / arrA[2][2]


    abs_1 = math.fabs(x1_0 - x)
    abs_2 = math.fabs(x2_0 - y)
    abs_3 = math.fabs(x3_0 - z)
    print('x1: {0}, x2: {1}, x3: {2}'.format(x, y, z))

    if max(abs_1, abs_2, abs_3) < epsi:
        break
print('--------------------{Решение методом Зейделя}--------------------')

x = np.zeros_like(arrB)
for l in range(iterations):
    print("Tekushee reshenie:", x)
    x_new = np.zeros_like(x)

    for i in range(arrA.shape[0]):
        sum1 = np.dot(arrA[i, :i], x[:i])
        sum2 = np.dot(arrA[i, i + 1:], x[i + 1:])
        x_new[i] = (arrB[i] - sum1 - sum2) / arrA[i, i]
    if np.allclose(x, x_new, atol=epsi, rtol=0.):
        break
    x = x_new
print("Reshenie:")
print(x)
