print('______________' + 'Задание #1' + '______________')
import math
import numpy
T = 2
U = 1
R1 = 8
R2 = 15
L = 0.5
C = 0.005
dt = 0.01
epsi = 0.01
methods = ['Метод фундаментальных матриц', ' Метод прогноза и коррекции']
print('Даны условия:')
print('-----------------------------------------')
print('R1: {}'.format(R1) + ' ,R2: {}'.format(R2))
print('-----------------------------------------')
print('C: {}'.format(C) + ' ,L: {}'.format(L))
print('------------------------------------------')
print('U: {}'.format(U) + ' ,T: {}'.format(T))
print('------------------------------------------')
print('epsi: {}'.format(epsi) + ' ,dt: {}'.format(dt))
print('-----------------------------------------')
print('Список численных методов:')
for i in methods:
    print('{}.'.format(methods.index(i) + 1), i)
print('Какой из методов применить?')
choise = int(input())

if choise == 1:
    print('-----------' + methods[0] + '-----------')
    y1 = []
    y2 = []
    prev_y1 = U
    prev_y2 = 0
    y1.insert(0, prev_y1)
    y2.insert(0, prev_y2)

    def f1(y1, y2):
        y1_ur = -8.6956 * y1 + 130.4 * y2
        return y1_ur

    def f2(y1, y2):
        y2_ur = -1.305 * y1 - 10.434 * y2
        return y2_ur

    def runge_kutta(prev_y1, prev_y2, h):

        k11 = f1(prev_y1, prev_y2)
        k12 = f2(prev_y1, prev_y2)

        k21 = f1(prev_y1 + h * k11 / 2, prev_y2 + h * k12 / 2)
        k22 = f2(prev_y1 + h * k11 / 2, prev_y2 + h * k12 / 2)

        k31 = f1(prev_y1 + h * k21 / 2, prev_y2 + h * k22 / 2)
        k32 = f2(prev_y1 + h * k21 / 2, prev_y2 + h * k22 / 2)

        k41 = f1(prev_y1 + h * k31, prev_y2 + h * k32)
        k42 = f2(prev_y1 + h * k31, prev_y2 + h * k32)

        next_y1 = prev_y1 + (h / 6) * (k11 + 2 * k21 + 2 * k31 + k41)
        next_y2 = prev_y2 + (h / 6) * (k12 + 2 * k22 + 2 * k32 + k42)

        return [next_y1, next_y2]

    print("step=%0.3f, y1=%0.3f, y2=%0.3f" % (0, y1[0], y2[0]))
    for i in range(4):
        [prev_y1, prev_y2] = runge_kutta(prev_y1, prev_y2, dt)
        print("step =%0.3f, y1 = %0.6f y2 = %0.6f" % (dt * (i + 1), prev_y1, prev_y2))
        y1.append(prev_y1)
        y2.append(prev_y2)
    u1 = y1
    u2 = y2
    for i in range(4):
        q11 = f1(y1[i], y2[i]) - f1(y1[i - 1], y2[i - 1])
        q12 = f1(y1[i], y2[i]) - 2 * f1(y1[i - 1], y2[i - 1]) + f1(y1[i - 2], y2[i - 2])
        q13 = f1(y1[i], y2[i]) - 3 * f1(y1[i - 1], y2[i - 1]) + f1(y1[i - 2], y2[i - 2]) - f1(y1[i - 3], y2[i - 3])
        q21 = f2(y1[i], y2[i]) - f2(y1[i - 1], y2[i - 1])
        q22 = f2(y1[i], y2[i]) - 2 * f2(y1[i - 1], y2[i - 1]) + f2(y1[i - 2], y2[i - 2])
        q23 = f2(y1[i], y2[i]) - 3 * f2(y1[i - 1], y2[i - 1]) + f2(y1[i - 2], y2[i - 2]) - f2(y1[i - 3], y2[i - 3])
        u1[i] = y1[i] + dt * f1(y1[i], y2[i]) + dt * 0.5 * q11 + 0.41666 * dt * q12 + 0.375 * dt * q13
        u2[i] = y2[i] + dt * f2(y1[i], y2[i]) + dt * 0.5 * q21 + 0.41666 * dt * q22 + 0.375 * dt * q23
    print(u1, u2)

elif choise == 2:
    print('-----------' + methods[1] + '-----------')
    y1 = []
    y2 = []
    prev_y1 = U
    prev_y2 = 0
    y1.insert(0, prev_y1)
    y2.insert(0, prev_y2)

    def f1(y1, y2):
        y1_ur = -8.6956 * y1 + 130.4 * y2
        return y1_ur

    def f2(y1, y2):
        y2_ur = -1.305 * y1 - 10.434 * y2
        return y2_ur

    def runge_kutta(prev_y1, prev_y2, h):

        k11 = f1(prev_y1, prev_y2)
        k12 = f2(prev_y1, prev_y2)

        k21 = f1(prev_y1 + h * k11 / 2, prev_y2 + h * k12 / 2)
        k22 = f2(prev_y1 + h * k11 / 2, prev_y2 + h * k12 / 2)

        k31 = f1(prev_y1 + h * k21 / 2, prev_y2 + h * k22 / 2)
        k32 = f2(prev_y1 + h * k21 / 2, prev_y2 + h * k22 / 2)

        k41 = f1(prev_y1 + h * k31, prev_y2 + h * k32)
        k42 = f2(prev_y1 + h * k31, prev_y2 + h * k32)

        next_y1 = prev_y1 + (h / 6) * (k11 + 2 * k21 + 2 * k31 + k41)
        next_y2 = prev_y2 + (h / 6) * (k12 + 2 * k22 + 2 * k32 + k42)

        return [next_y1, next_y2]

    print("step=%0.3f, y1=%0.3f, y2=%0.3f" % (0, y1[0], y2[0]))
    for i in range(4):
        [prev_y1, prev_y2] = runge_kutta(prev_y1, prev_y2, dt)
        print("step =%0.3f, y1 = %0.6f y2 = %0.6f" % (dt * (i + 1), prev_y1, prev_y2))
        y1.append(prev_y1)
        y2.append(prev_y2)
    for i in range(4):
        pred_y1 = y1[i-1] + dt / 24 * (
                    55 * f1(y1[i-1], y2[i-1]) - 59 * f1(y1[i-2], y2[-2]) + 37 * f1(y1[i-3], y2[i-3]) - 9 * f1(y1[i-4],
                                                                                                         y2[-4]))
        pred_y2 = y2[i-1] + dt / 24 * (
                    55 * f2(y1[i-1], y2[i-1]) - 59 * f2(y1[i-2], y2[i-2]) + 37 * f2(y1[i-3], y2[i-3]) - 9 * f2(y1[i-4],
                                                                                                         y2[-4]))
        corr_y1 = y1[i-1] + dt / 24 * (
                    9 * f1(pred_y1, pred_y2) + 19 * f1(y1[i-1], y2[-1]) - 5 * f1(y1[i-2], y2[i-2])
                    + f1(y1[i-3], y2[i-3]))
        corr_y2 = y2[i-1] + dt / 24 * (
            9 * f2(pred_y1, pred_y2) + 19 * f2(y1[i-1], y2[i-1]) - 5 * f2(y1[i-2], y2[i-2]) + f2(y1[i-3], y2[i-3]))
        print(pred_y1, pred_y1, corr_y1, corr_y2)

else:
    print('-----------' + 'Ошибка! Введите число от одного до двух!' + '-----------')
