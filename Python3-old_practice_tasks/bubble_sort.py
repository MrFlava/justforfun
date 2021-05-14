word_1 = 'gfg'
word_2 = 'fgfdgdf'
word_3 = 'gdfgffgdgfd'

a = [len(word_3.replace('', ' ')), len(word_1.replace('', ' ')), len(word_2.replace('', ' '))]


print('Изначальный массив: ', *a)
for j in range(len(a)):

    i = 0
    while i < len(a)-1:

        if a[i] > a[i+1]:

            a[i], a[i+1] = a[i+1], a[i]

        i = i+1
print('Отсортированный массив: ', *a)
