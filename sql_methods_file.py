# import sqlite3 as sl
#
# db = sl.connect('my-database.db')
#
#
# # sql = db.cursor()
#
#
# class UserDataBase:
#     def __init__(self):
#         self.db = db
#         self.login = ""
#         self.password = ""
#         self.session = 0
#         self.socket = None
#         self.messages = []
#         self.cursor = self.db.cursor()
#
#     def create_table(self):
#         self.cursor.execute(
#             """
#                 CREATE TABLE IF NOT EXISTS users(
#                     login TEXT,
#                     password TEXT,
#                     session INTEGER,
#                     socket INTEGER,
#                     messages TEXT
#                     );
#                 """
#         )
#         self.db.commit()
#
#     def db_update(self, user_login, field, value):
#         self.cursor.execute(f'UPDATE users SET {field} = {value} WHERE login = "{user_login}"')
#         self.db.commit()
#
#     def conclusion(self):
#         for i in self.cursor.execute('SELECT login, session FROM users'):
#             print(i)
#             return i[0]
#
#     def return_user_info(self, socket):
#         print(">>>>>>>>>>>>>>", socket)
#         u_name = self.cursor.execute(f"SELECT * FROM users WHERE socket = '{socket}'")
#         print('u_name=====', u_name)
#         return u_name
#
#     # sql.execute(
# #     """
# #         CREATE TABLE IF NOT EXISTS users(
# #             login TEXT,
# #             password TEXT,
# #             session INTEGER,
# #             socket INTEGER,
# #             messages TEXT
# #             );
# #         """
# # )
# # db.commit()
#
#
# # def reg():
# #     user_login = input("Login: ")
# #     user_password = input("Password: ")
# #
# #     sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
# #     if sql.fetchone() is None:
# #         sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_login, user_password, 0, 0, ""))
# #         db.commit()
# #     else:
# #         print(" Такое уже есть ")
# #
# #     for value in sql.execute("SELECT * FROM users"):
# #         print(value)
# #
# #     logining()
#
#
# # def db_update(user_login, field, value):
# #     # print('user_login, field, value', user_login, field, value)
# #     # sql.execute(f'UPDATE users SET {field} = {value} WHERE login = "{user_login}"')
# #     db.commit()
# #
# #
# # def conclusion():
# #     for i in sql.execute('SELECT login, session FROM users'):
# #         print(i)
# #         return i[0]
