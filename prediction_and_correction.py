import matplotlib.pyplot as plt
import math
y1 = []
import math
y2 = []
prev_y1 = 1
prev_y2 = 0
begin_t = 0 
step = 0.001
epsi = 0.001
check = False 
y1.insert(0,prev_y1)
y2.insert(0,prev_y2)
#Первое уравнение системы
def f1(y1, y2):
    return -0.08*y1 + 1.304*y2
#Второе уравнение системы 
def f2(y1, y2):
    return -1.31*y1 - 13.21*y2

#Использование метода Рунге-Кутта для начальной таблицы 
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
print("step=%0.3f, y1=%0.3f, y2=%0.3f"%(begin_t, y1[0], y2[0]))
for i in range(4):
    [prev_y1, prev_y2] = runge_kutta(prev_y1, prev_y2, step)
    print("step =%0.3f, y1 = %0.6f y2 = %0.6f" % (step * (i + 1), prev_y1, prev_y2))
    y1.append(prev_y1)
    y2.append(prev_y2)
plt.plot(step, 'o',y1, y2)
plt.show()

def prediction_and_correction(y1,y2, f1,f2, step,check,epsi):
  #Этап прогноза
    pred_y1 = y1[-1] + step/24*(55*f1(y1[-1],y2[-1])-59*f1(y1[-2],y2[-2])+ 37*f1(y1[-3],y2[-3])-9*f1(y1[-4],y2[-4]))
    pred_y2 = y2[-1] + step/24*(55*f2(y1[-1],y2[-1])-59*f2(y1[-2],y2[-2]) + 37*f2(y1[-3],y2[-3])-9*f2(y1[-4],y2[-4]))
  #Этап коррекции
    corr_y1 = y1[-1] + step/24*(9*f1(pred_y1,pred_y2) + 19*f1(y1[-1],y2[-1])- 5*f1(y1[-2],y2[-2]) + f1(y1[-3],y2[-3]))
    corr_y2 = y2[-1] + step/24*(9*f2(pred_y1,pred_y2)+ 19*f2(y1[-1],y2[-1])-5*f2(y1[-2],y2[-2]) + f2(y1[-3],y2[-3]))
    summa = math.sqrt(math.pow(corr_y1 - pred_y1,2)+math.pow(corr_y2 - pred_y2,2))
    while  summa < epsi:
      check = True
      y1.append(corr_y1)
      y1.append(corr_y2)
      print('yn1 на этапе прогноза:',pred_y1 ,'yn2 на этапе прогноза:',pred_y2,'yn1 на этапе коррекции:',corr_y1,'yn2 на этапе коррекции:',corr_y2,'Выполнение условия:',check)

print(prediction_and_correction(y1,y2, f1,f2, step,check,epsi))
