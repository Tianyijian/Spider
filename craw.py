"""
调用scrapy 命令行执行爬虫
crawl url -> crawl view -> crawl file
"""
from scrapy import cmdline


def craw_url():
    """
    提取网页链接
    :return:
    """
    print("Crawling url... write log in /log ")
    cmdline.execute("scrapy crawl url_spider".split())



def crawl_view():
    """
    爬取网页标题、正文，提取附件链接
    :return:
    """
    print("Crawling view... write log in /log ")
    cmdline.execute("scrapy crawl view_spider".split())



def crawl_file():
    """
    爬取附件
    :return:
    """
    print("Crawling file... write log in /log ")
    cmdline.execute("scrapy crawl file_spider".split())



if __name__ == '__main__':
    # craw_url()
    # crawl_view()
    crawl_file()
