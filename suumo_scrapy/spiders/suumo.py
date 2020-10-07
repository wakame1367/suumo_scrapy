import scrapy


class SuumoSpider(scrapy.Spider):
    name = 'suumo'
    allowed_domains = ['suumo.jp']
    start_urls = [
        'https://suumo.jp/jj/chintai/ichiran/FR301FC001/'
        '?ar=030&bs=040&ta=13&sc=13103&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1']

    def parse(self, response):
        pass
