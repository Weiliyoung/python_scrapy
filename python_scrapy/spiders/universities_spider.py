import scrapy
from scrapy_splash import SplashRequest
from python_scrapy.spiders.items import UniversityItem

class GaokaoSpider(scrapy.Spider):
    name = 'universities'
    allowed_domains = ['www.gaokao.cn']
    start_urls = ['https://www.gaokao.cn/school/search']

    def start_requests(self):
        script = """
        function main(splash)
            splash:set_viewport_size(1024, 768)
            splash:wait(1)
            splash:runjs("document.querySelector('.filter-wrap a[data-province=\"广东\"]').click()")
            splash:wait(2)
            return splash:html()
        end
        """

        yield SplashRequest(url=self.start_urls[0], callback=self.parse, endpoint='execute',
                            args={'lua_source': script})

    def parse(self, response):
        # 获取广东所有学校的数据
        school_data_list = response.xpath('//div[@class="search-item"]')

        for school_data in school_data_list:
            # 提取学校名称和触发点击事件的 JavaScript 代码
            school_name = school_data.xpath('//div[@class="school-search_schoolItem__3q7R2"]//h3/em/text()').get()
            js_event = school_data.xpath('.//h3/a/@onclick').get()

            # 提取学校的省份和城市
            province = school_data.xpath('.//span[contains(text(), "所在地")]/following-sibling::span/text()').get()
            city = school_data.xpath('.//span[contains(text(), "城市")]/following-sibling::span/text()').get()

            if school_name and js_event:
                # 使用 Splash 发起点击事件
                yield SplashRequest(url=response.url,
                                    callback=self.parse_university,
                                    endpoint='execute',
                                    args={'lua_source': js_event},
                                    meta={'province': province, 'city': city, 'school_name': school_name})

    def parse_university(self, response):
        # 获取大学信息
        item = UniversityItem()
        item['province'] = response.meta['province']
        item['city'] = response.meta['city']
        item['university_name'] = response.meta['school_name']
        item['university_url'] = response.url  # 这里直接使用 response.url 作为大学的 URL
        yield item
