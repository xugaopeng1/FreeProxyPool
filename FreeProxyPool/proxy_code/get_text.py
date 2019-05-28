"""
此文件是抓取网页
"""
import random
import chardet
import requests
from setting import user_agent_list


def get_response(url, parameter={}):
    UserAgent = random.choice(user_agent_list)
    headers = dict({"User-Agent": UserAgent}, **parameter)
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response_content = response.content
            charset = chardet.detect(response_content).get("encoding")
            html = response_content.decode(charset, "ignore")
            print("抓取 %s 成功" % url)
            return html
    except ConnectionError as e:
        print("抓取 %s 失败" % url)
        return None


if __name__ == "__main__":
    url = "http://www.data5u.com"
    parameter = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Referer": "http://www.data5u.com/free/index.shtml",
        "Upgrade-Insecure-Requests": "1",
    }
    get_response(url, parameter)
