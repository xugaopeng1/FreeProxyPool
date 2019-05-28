"""
把采集到的数据保存到 MySQL数据库中
"""
import pymysql
from setting import *

db_config = {
    "host": host,
    "port": 3306,
    "user": user,
    "passwd": passwd,
    "charset": "utf8",
    "db": "db_proxy",
}
conn_instance_dict = {}


def get_conn(db):
    db_config.update(db=db)
    conn = pymysql.connect(**db_config)
    return conn


def insert_db_method(data, db, table):
    if not data:
        return
    try:
        conn = get_conn(db)
    except BaseException as e:
        print(e)
    else:
        cur = conn.cursor()
        if isinstance(data, tuple):
            sql = (
                """
                INSERT INTO db_proxy.proxy (
                    ip_info,
                    ip_type,
                    res_time,
                    score,
                    flag,
                    date_time
                )
                VALUES
                    ("%s","%s","%s","%s","%s","%s")
            """
                % data
            )
            try:
                cur.execute(sql)
            except Exception as e:
                print(e)
                conn.rollback()
        else:
            sql = (
                """
                INSERT INTO db_proxy.proxy (
                    ip_info,
                    ip_type,
                    res_time,
                    score,
                    flag,
                    date_time
                )
                VALUES
                    ("%s","%s","%s","%s","%s","%s")
            """
                % data[0]
            )
            try:
                cur.execute(sql)
            except Exception as e:
                print(e)
                conn.rollback()
        cur.close()
        conn.commit()
