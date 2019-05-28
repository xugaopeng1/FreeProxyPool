import time
import pymysql
from setting import *
from proxy_code.test_proxy import check_mysql_agent


def check_number():
    """
    统计表中是否有数据。
    :return:
    """
    con = pymysql.connect(host=host, user=user, passwd=passwd, charset="utf8")
    cur = con.cursor()
    sql_ = """
        SELECT
            COUNT(*)
        FROM
            db_proxy.proxy
    """
    try:
        cur.execute(sql_)
    except BaseException as e:
        print(e)
    else:
        row = cur.fetchone()
        all_number = row[0]
        return all_number


def select_all_sql():
    """
    取到所有已经存在数据库中的 代理IP。
    :return:
    """
    con = pymysql.connect(host=host, user=user, passwd=passwd, charset="utf8")
    cur = con.cursor()
    sql_0 = """
        UPDATE db_proxy.proxy
        SET flag = 0
    """
    cur.execute(sql_0)
    con.commit()

    sql_1 = """
        SELECT
            *
        FROM
            db_proxy.proxy
        ORDER BY
            score DESC
    """
    try:
        cur.execute(sql_1)
    except BaseException as e:
        cur.rollback()
        print(e)
    row = cur.fetchall()
    return row


def check_all_proxy():
    """
    在每次开始之前 进行检测数据库中的每一条数据是否还能用，如果不能用且分数
    小于 3 删除掉
    小于 3 但大于 4，把其状态 flag 为 1
    如果可以用 分数使其变为 5 且其状态 flag 为 0
    :return:
    """
    con = pymysql.connect(host=host, user=user, passwd=passwd, charset="utf8")
    cur = con.cursor()
    """
    首先检测所有的数据库中的代理是否还能用
    :return:
    """
    all_info = select_all_sql()
    for each_info in all_info:
        check_id = each_info[0]
        check_ip = each_info[1]
        score = each_info[4]
        if int(score) <= 3:  # 如果分数小于 3 分的直接选择删除此条记录。
            sql_0 = (
                """
                DELETE
                FROM
                    db_proxy.proxy
                WHERE
                    id = %s
            """
                % check_id
            )
            try:
                cur.execute(sql_0)
            except BaseException as e:
                print(e)

        check_type = each_info[2]
        check_full_ip = {"%s" % check_type.lower(): "%s:%s" % (check_type, check_ip)}
        ret_ = check_mysql_agent(check_full_ip)
        if ret_ == False:
            sql_1 = """
                UPDATE db_proxy.proxy
                SET score = %s,
                 flag=1
                WHERE
                    id = %s
            """ % (
                str(int(score) - 1),
                check_id,
            )
            try:
                cur.execute(sql_1)
                con.commit()
            except BaseException as e:
                print(e)
        else:
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            sql_2 = """
                UPDATE db_proxy.proxy
                SET score = 5,
                 flag=0,
                 date_time ="%s"
                WHERE
                    id = "%s"
            """ % (
                time_,
                check_id,
            )
            try:
                cur.execute(sql_2)
            except BaseException as e:
                print(e)


def success_proxy():
    """
    统计成功的代理。
    :return:
    """
    con = pymysql.connect(host=host, user=user, passwd=passwd, charset="utf8")
    cur = con.cursor()
    sql_ = """
        SELECT
            COUNT(*)
        FROM
            db_proxy.proxy
        WHERE
            score = 5
        AND flag = 0
        LIMIT 1
    """
    try:
        cur.execute(sql_)
    except BaseException as e:
        print(e)
    else:
        row = cur.fetchone()
        return row[0]


def count_sql():
    """
    统计余下 可以用的条数。
    :return:
    """
    con = pymysql.connect(host=host, user=user, passwd=passwd, charset="utf8")
    cur = con.cursor()
    sql_ = """
        SELECT
            COUNT(*)
        FROM
            db_proxy.proxy
        WHERE
            flag = 0
    """
    cur.execute(sql_)
    row = cur.fetchone()
    return row


def task():
    """
    执行函数
    :return:
    """
    all_number = check_number()
    if all_number:
        check_all_proxy()
        all_number = success_proxy()
    print('此时可用的代理为 %s number' % str(all_number))
    return all_number


if __name__ == '__main__':
    task()
