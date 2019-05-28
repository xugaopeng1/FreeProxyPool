import multiprocessing
from db_method.db_untils import db_start
from tornado_api.api_code import work
from proxy_code.proxy_untils import start_proxy

if __name__ == '__main__':
    t0 = multiprocessing.Process(target=db_start)
    t0.start()
    t1 = multiprocessing.Process(target=work)
    t1.start()
    t2 = multiprocessing.Process(target=start_proxy)
    t2.start()
