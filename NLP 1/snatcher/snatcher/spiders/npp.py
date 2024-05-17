import scrapy
from snatcher.dblib import DB_link

class NppSpider(scrapy.Spider):
    name = "npp"
    allowed_domains = ["nplus1.ru"]
    start_url = "https://nplus1.ru"
    #custom_settings = {"LOG_FILE":f"db/log/{name}.log",'DOWNLOAD_DELAY':0,'ROBOTSTXT_OBEY':False}

    # cookie = {}
    # header = {}


    def start_requests(self):

        self.db = DB_link(self.name)
        self.db.InitDir()
        self.db.InitDB()

        yield scrapy.Request(
            url=self.start_url,
            # cookies=
            callback=self.main_parse
        )

    def main_parse(self, response):
        
        # Получаем список ссылко и делим их
        # На Блог, Материал, Новость\
        methods = {'material':self.material_parser, 'news':self.news_parser, 'blog':self.blog_parser}

        for link in response.xpath('//a/@href').getall():
            if ('https://nplus1.ru/' in link and ('/material/' in link or '/news/' in link or '/blog/' in link)):
                method = methods[link.split('/')[3]]

                yield scrapy.Request(
                    url=link,
                    callback=method
                    # cookie
                    # header
                )


    # Вообще на сайте много чего прописано в <head>
    # Но xpath-ы практиковать веселей
    
    

    def news_parser(self, response):
        article = []
        content_div = response.xpath("//div[@class='flex flex-col']")[0]
        p2 = content_div.xpath('p/text()').get() if content_div.xpath('p/text()') else ''
        article.append('.'.join([content_div.xpath('h1/text()').get().strip(), p2.strip() ])) # title
        article.append('.'.join(content_div.xpath('//div[@class="n1_material text-18"]/p/text()').getall())) # content
        meta_div = response.xpath('//div[@class="flex flex-wrap lg:mb-10 gap-2 text-tags xl:pr-9"]')[0].xpath('a/span/text()').getall() 
        article.append(';'.join(meta_div[2:])) # tags
        article.append(meta_div[0]) # dt
        article.append('news')
        
        self.db.AddToDB(article)

    def blog_parser(self, response):
        article = []
        content_div = response.xpath("//div[@class='flex flex-col']")[0]
        p2 = content_div.xpath('p/text()').get() if content_div.xpath('p/text()') else ''
        article.append('.'.join([content_div.xpath('h1/text()').get().strip(), p2.strip() ])) # title
        article.append('.'.join(content_div.xpath('//div[@class="n1_material text-18"]/p/text()').getall())) # content
        meta_div = response.xpath('//div[@class="flex flex-wrap lg:mb-10 gap-2 text-tags xl:pr-9"]/a/span/text()').getall() 
        article.append(';'.join(meta_div[2:])) # tags
        article.append(meta_div[0]) # dt
        article.append('blog')

        self.db.AddToDB(article)
    
    def material_parser(self, response):
        article = []
        content_div = response.xpath("//div[@class='flex flex-col']")[0]
        p2 = content_div.xpath('p/text()').get() if content_div.xpath('p/text()') else ''
        article.append('.'.join([content_div.xpath('h1/text()').get().strip(), p2.strip() ])) # title
        article.append('.'.join(content_div.xpath('//div[@class="n1_material text-18"]/p/text()').getall())) # content
        meta_div = response.xpath('//div[@class="flex text-white n1_text_shadow lg:text-main-black flex-wrap mb-10 gap-2 text-tags"]/a/span/text()').getall() 
        article.append(';'.join(meta_div[2:])) # tags
        article.append(meta_div[0]) # dt
        article.append('material')
        
        self.db.AddToDB(article)