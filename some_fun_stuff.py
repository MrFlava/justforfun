# 1. Palindrome in list checking

#
# def palindromes_check(words: list) -> list:
#     return list(filter(lambda s: s[::-1] == s, words))
#

# 2. Decorator benchmark

# import time
# import functools
#
#
# class myShinyDeco:
#     def __init__(self, fmt="completed {:s} in {:.3f} seconds"):
#         self.fmt = fmt
#
#     def __call__(self, fn):
#         @functools.wraps(fn)
#         def wrapper(*args, **kwargs):
#             t1 = time.time()
#             res = fn(*args, **kwargs)
#             t2 = time.time()
#             print(self.fmt.format(fn.__name__, t2 - t1))
#             return res
#
#         return wrapper
#
#
# def calling_counter(f):
#     def wrapper(*args, **kwargs):
#         wrapper.calls += 1
#         print(f"Decorator was called : {wrapper.calls}  times")
#         return f(*args, **kwargs)
#
#     wrapper.calls = 0
#     return wrapper
#
#
# @myShinyDeco()
# @calling_counter
# def func():
#     return "coolest function across USA "


# 3. Delete duplicates with two ways
""" First way """

# def delete_duplicates_way_two(strings_list: list) -> list:
#     return list(set(strings_list))


""" Second way """

#
# def delete_duplicates_way_one(strings_list: list) -> list:
#     output_list = []
#     for i in strings_list:
#         if i not in output_list:
#             output_list.append(i)
#     return output_list


# 4. Operations with string numbers


# def str_sum(num1: str, num2: str, oper: str) -> float:
#     if oper not in ["+", "-", "/", "*"]:
#         raise NotImplementedError
#
#     operators = {
#         "+": (lambda: int(num1) + int(num2))(),
#         "-": (lambda: int(num1) - int(num2))(),
#         "*": (lambda: int(num1) * int(num2))(),
#         "/": (lambda: int(num1) / int(num2))(),
#     }
#
#     return operators[oper]


# 5. Iterator with Class


# class Count:
#     def __init__(self, start):
#         self.num = start
#         self.limit = 1000
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         num = self.num
#         self.num += 1
#         if not self.num >= self.limit:
#             return num
#         else:
#             raise ValueError


# 6. Python generator
# def simple_generator(val: str):
#     if isinstance(val, str):
#         while len(val) > 0:
#             val += "a"
#             yield val
#     raise TypeError


# 7. Backpack task ( dynamic programming )

# from argparse import ArgumentParser
#
# parser = ArgumentParser(description="Task 2 Exercise 1")
# parser.add_argument("-W", nargs=1, type=int, help="capacity")
# parser.add_argument("-w", nargs="*", type=int, help="weights")
# parser.add_argument("-n", nargs=1, type=int, help="bars_number")
#
#
# def max_gold(c, w, n):
#     K = [[0 for x in range(c + 1)] for x in range(n + 1)]
#
#     for i in range(n + 1):
#         for j in range(c + 1):
#             if i == 0 or j == 0:
#                 K[i][j] = 0
#             elif w[i - 1] <= j:
#                 K[i][j] = max(w[i - 1] + K[i - 1][j - w[i - 1]], K[i - 1][j])
#             else:
#                 K[i][j] = K[i - 1][j]
#
#     return K[n][c]
#
#
# def bounded_knapsack(args):
#
#     args_dict = vars(args)
#     capacity = args_dict["W"][0]
#     weights = args_dict["w"]
#     bars_number = args_dict["n"][0]
#
#     for w in weights:
#         if w < 0:
#             raise ValueError
#
#     if len(weights) != bars_number or capacity < 0:
#         raise ValueError
#     else:
#         return max_gold(capacity, weights, bars_number)

# 8. Working with SQLite

import sqlite3

"""Basic example"""

# def sqlite3_db_work(database_name):
#     con = sqlite3.connect(database_name)
#     try:
#         cur = con.cursor()
#         # Create table
#         cur.execute(
#             """CREATE TABLE stocks
#                        (date text, trans text, symbol text, qty real, price real)"""
#         )
#         # Insert a row of data
#         cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
#         # Save (commit) the changes
#         con.commit()
#         return f"{[row for row in cur.execute('SELECT * FROM stocks ORDER BY price')]}"
#     except sqlite3.Error as error:
#         return f"Error while connecting to sqlite, {error}"

"""Some requests"""

# 9. Working with PostgreSQL

import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""Basic example with psycopg2"""


# def psycopg2_basic_db_usage():
#     conn = psycopg2.connect(dbname='postgres', user='postgres',
#                             password='112323', host='localhost')
#     cursor = conn.cursor()
#
#     # Create table
#     # cursor.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, " +
#     #                "login VARCHAR(64), password VARCHAR(64))")
#     # conn.commit()
#     # Insert a row of data
#     # cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s)",
#     #                ("afiskon", "123"))
#     # cursor.execute("INSERT INTO users (login, password) VALUES (%s, %s)",
#     #                ("eax", "456"))
#
#     conn.commit()
#
#     cursor.execute("SELECT id, login, password FROM users")
#     print(cursor.fetchall())
#
#     return 'Connection were closed'


"""Basic example with sqlalchemy  ORM"""


# def sqlalchemy_orm_usage():
#     engine = create_engine('postgresql://postgres:112323@localhost:5432/postgres')
#     base = declarative_base()
#
#     class Film(base):
#         __tablename__ = 'films'
#
#         title = Column(String, primary_key=True)
#         director = Column(String)
#         year = Column(String)
#
#     Session = sessionmaker(engine)
#     session = Session()
#
#     base.metadata.create_all(engine)
#
#     # Create
#     doctor_strange = Film(title="CCC Strange", director="Scott Derrickson", year="2016")
#     session.add(doctor_strange)
#     session.commit()
#
#     # Update
#     doctor_strange.title = "Some2013Film"
#     session.commit()
#
#     # Read
#     films = session.query(Film)
#     for film in films:
#         print(film.title)
#
#     # Delete
#     session.delete(doctor_strange)
#     session.commit()


def main():
    pass
    # print(sqlalchemy_orm_usage())
    # print(psycopg2_basic_db_usage())
    # database_name = "example.db"

    # print(sqlite3_db_work(database_name))
    # args = parser.parse_args()
    #
    # print(bounded_knapsack(args))

    # new_generator = simple_generator("b")
    #
    # print(next(new_generator))
    # print(next(new_generator))
    # print(next(new_generator))
    # print(next(new_generator))
    # print(next(new_generator))
    #
    # c = Count(-100)
    # for i in c:
    #     print(i)

    # num1 = "555"
    # num2 = "888"
    # operator = "+"
    #
    # a = ["mega", "level", "pop", "funny", "wave", "cool", "super", "mom"]
    # s_list = ["bill", "there", "hey", "pay", "bill", "there", "sugar"]
    #
    # print(str_sum(num1, num2, operator))
    # print(delete_duplicates_way_one(s_list))
    # print(delete_duplicates_way_two(s_list))
    #
    # print(func())
    #
    # print(palindromes_check(a))


if __name__ == "__main__":
    main()
