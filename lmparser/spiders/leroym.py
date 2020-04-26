# -*- coding: utf-8 -*-
import scrapy
from pprint import pprint
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader

class LeroymSpider(scrapy.Spider):
	name = 'leroym'
	allowed_domains = ['leroymerlin.ru']
	#start_urls = ['https://leroymerlin.ru/search/?q=%D1%88%D1%83%D1%80%D1%83%D0%BF%D0%BE%D0%B2%D0%B5%D1%80%D1%82']
	def __init__(self, search):
		self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

	def parse(self, response):
		goods_links = response.xpath("//div[@class='product-name']/a[@href]/@href").extract()
		for link in goods_links[0:5]:  # поставил ограничение только на 5 товаров
			yield response.follow(link, callback=self.parse_goods)

	def parse_goods(self,response):
		loader = ItemLoader(item=LmparserItem(), response=response)
		loader.add_xpath('name',"//h1[@class='header-2']/text()")
		loader.add_xpath('photos',"//picture[@slot='pictures']/img[@itemprop='image']/@src")
		loader.add_value('link',response.url)
		loader.add_xpath('price',"//span[@slot='price']/text()")
		loader.add_xpath('currency',"//span[@slot='currency']/text()")
		loader.add_xpath('params',"//div[@class='def-list__group']")
		loader.add_xpath('describ',"//section[@class='pdp-section pdp-section--product-description']//uc-pdp-section-vlimited[@class='section__vlimit']//p/text()")
		yield loader.load_item()

