# _*_ coding:utf8 _*_


from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from Spider.items import UrlItem


class UrlSpider(CrawlSpider):
    name = 'url_spider'  # 用于区分不同的 spider，值唯一
    start_urls = ['http://today.hit.edu.cn/category/11']  # 启动时进行爬取的url列表
    allowed_domains = ['today.hit.edu.cn']
    allowed_urls = []   # 允许的url列表为空，默认都爬取

    rules = (
        Rule(LinkExtractor(allow=allowed_urls, restrict_xpaths='//li[@class="pager__item pager__item--next"]/a[1]'), callback='get_view_urls', follow=True),
    )

    custom_settings = {
        "ITEM_PIPELINES": {
            'Spider.pipelines.UrlPipeline': 300
        },
    }

    def get_view_urls(self, response):
        itemld = ItemLoader(item=UrlItem(), response=response)
        itemld.add_xpath('view_urls', '//div[@class="view-content"]//li/span//a/@href')
        return itemld.load_item()
