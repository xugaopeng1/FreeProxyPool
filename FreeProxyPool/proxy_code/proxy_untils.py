from proxy_code.crawler import ProxySpider


def start_proxy():
    ProxySpider().work()


if __name__ == '__main__':
    start_proxy()
