"""

Лаборатонрая работа #10
Вариант 9

"""

import numpy as np

mas_x = np.array([1, 1.15, 1.3, 1.45,  1.6,  1.75, 1.9])
mas_y = np.array([1.0806, 1.0805, 0.9042, 0.5067, -0.1495, -1.0918,  -2.3342])
r = 1.4
h = (1.9-1.0)/6.0
q = (r-1.0)/h
mas_0 = [mas_y[1]-mas_y[0], mas_y[2]-mas_y[1],
         mas_y[3]-mas_y[2], mas_y[4]-mas_y[3],
         mas_y[5]-mas_y[4], mas_y[6]-mas_y[5]]

mas_1 = [mas_0[1] - mas_0[0], mas_0[2] - mas_0[1], mas_0[3] - mas_0[2], mas_0[4] - mas_0[3], mas_0[5] - mas_0[4]]

mas_2 = [mas_1[1] - mas_1[0], mas_0[2] - mas_0[1], mas_0[3] - mas_0[2], mas_0[4] - mas_0[3]]

mas_3 = [mas_2[1] - mas_2[0], mas_2[2] - mas_2[1], mas_2[3] - mas_2[2]]

first_function = 1/h*(mas_0[0]+((2*q-1)/2)*mas_1[0]+((3*pow(q, 2)-6*q+2)/6)*mas_2[0]+((2*pow(q, 3)-9*pow(q, 2)+11*q-3)/12)*mas_3[0])
second_function = 1/pow(h, 2)*(mas_1[0]+((q-1)/1)*mas_2[0]+((6*pow(q, 2)-18*q+11)/12)*mas_3[0])
print('first funciton = ', first_function)
print('second function = ', second_function)