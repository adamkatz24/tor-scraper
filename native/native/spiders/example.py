# Save this file to your_project/spiders/example_spider.py

import scrapy
from scrapy_scrapingbee import ScrapingBeeRequest


class ExampleComSpider(scrapy.Spider):
    name = 'ExampleSpider'

    def start_requests(self):
        # URL to scrape
        url = 'https://example.com'

        # Create a ScrapingBeeRequest
        yield ScrapingBeeRequest(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        # Extract the title
        title = response.css('h1::text').get()

        # Extract the paragraph text
        paragraph = response.css('p::text').get()

        # Yield the extracted data
        yield {
            'title': title,
            'paragraph': paragraph,
            'url': response.url
        }
