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
import data_handle

rds = redis.Redis(host='localhost', port=6379, db=0)


def extract_content(text):
    """
    移除HTML标签，删除空格
    :param text:
    :return:
    """
    content = remove_tags(text.replace('<br>', '\n'))
    return ''.join(content.split())


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
    result = []  # 存储网页爬取的结果
    view_num = 0  # 记录写入json的网页数目
    file_num = 0  # 记录附件的数目
    file_url = []  # 记录文件的url
    url_set, file_name_set = data_handle.json_statistic()  # 获得当前已有的url,文件名字集合

    def process_item(self, item, spider):
        url = item['url'][0]
        if url in self.url_set:  # url已存在，直接返回
            return
        self.url_set.add(url)
        if 'title' in item and 'paragraphs' in item:
            title = item['title'][0]
            paragraphs = '\n'.join(item['paragraphs'])
            # 网页正文的处理
            content = extract_content(paragraphs)
            # logging.info(content)

            temp_dict = {}
            temp_dict['url'] = url
            temp_dict['title'] = title
            temp_dict['paragraphs'] = content
            temp_dict['file_name'] = []
            # 判断是否有附件
            if 'file_urls' in item and 'file_name' in item:
                # 判断附件的名字是否在已有的附件名字集合中
                if len([file for file in item['file_name'] if file in self.file_name_set]):
                    # 只要有相同名字的附件，直接返回
                    return
                temp_dict['file_name'] = item['file_name']
                self.file_num += len(item['file_name'])
                self.file_name_set = self.file_name_set or set(item['file_name'])
                # 将文件 url 加入redis 队列
                for file_url in item['file_urls']:
                    rds.lpush('today_hit_file:urls', file_url)
                # 存储 file_urls
                file_dict = {}
                file_dict[url] = item['file_urls']
                self.file_url.append(file_dict)
            self.result.append(temp_dict)

            if len(self.result) >= 10:  # 一定数量时写入文件，批量存储，降低读写次数
                # logging.info(result)
                # 写入网页数据
                with open('data/data.json', 'a', encoding='utf-8') as f:
                    for sample in self.result:
                        f.write(json.dumps(sample, ensure_ascii=False) + '\n')
                self.result.clear()
                self.view_num += 10
                logging.info("------- write json (view_num: {} file_num: {})-------".format(self.view_num,
                                                                                            self.file_num))
                # 记录文件的 url
                with open("data/file_url.json", 'a', encoding='utf-8') as f:
                    for line in self.file_url:
                        f.write(json.dumps(line, ensure_ascii=False) + '\n')
                self.file_url.clear()
                # spider.crawler.engine.close_spider(spider, 'Get 1000')
                # raise CloseSpider('1000')
        return item


class FilePipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        '''
        从 url 中获取文件名
        :param request:
        :param response:
        :param info:
        :return:
        '''
        return '/%s' % parse.unquote(request.url).split('/')[-1]
