import scrapy


class UfrpeCrawlerSpider(scrapy.Spider):
    name = 'ufrpe_crawler'
    START_URL = ''
   # allowed_domains = ['https://crawler-test.com']

    def __init__(self, *args, **kwargs):
        global START_URL
        super(UfrpeCrawlerSpider, self).__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls').split(',') # retorna uma lista de urls com a separação das strings pela ','
        START_URL = kwargs.get('start_urls').split(',')
        
    def parse(self, response):
        global START_URL
        
        if 'bompreco' in START_URL[0]:
        
            for r in response.css('a.vtex-product-summary-2-x-clearLink'):
                url = r.css('::attr(href)').get()
                txt = r.css('::text').get()
                preco = r.css('span.vtex-productShowCasePrice ::text').get()
                
                yield {
                    'URL' : 'https://www.bompreco.com.br/' + url,
                    'NOME_PRODUTO' : txt,
                    'PRECO': preco,
                    'IMAGEM': '',
                }
        elif 'amazon' in START_URL[0]:
            for r in response.css('a.s-no-outline'):
                url = r.css('::attr(href)').get()
                txt = r.css('img::attr(alt)').get()
                preco = r.css('span::text').get()
                yield {
                    'URL' :  url,
                    'NOME_PRODUTO' : txt,
                    'PRECO': preco,
                }
            
      
