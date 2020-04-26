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

class LmparserPipeline(object):
	def __init__(self):
		client = MongoClient('localhost',27017)
		self.mongo_base = client.leroymerlin
	def process_item(self, item, spider):
		collection = self.mongo_base[spider.name]
		item['local_link'] = []
		if item['photos']:
			folder = item['link'].split('/')[-2].split('-')[-1]
			if not (os.path.exists(folder)):
				os.mkdir(folder)
			for img in item['photos']:
				try:
					#wget.download(img)
					file = img.split('/')[-1]
					print (file)
					#shutil.move(file,folder)
					item['local_link'].append(folder+'/'+file)
				except Exception as e:
					print(e)
		collection.insert_one(item)
		return item


class LmPhotosPipeline(ImagesPipeline): # этот класс в setting закомментировал, так как не работает scrapy.Request(img)
	def get_media_requests(self, item, info):
		if item['photos']:
			for img in item['photos']:
				print(img)
				try:
					#wget.download(img) 
					yield scrapy.Request(img)
				except Exception as e:
					print(e)
	def file_path(self, request, response=None, info=None):
		pass

	def item_completed(self, results, item, info):
		if results[0]:
			item['photos'] = [itm[1] for itm in results if itm[0]]
			print(item['photos'])
		return item