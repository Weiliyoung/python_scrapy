import scrapy

class UniversityItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    university_name = scrapy.Field()
    university_url = scrapy.Field()
