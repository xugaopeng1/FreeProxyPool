from db_method.creat_db import creat_db
from db_method.creat_table import create_table
from db_method.check_mysql import task


def db_start():
    creat_db()  # 创建数据库
    create_table()  # 创建表
    task()  # 检查表中的数据


if __name__ == '__main__':
    db_start()
