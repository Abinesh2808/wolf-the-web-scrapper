import scrapy
from ..items import QuotesItem
from scrapy.http import FormRequest
from scrapy.utils.response import open_in_browser


class Quotes(scrapy.Spider):
	name = "quotes"
	# start_urls = ["https://quotes.toscrape.com/"]

	# page_number = 2
	# start_urls = ["https://quotes.toscrape.com/page/1/"]

	start_urls = ["https://quotes.toscrape.com/login"]
	
	def parse(self, response):
		token = response.xpath("//input[@name='csrf_token']/@value").extract_first()

		return FormRequest.from_response(response, formdata={
			'csrf-token' : token,
			'username' : "admin@gmail.com",
			'password' : "admin@123"
			}, callback=self.scrap)


	def scrap(self, response):
		open_in_browser(response)
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


		# next_page = response.xpath("//li[@class='next']/a/@hre").get()
		# # next_page = response.css("li.next a::attr(href)").get()

		# if next_page is not None:
		# 	yield response.follow(next_page, callback=self.parse)


		# next_page = f"https://quotes.toscrape.com/page/{Quotes.page_number}/"

		# if Quotes.page_number < 11:
		# 	Quotes.page_number += 1
		# 	yield response.follow(next_page, callback=self.parse)