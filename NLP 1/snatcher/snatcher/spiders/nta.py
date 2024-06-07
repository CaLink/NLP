import scrapy
from .lib import DB_link
import dateutil.parser as dp


class NtaSpider(scrapy.Spider):
    name = "nta"
    allowed_domains = ["nta-pfo.ru"]

    main_url = 'https://nta-pfo.ru'
    pagin_url = 'https://nta-pfo.ru/news/?PAGEN_1={page}&SIZEN_1={count}'
    
    page = 800
    cnt = 30

    saver = None

    def start_requests(self):
        self.saver = DB_link(self.name)
        self.saver.InitDir()
        self.saver.InitDB()




        yield scrapy.Request(
            self.pagin_url.format(page=self.page, count=self.cnt),
            callback=self.pagin_parser
        )


    def pagin_parser(self, response):
        article_urls = response.xpath('//div[@class="nta-news-list nta-news-line"]/a/@href').getall()

        for url in article_urls:
            yield scrapy.Request(
                self.main_url + url,
                callback=self.article_parser
            )

        next_page = response.xpath('//div[@class="bx_pagination_page"]/ul/li[last()]/a/@href').get()

        if next_page:
            yield scrapy.Request(
                self.main_url + next_page,
                callback=self.pagin_parser
            )

        

    def article_parser(self, response):

        tags = response.xpath('//div[@class="h1"]/text()').get()
        tags = ';'.join(tags.split('.'))

        title = response.xpath('//article/h1/text()').get()
        
        content = response.xpath('//div[@class="news-detail"]/text()').getall()
        content = ''.join(content).replace('\t', '').replace('\n', '')

        date = dp.parse(response.xpath('//time[@class="news-date-time"]/@datetime')
                         .get()).strftime('%Y-%m-%d')
        
        instance = (title, content, tags, date)
        self.saver.AddToDB(instance)

        