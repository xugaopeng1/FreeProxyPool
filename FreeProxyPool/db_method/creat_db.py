"""
创建数据库
"""

import pymysql
from setting import *
from pymysql.err import *


def creat_db():
    """
    直接创建数据库
    :return:
    """
    # 建库和建表
    con = pymysql.connect(host=host, user=user, passwd=passwd, charset="utf8")
    cur = con.cursor()
    # 开始建库
    try:
        cur.execute("create database db_proxy character set utf8;")
    except ProgrammingError as e:
        print(e)


if __name__ == "__main__":
    creat_db()
