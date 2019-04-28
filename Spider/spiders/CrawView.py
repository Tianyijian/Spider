# _*_ coding:utf8 _*_

from scrapy_redis.spiders import RedisSpider
from scrapy.loader import ItemLoader
from Spider.items import ViewItem


class ViewSpider(RedisSpider):
    name = 'view_spider'
    redis_key = 'today_hit_view:urls'


    custom_settings = {
        'ITEM_PIPELINES': {
            'Spider.pipelines.ViewPipeline': 300,
        },
    }

    def parse(self, response):
        itemld = ItemLoader(item=ViewItem(), response=response)
        itemld.add_value('url', response.url)
        itemld.add_xpath('title', '//div[@class="article-title text-center"]/h3/text()')
        itemld.add_xpath('paragraphs', '//div[@class="block-region-left"]/div[3]//p')
        itemld.add_xpath('file_name', '//div[@class="field--item"]//a/text()')
        itemld.add_xpath('file_urls', '//div[@class="field--item"]//a/@href')
        return itemld.load_item()
