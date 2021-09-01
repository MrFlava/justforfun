from collections import Counter

CHARACTER_APPERING = 2
lines = []

while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break
output = [element for element in lines if CHARACTER_APPERING in Counter(element).values()]

print(output)
