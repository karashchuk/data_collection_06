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
import shutil

class LeroyparserPipeline(object):
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.mongo_base = client.leroymerlin

	def process_item(self, item, spider):
		collection = self.mongo_base[spider.name]
		print(item['name'],"-------",item['photos'][0]['path'].split('/')[0]) # вывод скачанных товаров с указанием папки где хрянятся к ней фото
		collection.insert_one(item)
		return item



class LeroyPhotosPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		if item['photos']:
			for img in item['photos']:
				try:
					yield scrapy.Request(img)
				except Exception as e:
					print(e)

	def item_completed(self, results, item, info):
		if results[0]:
			item['photos'] = [itm[1] for itm in results if itm[0]]
			folder = item['link'].split('/')[-2].split('-')[0]+'_'+item['link'].split('/')[-2].split('-')[-1]
			item['photos'] = self.loader(item['photos'],folder)
		return item

	def loader(self, photos, folder): #раскладывает по папкам  и прописывает локальные ссылки для БД
		for img in photos:
			try:
				file = img['url'].split('/')[-1]
				src = img['path']
				if not (os.path.exists('images/'+folder)):
					os.mkdir('images/'+folder)
				shutil.move('images/'+src,'images/'+folder+'/'+file)
				img['path']=(folder+'/'+file)
			except Exception as e:
				print(e)
		return photos

