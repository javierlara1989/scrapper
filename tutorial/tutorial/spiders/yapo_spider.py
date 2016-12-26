import scrapy


class YapoSpider(scrapy.Spider):
	name = "yapo"

	start_urls = [
            'http://www.yapo.cl/chile?ca=15_s',
		]

	def parse(self, response):
		for quote in response.css('tr.ad.listing_thumbs'):
			yield {
                    'subject' : quote.css('td.thumbs_subject a.title.text::text').extract_first(),
                    'price' : quote.css('td.thumbs_subject span.price.text::text').extract_first(),
                    'category' : quote.css('td.clean_links p.line_cc span.category.text::text').extract_first(),
			}

            next_page = response.css('span.nohistory a::attr(href)').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
