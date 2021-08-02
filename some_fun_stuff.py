# 1 Palindrome in list checking

# def palindormes_check(words: list) -> list:
#     return list(filter(lambda s: s[::-1] == s, words))
# 2 Decorator benchmark

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
#     return 'cooletst function accross USA '

# def main():
# a = ['mega', 'level', 'pop', 'funny', 'wave', 'cool', 'super', 'mom']
# print(func())
# print(palindormes_check(a))

# if __name__ == "__main__":
#     main()


