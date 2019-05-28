"""
主要是一些免费网站代理的获取，使用者可自行对代理网站进行添加，添加方式如下代码，
当然如果有代码已经不能用了，请自行删除或者是联系作者进行修改。
"""
import multiprocessing
from scrapy import Selector
from proxy_code.get_text import get_response
from proxy_code.test_proxy import check_agent
from db_method.check_mysql import count_sql


class ProxySpider:
    # 抓取第 一 个网站
    def kuai_dai_li_spider(self):
        """
        抓取的代理网站：https://www.kuaidaili.com/free/
        :return:
        """
        url = "https://www.kuaidaili.com/free/inha/1/"
        try:
            response_info = get_response(url)
        except ConnectionError as e:
            print(e)
        else:
            if response_info:
                selector_response = Selector(text=response_info)
                self.parser_kuai_dai_li(selector_response)  # 进行第一页的抓取
                # all_page = selector_response.xpath('//div[@id="listnav"]/ul/li//text()').extract()[-2]
                for each_page in range(2, 30):
                    print("进行 %s 页的抓取" % each_page)
                    page_url = "https://www.kuaidaili.com/free/inha/%s/" % each_page
                    page_response = get_response(page_url)
                    if page_response:
                        selector_response = Selector(text=page_response)
                        self.parser_kuai_dai_li(selector_response)  # 进行第 n 页的抓取
            else:
                pass

    def parser_kuai_dai_li(self, response):
        """
        对获取的内容进行解析。
        :param response:获取到每页的内容。
        :return:
        """
        all_info = response.xpath("//tr")
        for each_info in all_info[1:]:
            each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
            each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
            each_type = each_info.xpath("td[4]/text()").extract_first()  # 代理的协议的类型：http or https
            full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
            check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 抓取第二个网站
    def crawl_66ip_spider(self):
        """
        抓取的网站是：http://www.66ip.cn/index.html
        :return:
        """
        url = "http://www.66ip.cn/index.html"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            self.parser_66ip(selector_response)  # 进行第一次的解析
            # all_page = selector_response.xpath('//div[@id="PageList"]/a/text()').extract()[-2]
            for each_page in range(2, 30):
                print("进行 %s 页的抓取" % each_page)
                page_url = "http://www.66ip.cn/{page}.html".format(page=str(each_page))
                page_response = get_response(page_url)
                if page_response:
                    selector_response = Selector(text=page_response)
                    self.parser_66ip(selector_response)  # 进行第 n 页的抓取
        else:
            pass

    def parser_66ip(self, response):
        """
        对获取的内容进行解析
        :param response:获取到的内容
        :return:
        """
        all_info = response.xpath("//tr")
        for each_info in all_info[2:]:
            each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
            each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
            full_agent = {"http": "http://%s:%s" % (each_ip, each_port)}
            each_type = "http"
            check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开始第三个代理厂家的抓取
    def fei_yi_spider(self):
        """
        抓取飞蚁代理的网站：http://www.feiyiproxy.com/?page_id=1457
        :return:
        """
        url = "http://www.feiyiproxy.com/?page_id=1457"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            all_info = selector_response.xpath("//tr")
            for each_info in all_info[1:26]:
                each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
                each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
                each_type = each_info.xpath("td[4]/text()").extract_first()  # 代理的协议的类型：http or https
                full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
                check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开始第四个代理厂家的抓取
    def iphai_spider(self):
        """
        开始第四个代理厂家的抓取：http://www.iphai.com/free/ng
        :return:
        """
        url = "http://www.iphai.com/free/ng"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            all_info = selector_response.xpath("//tr")
            for each_info in all_info[1:]:
                each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
                each_ip = each_ip.replace("\n", "").replace(" ", "") if each_ip else ""
                each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
                each_port = (each_port.replace("\n", "").replace(" ", "") if each_port else "")
                each_type = each_info.xpath("td[4]/text()").extract_first()  # 代理的协议的类型：http or https
                each_type = (
                    each_type.replace("\n", "").replace(" ", "")
                    if each_type.replace("\n", "").replace(" ", "")
                    else "http"
                )
                full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
                check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开始第五个代理商家的抓取
    def data5u_spider(self):
        """
        开始第五个代理商家的抓取：http://www.iphai.com/free/ng
        :return:
        """
        url = "http://www.data5u.com/"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            all_info = selector_response.xpath('//ul[@class="l2"]')
            for each_info in all_info:
                each_ip = each_info.xpath("span[1]/li/text()").extract_first()  # ip
                each_port = each_info.xpath("span[2]/li/text()").extract_first()  # 端口
                each_type = each_info.xpath("span[4]/li/text()").extract_first()  # 代理协议的类型：http or https
                full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
                check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开始第六个代理商家的抓取
    def ip3366_spider(self):
        """
        开始第六个代理商家的抓取：http://www.ip3366.net/free/?stype=1&page=1
        :return:
        """
        url = "http://www.ip3366.net/free/?stype=1&page=1"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            self.parser_ip3366(selector_response)  # 进行第一次下载.....
            all_page = selector_response.xpath("//strong/text()").extract_first()
            all_page = all_page.replace("/", "")
            for each_page in range(2, int(all_page) + 1):
                print("进行 %s 页的抓取" % each_page)
                page_url = "http://www.ip3366.net/free/?stype=1&page=%s" % str(each_page)
                page_response = get_response(page_url)
                if page_response:
                    selector_response = Selector(text=response_info)
                    self.parser_ip3366(selector_response)  # 进行第 n 次下载.....

    def parser_ip3366(self, response):
        """
        对获取的内容进行解析
        :param response:
        :return:
        """
        all_info = response.xpath("//tr")
        for each_info in all_info[1:]:
            each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
            each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
            each_type = each_info.xpath("td[4]/text()").extract_first()  # 代理的协议的类型：http or https
            full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
            check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开启第 七 个代理商家的抓取
    def ip_89ip_spider(self):
        """
        抓取网站是：http://www.89ip.cn/index_1.html
        :return:
        """
        url = "http://www.89ip.cn/index_1.html"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            self.parser_89ip(selector_response)  # 进行第一次下载.....
            # next_page = selector_response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
            # if next_page:
            #     next_page_url = "http://www.89ip.cn/" + next_page
            #     self.ip_89ip_next_page_spider(next_page_url)
            for each_page in range(2, 30):
                print("进行 %s 页的抓取" % each_page)
                page_url = "http://www.89ip.cn/index_%s.html" % str(each_page)
                page_response = get_response(page_url)
                if page_response:
                    selector_response = Selector(text=response_info)
                    self.parser_89ip(selector_response)  # 进行第 n 次下载.....

    # def ip_89ip_next_page_spider(self, next_page_url):
    #     """
    #     下一页的抓取
    #     :param next_page_url: 下一页的路径
    #     :return:
    #     """
    #     response_info = get_response(next_page_url)
    #     if response_info:
    #         selector_response = Selector(text=response_info)
    #         self.parser_89ip(selector_response)  # 进行第 n 次下载.....
    #         next_page = selector_response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
    #         if next_page:
    #             next_page_url = "http://www.89ip.cn/" + next_page
    #             self.ip_89ip_next_page_spider(next_page_url)
    #         else:
    #             return

    def parser_89ip(self, response):
        """
        进行解析获得到的 html 得到 ip port。
        :param response: 每次响应的内容
        :return:
        """
        all_info = response.xpath("//tr")
        for each_info in all_info[1:]:
            each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
            each_ip = each_ip.strip() if each_ip else ""
            each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
            each_port = each_port.strip()
            full_agent = {"http": "http://%s:%s" % (each_ip, each_port)}
            each_type = "http"
            check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开启第 八 个代理商的抓取
    def qydaili_sipder(self):
        """
        抓取的网站是：http://www.qydaili.com/free/?action=china&page=1
        :return:
        """
        url = "http://www.qydaili.com/free/?action=china&page=1"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            self.parser_qydaili(selector_response)  # 进行第一次的下载
            # next_page = selector_response.xpath('//a[@aria-label="Next"]/@href').extract_first()
            # if next_page:
            #     next_page_url = "http://www.qydaili.com/free/" + next_page
            #     self.qydaili_next_page_spider(next_page_url)
            # else:
            #     return
            for each_page in range(2, 30):
                print("进行 %s 页的抓取" % each_page)
                page_url = "http://www.qydaili.com/free/?action=china&page=%s" % str(each_page)
                page_response = get_response(page_url)
                if page_response:
                    selector_response = Selector(text=response_info)
                    self.parser_qydaili(selector_response)  # 进行第 n 次下载.....

    #
    # def qydaili_next_page_spider(self, next_page_url):
    #     """
    #     下一页的抓取
    #     :param next_page_url: 下一页的路径
    #     :return:
    #     """
    #     response_info = get_response(next_page_url)
    #     if response_info:
    #         selector_response = Selector(text=response_info)
    #         self.parser_qydaili(selector_response)  # 进行第一次的下载
    #         next_page = selector_response.xpath('//a[@aria-label="Next"]/@href').extract_first()
    #         if next_page:
    #             next_page_url = "http://www.qydaili.com/free/" + next_page
    #             self.qydaili_next_page_spider(next_page_url)
    #         else:
    #             return

    def parser_qydaili(self, response):
        """
        解析每一页想要的信息。
        :param response:
        :return:
        """
        all_info = response.xpath("//tr")
        for each_info in all_info[1:]:
            each_ip = each_info.xpath("td[1]/text()").extract_first()  # IP
            each_port = each_info.xpath("td[2]/text()").extract_first()  # port：端口
            each_type = each_info.xpath("td[4]/text()").extract_first()  # 代理的协议的类型：http or https
            full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
            check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    # 开启第 九 个代理商家的抓取
    def xici_daili_spider(self):
        """
        爬取的网站：https://www.xicidaili.com/nn/
        :return:
        """
        url = "https://www.xicidaili.com/nn/"
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            self.parser_xici_daili(selector_response)
            next_page = selector_response.xpath('//a[@class="next_page"]/@href').extract_first()
            if next_page:
                self.xici_next_page_spider(next_page)

    def xici_next_page_spider(self, next_page_url):
        """
        解析下一页的网站
        :param next_page_url: 下一页的路径
        :return:
        """
        url = "http://www.xicidaili.com" + next_page_url
        response_info = get_response(url)
        if response_info:
            selector_response = Selector(text=response_info)
            self.parser_xici_daili(selector_response)  # 进行第 n 次下载。
            next_page = selector_response.xpath('//a[@class="next_page"]/@href').extract_first()
            if next_page:
                self.xici_next_page_spider(next_page)

    def parser_xici_daili(self, response):
        """
        解析每一页获取内容想要的信息。
        :param response:
        :return:
        """
        all_agent = response.xpath('//tr[@class="odd"]')
        for each_agent in all_agent:
            each_ip = each_agent.xpath("td[2]/text()").extract_first()
            each_port = each_agent.xpath("td[3]/text()").extract_first()
            each_type = each_agent.xpath("td[6]/text()").extract_first()
            full_agent = {"%s" % each_type.lower(): "%s://%s:%s" % (each_type.lower(), each_ip, each_port)}
            check_agent(full_agent, each_ip, each_port, each_type)  # 进行代理的测试........

    def work(self):
        # 多进程开启
        t1 = multiprocessing.Process(target=self.fei_yi_spider())
        t1.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t2 = multiprocessing.Process(target=self.iphai_spider())
        t2.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t3 = multiprocessing.Process(target=self.data5u_spider())
        t3.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t4 = multiprocessing.Process(target=self.ip3366_spider())
        t4.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t5 = multiprocessing.Process(target=self.kuai_dai_li_spider())
        t5.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t6 = multiprocessing.Process(target=self.crawl_66ip_spider())
        t6.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t7 = multiprocessing.Process(target=self.ip_89ip_spider())
        t7.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t8 = multiprocessing.Process(target=self.qydaili_sipder())
        t8.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))
        t9 = multiprocessing.Process(target=self.xici_daili_spider())
        t9.start()
        all_number = count_sql()
        print('此时可用的代理为 %s number' % str(all_number))


if __name__ == "__main__":
    proxy_spider = ProxySpider()
    proxy_spider.work()
