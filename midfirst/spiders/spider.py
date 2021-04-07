import scrapy

from scrapy.loader import ItemLoader

from ..items import MidfirstItem
from itemloaders.processors import TakeFirst


class MidfirstSpider(scrapy.Spider):
	name = 'midfirst'
	start_urls = ['https://www.midfirst.com/inside-midfirst/press-releases']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="btn btn--primary next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="col-xs-12 col-lg-8 container"]/h2/text()').get()
		description = response.xpath('//div[@class="col-xs-12 col-lg-8 container"]//text()[normalize-space() and not(ancestor::h2 | ancestor::h4)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-xs-12 col-lg-8 container"]/h4/text()').get()

		item = ItemLoader(item=MidfirstItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
