import pymysql
from setting import *
from DBUtils.PooledDB import PooledDB

pool = PooledDB(
    creator=pymysql,
    mincached=6,
    maxcached=12,
    host=host,
    user=user,
    passwd=passwd,
    port=3306,
    charset="utf8",
    setsession=["SET AUTOCOMMIT = 1"]
)


def select_sql():
    """
    每次随机取出一个 分数为 5 时间是最近的，的最好的代理 IP
    :return:
    """
    conn = pool.connection()
    cur = conn.cursor()
    sql_ = """
        SELECT
            id,
            ip_info,
            ip_type
        FROM
            db_proxy.proxy
        WHERE
            score = 5
        AND flag = 0
        ORDER BY
            date_time DESC
        LIMIT 1
    """
    try:
        cur.execute(sql_)
    except BaseException as e:
        print(e)
        conn.rollback()
    row = cur.fetchone()
    return row


def update_sql(id_):
    """
    每次获取到的 IP 把其状态更新成 1 这样下次就不会选中。
    :param id_:
    :return:
    """
    conn = pool.connection()
    cur = conn.cursor()
    sql_ = """
        UPDATE db_proxy.proxy
        SET flag = 1
        WHERE
            id = "%s"
    """ % id_
    try:
        cur.execute(sql_)
    except BaseException as e:
        print(e)
    conn.commit()
    conn.close()


def select_other():
    """
    选中其他 分数不是 5 的记录
    :return:
    """
    conn = pool.connection()
    cur = conn.cursor()
    sql_ = """
        SELECT
            id,
            ip_info,
            ip_type
        FROM
            db_proxy.proxy
        WHERE
            flag = 0
        ORDER BY
            score DESC
        LIMIT 1
    """
    cur.execute(sql_)
    row = cur.fetchone()
    return row
