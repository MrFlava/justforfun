# 1. Palindrome in list checking

# def palindromes_check(words: list) -> list:
#     return list(filter(lambda s: s[::-1] == s, words))
# 2. Decorator benchmark

# import time
# import functools

# class myShinyDeco:
#     def __init__(self, fmt='completed {:s} in {:.3f} seconds'):
#             self.fmt = fmt

#     def __call__(self, fn):
#         @functools.wraps(fn)
#         def wrapper(*args, **kwargs):
#           t1 = time.time()
#           res = fn(*args, **kwargs)
#           t2 = time.time()
#           print(self.fmt.format(fn.__name__, t2-t1))
#           return res
#         return wrapper

# def calling_counter(f):
#     def wrapper(*args, **kwargs):
#         wrapper.calls += 1
#         print(f'Decorator was called : {wrapper.calls}  times')
#         return f(*args, **kwargs)
#     wrapper.calls = 0
#     return wrapper

# @myShinyDeco()
# @calling_counter
# def func():
#     return 'coolest function across USA '

# 3. Delete duplicates with two ways
""" First way """


# def delete_duplicates_way_two(strings_list: list) -> list:
#     return list(set(strings_list))


""" Second way """


# def delete_duplicates_way_one(strings_list: list) -> list:
#     output_list = []
#     for i in strings_list:
#         if i not in output_list:
#             output_list.append(i)
#     return output_list

# 4. Operations with string numbers

# def str_sum(num1: str, num2: str, oper: str) -> float:
#     if oper not in ['+', '-', '/', '*']:
#         raise NotImplementedError
#
#     operators = {
#         '+': (lambda: int(num1) + int(num2))(),
#         '-': (lambda: int(num1) - int(num2))(),
#         '*': (lambda: int(num1) * int(num2))(),
#         '/': (lambda: int(num1) / int(num2))(),
#     }
#
#     return operators[oper]

# def main():
# num1 = '555'
# num2 = '888'
# operator = '+'

# a = ['mega', 'level', 'pop', 'funny', 'wave', 'cool', 'super', 'mom']
# s_list = ['bill', 'there', 'hey', 'pay', 'bill', 'there', 'sugar']

# print(str_sum(num1, num2, operator))
# print(delete_duplicates_way_one(s_list))
# print(delete_duplicates_way_two(s_list))

# print(func())

# print(palindromes_check(a))

# if __name__ == "__main__":
#     main()


