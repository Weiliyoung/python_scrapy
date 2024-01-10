import scrapy

class GaokaoSpider(scrapy.Spider):
    name = 'universities'
    start_urls = ['https://www.gaokao.cn/school/search']

    def parse(self, response):
        # 点击广东省获取学校列表
        yield scrapy.FormRequest.from_response(
            response,
            formxpath='//div[contains(@class, "root") and contains(@class, "container") and contains(@class, "clearfix") and contains(@class, "main") and contains(@class, "layoutWrap") and contains(@class, "content-left_box__3SjwR") and contains(@class, "school-search_schoolListMain__B9yLk") and contains(@class, "school-search_findBox__3C5IT") and contains(@class, "filter-compents_filterBox__3mqfw") and contains(@class, "filter-compents_itemBox__1Q3EV") and contains(@class, "filter-compents_allFilter__2dgwE") and contains(@class, "filter-compents_filterItem__1JB3L")]//span[text()="广东"]',
            callback=self.parse_schools
        )

    def parse_schools(self, response):
        # 获取学校列表中的每个大学链接
        university_links = response.xpath('//div[@class="root"]//div[@class="container"]//div[@class="container"]//div[@class="container"]//div[@class="container"]//div[@class="clearfix"]//div[@class="main"]//div[@class="layoutWrap clearfix"]//div[@class="content-left_box__3SjwR"]//div[@class="school-search_schoolListMain__B9yLk"]//div[@class="school-search_listBox__at-rI"]//div[@style="border: none; padding: 0px;"]//div[@class="school-search_schoolItem__3q7R2"](@href, "school/")]')
        for link in university_links:
            university_url = link.xpath('./@href').get()
            yield response.follow(university_url, callback=self.parse_university)

    def parse_university(self, response):
        # 解析大学页面获取大学名称和官网 URL
        university_name = response.xpath('//div[@class="root"]//div[@class="container"]//div[@class="container"]//div[@class="container"]//div//div[@class="clearfix"]//div[@class="main"]//div[@class="layoutWrap clearfix"]//div[@class="relative-for-liuyan"]//div[@class="relative_box"]//div[@class="school clearfix"]//div[@class="schoolName clearfix school_view_top"]//div[@class="line1"]//span[@class="line1-schoolName"]//h1/text()').get()
        university_url = response.xpath('//div[@class="root"]//div[@class="container"]//div[@class="container"]//div[@class="container"]//div//div[@class="clearfix"]//div[@class="main"]//div[@class="layoutWrap clearfix"]//div[@class="relative-for-liuyan"]//div[@class="relative_box"]//div[@class="school clearfix"]//div[@class="schoolName clearfix school_view_top"]//div[@class="line3"]//div[@class="line3_item"]/span[@class="school-info-label"]//a[contains(text(), "官网")]/@href').get()

        # 获取大学所在省份和城市名称
        university_info = response.xpath('//div[@class="root"]//div[@class="container"]//div[@class="container"]//div[@class="container"]//div//div[@class="clearfix"]//div[@class="main"]//div[@class="layoutWrap clearfix"]//div[@class="relative-for-liuyan"]//div[@class="relative_box"]//div[@class="school clearfix"]//div[@class="schoolName clearfix school_view_top"]//div[@class="l-city"]/span[@class="line1-province" contains(text(), "所在地")]/following-sibling::a')
        province = university_info[0].xpath('./text()').get()
        city = university_info[1].xpath('./text()').get()

        yield {
            'university_name': university_name,
            'university_url': university_url,
            'province': province,
            'city': city
        }
