
import sys
import os

from scrapy.cmdline import execute


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    args = sys.argv

    try:
        spider_name = args[1].split("=")[-1]
    except Exception:
        spider_name = "qichacha"
        # raise Exception("you must give name of spider! eg: python3 start_spider.py --name=xxx")
    spider_arguments = args[2:]
    arguments = []
    if spider_arguments:
        arguments = "-a " + " -a ".join(spider_arguments)
        arguments = arguments.split()
    execute_cmd = ['scrapy', 'crawl', spider_name] + arguments
    print(execute_cmd)
    execute(execute_cmd)
