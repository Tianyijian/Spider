# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from w3lib.html import remove_tags
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import CloseSpider
import redis
import json
import logging
from urllib import parse

rds = redis.Redis(host='localhost', port=6379, db=0)


def extract_content(text):
    """
    移除HTML标签，删除空格
    :param text:
    :return:
    """
    content = remove_tags(text.replace('<br>', '\n'))
    return ''.join(content.split())


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class UrlPipeline(object):
    def process_item(self, item, spider):
        if item['view_urls']:
            # 列表不为空
            url = "http://today.hit.edu.cn"
            for it in item['view_urls']:
                # 将要爬取的url加入redis队列
                rds.lpush('today_hit_view:urls', url + it)
        return item


class ViewPipeline(object):
    result = []     # 存储网页爬取的结果
    view_num = 0    # 记录写入json的网页数目
    file_num = 0    # 记录附件的数目
    def process_item(self, item, spider):
        url = item['url'][0]
        if 'title' in item and 'paragraphs' in item:
            title = item['title'][0]
            paragraphs = '\n'.join(item['paragraphs'])
            content = extract_content(paragraphs)
            logging.info(content)

            temp_dict = {}
            temp_dict['url'] = url
            temp_dict['title'] = title
            temp_dict['paragraphs'] = content
            temp_dict['file_name'] = []
            # 判断是否有附件
            if 'file_urls' in item and 'file_name' in item:
                temp_dict['file_name'] = item['file_name']
                self.file_num += len(item['file_name'])
                # 将文件 url 加入redis 队列
                for url in item['file_urls']:
                    rds.lpush('today_hit_file:urls', url)
            self.result.append(temp_dict)

            if len(self.result) >= 10:  # 一定数量时写入文件
                # logging.info(result)
                with open('data.json', 'a', encoding='utf-8') as f:
                    for sample in self.result:
                        f.write(json.dumps(sample, ensure_ascii=False) + '\n')
                self.result.clear()
                self.view_num += 100
                logging.info("----------- write json (view_num: {} file_num: {})-----------".format(self.view_num, self.file_num))
                # spider.crawler.engine.close_spider(spider, 'Get 1000')
                # raise CloseSpider('1000')
        return item


class FilePipeline(FilesPipeline):
    # 'http://today.hit.edu.cn/sites/today1.prod1.dpweb1.hit.edu.cn/files/attachments/2019/04/25/%E9%99%84%E4%BB%B62%EF%BC%9A%E5%93%88%E5%B0%94%E6%BB%A8%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6XX%E5%B9%B4%E5%BA%A6%E6%94%B9%E5%96%84%E5%9F%BA%E6%9C%AC%E5%8A%9E%E5%AD%A6%E6%9D%A1%E4%BB%B6%E4%B8%93%E9%A1%B9%E9%A1%B9%E7%9B%AE%E4%BF%A1%E6%81%AF%E8%A1%A8_doc.doc'
    def file_path(self, request, response=None, info=None):
        '''
        从 url 中获取文件名
        :param request:
        :param response:
        :param info:
        :return:
        '''
        return '/%s' % parse.unquote(request.url).split('/')[-1]

