# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os 
import wget

class LmparserPipeline(object):
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.mongo_base = client.leroymerlin

	def process_item(self, item, spider):
		collection = self.mongo_base[spider.name]
		item['local_link'] = []
		folder = 'images/' + item['link'].split('/')[-2].split('-')[-1]
		print(item['name'],"------",folder)
		if item['photos']:
			item['local_link'] = self.loader(item['photos'],folder)
		collection.insert_one(item)
		return item

	def loader(self, photos, folder): #загружает фото и раскладывает по папкам  и прописывает локальные ссылки для БД
		llink = []
		if not (os.path.exists(folder)):
			os.mkdir(folder)
		for img in photos:
			try:
				file = img.split('/')[-1]
				wget.download(img,(folder+'/'+file))
				llink.append(folder+'/'+file)
			except Exception as e:
				print(e)
		return llink

