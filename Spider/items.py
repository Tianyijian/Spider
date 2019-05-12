# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    """
    主程序提取出页面链接
    """
    view_urls = scrapy.Field()


class ViewItem(scrapy.Item):
    """
    从每个页面中提取出标题、正文、附件
    """
    url = scrapy.Field()  # 网页链接
    title = scrapy.Field()  # 标题
    paragraphs = scrapy.Field()  # 正文
    file_name = scrapy.Field()  # 附件名称
    file_urls = scrapy.Field()  # 附件url


class FileDownloadItem(scrapy.Item):
    """
    下载附件
    """
    file_urls = scrapy.Field()
    files = scrapy.Field()
