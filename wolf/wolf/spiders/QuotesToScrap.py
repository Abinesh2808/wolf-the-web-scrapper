import scrapy



class QuotesToScrap(scrapy.Spider):
	name = "quotes_to_scrap"
	start_urls = ["https://quotes.toscrape.com/"]


	def parse(self, response):
		# text = response.css("title").extract() #will get the tag
		# text = response.css("title::text").extract() #will get the text of the tag, o/p will in a list
		# text = response.css("title::text")[0].extract()
		# text = response.css("title::text").extract_first() #wont throw index out of range error
		# author = response.css('small.author::text')[-1].extract()


		text = response.xpath("//title/text()").extract()
		author = response.xpath("//small[@class='author']/text()").extract()	#text of the tag
		author = response.xpath("//small[@class='author']/@class").extract()   #attribute if the tag
		yield {"page_title": text}