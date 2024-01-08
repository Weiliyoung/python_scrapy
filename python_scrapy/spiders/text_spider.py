import scrapy
import csv

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # 提取名言数据
        quotes = response.css('div.quote')
        for quote in quotes:
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            tags = quote.css('div.tags a.tag::text').getall()

            # 保存数据到CSV文件
            with open('quotes.csv', 'a', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['text', 'author', 'tags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writerow({'text': text, 'author': author, 'tags': ', '.join(tags)})
                self.logger.info(f"Saved '{text}' by {author} to CSV")

        # 翻页处理
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
