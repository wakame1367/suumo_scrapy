import hashlib
from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from suumo_scrapy.items import SuumoScrapyItem, ArticleItemLoader


def _get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


class SuumoSpider(CrawlSpider):
    name = 'suumo'
    allowed_domains = ['suumo.jp']
    start_urls = [
        'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13103&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1']

    rules = (
        Rule(LinkExtractor(allow=r'chintai/'), callback='parse_item', follow=True),
    )

    #
    # def parse_start_url(self, response):
    #     return []
    #
    # def process_results(self, response, results):
    #     return results

    def parse_item(self, response):
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        if response.css('.property_view_note-emphasis').extract():
            price_class = '.property_view_note-emphasis'
        else:
            price_class = '.property_view_main-emphasis'

        if response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tr[1]/td').extract():
            address_xpath = '//*[@id="js-view_gallery"]/div[3]/table/tr[1]/td'
            stations_xpath = '//*[@id="js-view_gallery"]/div[3]/table/tr[2]/td'
            size_xpath = '//*[@id="js-view_gallery"]/div[3]/table/tr[3]/td[1]'
            area_xpath = '//*[@id="js-view_gallery"]/div[3]/table/tr[3]/td[2]'
            build_year_xpath = '//*[@id="js-view_gallery"]/div[3]/table/tr[4]/td[1]'
        else:
            address_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div'
            stations_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]'
            size_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[1]/div/div[2]/ul/li[1]/div/div[2]'
            area_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[1]/div/div[2]/ul/li[2]/div/div[2]'
            build_year_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[1]/div/div[2]/ul/li[5]/div/div[2]'

        if response.xpath('//*[@id="js-view_gallery"]/div[3]/table/tr[4]/td[2]').extract():
            floor_xpath = '//*[@id="js-view_gallery"]/div[3]/table/tr[4]/td[2]'
        elif response.xpath('//*[@id="contents"]/div[2]/table/tr[2]/td[1]').extract():
            floor_xpath = '//*[@id="contents"]/div[2]/table/tr[2]/td[1]'
        elif response.xpath('//*[@id="contents"]/div[3]/table/tr[2]/td[1]').extract():
            floor_xpath = '//*[@id="contents"]/div[3]/table/tr[2]/td[1]'
        else:
            floor_xpath = '//*[@id="contents"]/div[4]/table/tr[2]/td[1]'

        item_loader = ArticleItemLoader(item=SuumoScrapyItem(), response=response)

        item_loader.add_xpath("name", '//*[@id="wrapper"]/div[3]/div[1]/h1')
        item_loader.add_css("price", price_class)
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", _get_md5(response.url))
        # do not ues tbady
        item_loader.add_xpath("address", address_xpath)
        item_loader.add_xpath("stations", stations_xpath)
        item_loader.add_xpath("size", size_xpath)
        item_loader.add_xpath("area", area_xpath)
        # >
        item_loader.add_xpath("build_year", build_year_xpath)
        item_loader.add_xpath("floor", floor_xpath)

        item_loader.add_value("crawl_time", datetime.now())

        article_item = item_loader.load_item()

        return article_item
