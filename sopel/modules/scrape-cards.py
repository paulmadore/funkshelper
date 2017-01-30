from scrapy.selector import HtmlXPathSelector
from scrapy.spiders import Spider
from scrapy.http import Request

DOMAIN = 'gatherer.wizards.com/Pages/Search/Default.aspx?output=compact&color=|[W]|[U]|[B]|[R]|[G]&type=+[Creature]'
URL = 'http://%s' % DOMAIN

class MySpider(Spider):
    name = DOMAIN
    allowed_domains = [DOMAIN]
    start_urls = [
        URL
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        for url in hxs.select('//a/@href').extract():
            if not ( url.startswith('http://') or url.startswith('https://') ):
                url = URL + url
            print url
            yield Request(url, callback=self.parse)
            