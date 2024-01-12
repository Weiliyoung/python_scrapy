# import scrapy
# from python_scrapy.spiders.items import UniversityItem
#
# class GaokaoSpider(scrapy.Spider):
#     name = 'universities'
#     allowed_domains = ['www.gaokao.cn']
#     start_urls = ['https://www.gaokao.cn/school/search']
#
#     def parse(self, response):
#         # 点击广东
#         yield scrapy.Request(url='https://www.gaokao.cn/school/search?&filter_province=广东', callback=self.parse_province)
#
#     def parse_province(self, response):
#         # 爬取广东所有学校
#         university_links = response.xpath('//div[@class="root"]/div[@class="container"]/div[@class="container"]/div[@class="container"]/div[@class="container"]/div[@class="clearfix"]/div[@class="main"]/div[@class="layoutWrap clearfix"]/div[@class="content-left_box__3SjwR"]/div[@class="school-search_schoolListMain__B9yLk"]/div[@class="school-search_listBox__at-rI"]/div/div[@class="school-search_schoolItem__3q7R2"]/h3/a/@href').extract()
#         for university_link in university_links:
#             yield scrapy.Request(url=university_link, callback=self.parse_university)
#
#     def parse_university(self, response):
#         # 爬取大学信息
#         item = UniversityItem()
#         item['province'] = response.xpath('//span[contains(text(), "所在地")]/following-sibling::span/text()').extract_first()
#         item['city'] = response.xpath('//span[contains(text(), "城市")]/following-sibling::span/text()').extract_first()
#         item['university_name'] = response.xpath('//h1[@class="school-name"]/text()').extract_first()
#         item['university_url'] = response.xpath('//a[@class="school-badge"]/@href').extract_first()
#         yield item
