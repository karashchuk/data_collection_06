from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lmparser import settings
from lmparser.spiders.leroym import LeroymSpider
if __name__ == '__main__':
	crawler_settings = Settings()
	crawler_settings.setmodule(settings)
	process = CrawlerProcess(settings=crawler_settings)
	process.crawl(LeroymSpider, search = 'цветы')
	process.start()