# _*_ coding:utf8 _*_

from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request
from Spider.items import FileDownloadItem


class FileSpider(RedisSpider):
    name = 'file_spider'
    redis_key = 'today_hit_file:urls'
    redis_batch_size = 1

    custom_settings = {
        'ITEM_PIPELINES': {
            'Spider.pipelines.FilePipeline': 300,
        },
    }

    def parse(self, response):
        yield Request(response.url, callback=self.parse_link)

    def parse_link(self, response):
        item = FileDownloadItem()
        item['file_urls'] = [response.url]
        return item
