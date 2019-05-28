# FreeProxyPool
"""
#### 声明主要是分三个模块，写的比较lower，你可以在此基础上添加使用。

#### 第一个模块：数据库模块。
    1：首先检查数据库合表是否存在，如果不存在创建，如果已经存在了，那么便开始检测表中的代理是否还可以用。


#### 第二个模块：代理的抓取，主要是分为 9 个免费代理网址的抓取，抓取的代码逻辑都在代码中，可自行添加和修改。

#### 第三个模块：API的编写，采用 tornado 框架进行编写，不会 tornado 框架的自行去看一下其官方文档。

#### 配置模块：setting,主要是连接数据库的一些账号和密码[采用 MySQL 数据库]。

#### 注意信息：使用的代理的时候可提前运行代理 run方法。

"""
#### 正文：

## FreeProxyPool

### 安装

#### 安装Python

至少Python3.5以上

#### 安装 MySQL

安装好之后将 MySQL 服务开启

#### 配置代理池

```
cd FreeProxyPool
```

进入 FreeProxyPool 目录，修改settings.py文件

user = 'root'  # 数据库的 账号。
passwd = ''  # 数据库的 密码。
#### 测试代理 IP 能否使用，建议抓取那个可以测试那个网站
test_url = 'http://www.xicidaili.com/nt/'

#### 安装依赖

```
pip3 install -r requirements.txt

这里依赖没有填写完，等你报错哪一项了你在装，尴尬，
```

#### 打开代理池和API

```
python3 run.py
```

#### 获取代理


利用requests获取方法如下

```python
import requests


def get_proxy():
    try:
        response = requests.get('http://localhost:5000/')
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


if __name__ == '__main__':
    proxy_ip = get_proxy()
    print(proxy_ip)

# 返回格式：{"http": "http:121.204.150.159:8118"}
# 注意如果返回的是：代理池已经枯竭.....sorry  说明抓取的所有免费代理都不能用了，如果你还不够用，自行去买吧。
小本生意仅供小型项目用，大型项目勿考虑。
```
