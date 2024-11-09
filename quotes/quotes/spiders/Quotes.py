import scrapy
from ..items import QuotesItem



class Quotes(scrapy.Spider):
	name = "quotes"
	start_urls = ["https://quotes.toscrape.com/"]

	def parse(self, response):
		quote_item = QuotesItem()

		parent_tags = response.xpath("//div[@class='quote']")

		for tag in parent_tags:
			quotes = tag.xpath("span[@class='text']/text()").extract()
			author = tag.xpath("span/small[@class='author']/text()").extract()
			tags = tag.xpath("div/meta/@content").extract()

			quote_item['title'] = quotes
			quote_item['author'] = author
			quote_item['tags'] = tags

			yield quote_item

