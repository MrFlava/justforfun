import sys
from collections import Counter

CHARACTER_APPERING = 2
lines = []

for line in sys.stdin:
    if '' == line.rstrip():
        break
    lines.append(line)

output = [element for element in lines if CHARACTER_APPERING in Counter(element).values()]
result = ''.join(output)

sys.stdout.write(str(result))
