import time
import random
import requests
from setting import test_url, user_agent_list
from db_method.insert_db import insert_db_method


def check_agent(full_agent, each_ip, each_port, each_type):
    """
    检查爬起的 代理ip是否可用
    :param full_agent: 代理ip
    :return:
    """
    user_agent = random.choice(user_agent_list)
    headers = {"User-Agent": user_agent}
    try:
        test_response = requests.get(url=test_url, headers=headers, proxies=full_agent, timeout=5)
    except BaseException as e:
        print(e)
    else:
        if test_response.status_code == 200:
            time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            r_time = test_response.elapsed.microseconds / 1000 / 60  # 查看响应的速度，以分钟为单位
            print("Successfully this %s agent is available" % full_agent)
            ip_info = each_ip + ":" + each_port
            proxy_info = (ip_info, each_type.lower(), r_time, 5, 0, time_)
            insert_db_method(proxy_info, "db_proxy", "proxy")  # 进行插入到数据库中


def check_mysql_agent(proxy_ip):
    """
    检查 数据库中所有的代理是否还能用
    :return:
    """
    user_agent = random.choice(user_agent_list)
    headers = {"User-Agent": user_agent}
    try:
        test_response = requests.get(url=test_url, headers=headers, proxies=proxy_ip, timeout=3)
    except BaseException as e:
        print(e)
        return False
    else:
        if test_response.status_code == 200:
            return True
