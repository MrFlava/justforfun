numbers = []

while True:
    try:
        number = input("enter a number  or Enter to finish: ")
        if not number:
            break
        numbers.append(int(number))
    except ValueError as err:
        print(err)
sum = sum(numbers)
count = len(numbers)
lowest = min(numbers)
highest = max(numbers)
mean = sum/count
print("numbers: ", numbers)
print("count: ", count, "sum: ", sum, "lowest: ", lowest, "highest: ", highest, "mean: ", mean)