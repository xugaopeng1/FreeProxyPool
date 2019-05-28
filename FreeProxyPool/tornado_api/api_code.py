import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado_api.api_db_method import *
from tornado.web import RequestHandler
from tornado.options import define, options

# 进行 tornado 渲染效果
define("port", 5000, type=int, help="this is server port")


class ItemHandler(RequestHandler):
    def get(self):
        info = select_sql()  # 随机取出来一个 响应速度比较快的，而且得分速度为 5 的。
        if info:
            full_agent = self.t_parser(info)
            self.write(full_agent)
        else:
            info = select_other()
            if info:
                full_agent = self.t_parser(info)
                self.write(full_agent)
            else:
                self.write('代理池已经枯竭.....sorry')

    def t_parser(self, info):
        """
        自定义解析信息
        :return:
        """
        info_id = info[0]
        info_ip = info[1]
        info_type = info[2]
        full_agent = {'%s' % info_type: '%s:%s' % (info_type, info_ip)}
        update_sql(info_id)  # 把数据库的状态更新成 1，不在选中这条记录。
        return full_agent


def work():
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/", ItemHandler),
    ])
    # 创建服务器
    server = tornado.httpserver.HTTPServer(app, xheaders=True)
    # 监听端口下的 app
    server.listen(options.port)
    # 启动服务
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    work()
