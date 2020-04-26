# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avitoparser.items import AvitoparserItem
from scrapy.loader import ItemLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    #start_urls = ['http://avito.ru/']
    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q=%D1%88%D1%83%D1%80%D1%83%D0%BF%D0%BE%D0%B2%D0%B5%D1%80%D1%82']

    def parse(self, response):
        ads_links = response.xpath("//div[@class='product-name']/a[@href]/@href").extract()
        print(ads_links)
        for link in ads_links:
            flink = 'https://leroymerlin.ru'+link
            yield response.follow(flink, callback=self.parse_ads)
    def parse_ads(self, response:HtmlResponse):
        name = response.xpath("//h1[@class='header-2']/text()").extract_first()
        photos = response.xpath("//picture[@slot='pictures']/img[@itemprop='image']/@src").extract()
        yield AvitoparserItem(name=name, photos=photos)
'''        name = response.xpath("//h1[@class='header-2']/text()").extract_first()
        photos = response.xpath("//picture[@slot='pictures']/img[@itemprop='image']/@src").extract()
        yield AvitoparserItem(name = name, photos = photos)'''
                # loader = ItemLoader(item=AvitoparserItem(), response=response)
        #         loader.add_xpath('name',"//h1/span/text()")
        #         loader.add_xpath('photos',"//div[contains(@class, 'gallery-img-frame')]/@data-url")
        #         yield loader.load_item()