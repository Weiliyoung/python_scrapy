import scrapy


class GDHSCSpider(scrapy.Spider):
    name = 'test_gdhsc_spider'
    start_urls = ['https://www.gdhsc.edu.cn/']

    def parse(self, response):
        self.logger.debug("Parsing started for URL: %s", response.url)

        # 在此处添加提取招生就业链接的代码
        recruitment_url = response.xpath('//a[text()="招生就业"]/@href').get()
        if recruitment_url:
            yield response.follow(recruitment_url, callback=self.parse_recruitment_news)

    def parse_recruitment_news(self, response):
        self.logger.debug("Parsing recruitment news URL: %s", response.url)

        # 在此处添加提取招生要闻数据的代码
        recruitment_news = response.xpath('//a[text()="招生要闻"]/@href').get()
        if recruitment_news:
            yield response.follow(recruitment_news, callback=self.parse_news_content)

    def parse_news_content(self, response):
        self.logger.debug("Parsing recruitment news content URL: %s", response.url)

        # 在此处添加提取招生要闻内容的代码
        news_content = response.xpath(
            '//div[@class="l_con"]//div[contains(@class, "l_box") and contains(@class, "clearfix")]//div[contains(@class, "l_right") and contains(@class, "fr")]/ul/li//text()').getall()
        for content in news_content:
            yield {
                'news_content': content.strip()
            }
