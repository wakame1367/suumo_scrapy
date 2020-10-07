from datetime import datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import scrapy
from suumo_scrapy.items import SuumoScrapyItem, ArticleItemLoader


class SuumoSpider(CrawlSpider):
    name = 'suumo'
    allowed_domains = ['suumo.jp']
    # start_urls = [
    #     'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ta=13&sc=13103&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&srch_navi=1']
    # start_urls = ['https://suumo.jp/chintai/bc_100210936511/']
    # rules = (
    #     Rule(LinkExtractor(allow=r'chintai/'), callback='parse_item', follow=True),
    # )
    def start_requests(self):
        urls = ['https://suumo.jp/chintai/bc_100210936511/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_item)
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

        else:

            address_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div[2]/div'
            stations_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[2]/div[1]/div/div[2]'
            size_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[1]/div/div[2]/ul/li[1]/div/div[2]'
            area_xpath = '//*[@id="js-view_gallery"]/div[1]/div[2]/div[3]/div[1]/div/div[2]/ul/li[2]/div/div[2]'
            direction_xpath = '//*[@id="js-view_gallery"]/div/div[2]/div[3]/div[1]/div/div[2]/ul/li[3]/div/div[2]'
            building_type_xpath = '//*[@id="js-view_gallery"]/div/div[2]/div[3]/div[1]/div/div[2]/ul/li[4]/div/div[2]'
            deposit_and_gratuity_fee_xpath = '//*[@id="js-view_gallery"]/div/div[2]/div[2]/div/div[2]/div/div[2]/ul/li[1]/div/div[2]'
            security_deposit_xpath = '//*[@id="js-view_gallery"]/div/div[2]/div[2]/div/div[2]/div/div[2]/ul/li[2]/div/div[2]'
            expense_deposits_xpath = '//*[@id="js-view_gallery"]/div/div[2]/div[2]/div/div[2]/div/div[2]/ul/li[3]/div/div[2]'
            common_charges_xpath = '//*[@id="js-view_gallery"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div[2]'

        # 物件概要
        # 動的にテーブルの構造が変化する
        table_xpaths = ['//*[@id="js-view_gallery"]/div[3]/table',
                        '//*[@id="contents"]/div[2]/table',
                        '//*[@id="contents"]/div[3]/table',
                        '//*[@id="contents"]/div[4]/table']
        for table_xpath in table_xpaths:
            if response.xpath(table_xpath).get():
                break

        floor_plan_details_xpath = table_xpath + '/tbody/tr[1]/td[1]'
        floor_xpath = table_xpath + '/tr[4]/td[2]'
        damage_insurance_xpath = table_xpath + '/tbody/tr[3]/td[1]'
        move_in_xpath = table_xpath + '/tbody/tr[4]/td[1]'
        requirement_xpath = table_xpath + '/tbody/tr[5]/td[1]'
        suumo_code_xpath = table_xpath + '/tbody/tr[6]/td[1]'
        brokerage_fee_xpath = table_xpath + '/tbody/tr[7]/td/ul/li'
        other_expenses_xpath = table_xpath + '/tbody/tr[8]/td/ul/li'
        note_xpath = table_xpath + '/tbody/tr[9]/td/ul/li'
        structure_xpath = table_xpath + '/tbody/tr[1]/td[2]'
        build_year_xpath = table_xpath + '/tbody/tr[2]/td[2]'
        parking_lot_xpath = table_xpath + '/tbody/tr[3]/td[2]'
        business_transactions_xpath = table_xpath + '/tbody/tr[4]/td[2]'
        stores_code_xpath = table_xpath + '/tbody/tr[5]/td[2]'
        total_number_of_houses_xpath = table_xpath + '/tbody/tr[6]/td[2]'

        others_xpath = '//*[@id="bkdt-option"]/div/ul/li'
        item_loader = ArticleItemLoader(item=SuumoScrapyItem(), response=response)

        item_loader.add_xpath("name", '//*[@id="wrapper"]/div[3]/div[1]/h1')
        item_loader.add_css("price", price_class)
        item_loader.add_value("url", response.url)
        # do not ues tbady
        item_loader.add_xpath("address", address_xpath)
        item_loader.add_xpath("stations", stations_xpath)
        item_loader.add_xpath("size", size_xpath)
        item_loader.add_xpath("area", area_xpath)
        # >
        item_loader.add_xpath("build_year", build_year_xpath)
        item_loader.add_xpath("floor", floor_xpath)
        item_loader.add_xpath("building_type", building_type_xpath)

        item_loader.add_xpath("direction", direction_xpath)
        item_loader.add_xpath("deposit_and_gratuity_fee", deposit_and_gratuity_fee_xpath)
        item_loader.add_xpath("security_deposit", security_deposit_xpath)
        item_loader.add_xpath("expense_deposits", expense_deposits_xpath)
        item_loader.add_xpath("common_charges", common_charges_xpath)

        item_loader.add_xpath("others", others_xpath)

        item_loader.add_xpath("brokerage_fee", brokerage_fee_xpath)
        item_loader.add_xpath("is_move_in", move_in_xpath)
        item_loader.add_xpath("floor_plan_details", floor_plan_details_xpath)
        item_loader.add_xpath("damage_insurance", damage_insurance_xpath)
        item_loader.add_xpath("requirement", requirement_xpath)
        item_loader.add_xpath("suumo_code", suumo_code_xpath)
        item_loader.add_xpath("other_expenses", other_expenses_xpath)
        item_loader.add_xpath("note", note_xpath)
        item_loader.add_xpath("structure", structure_xpath)
        item_loader.add_xpath("parking_lot", parking_lot_xpath)
        item_loader.add_xpath("business_transactions", business_transactions_xpath)
        item_loader.add_xpath("stores_code", stores_code_xpath)
        item_loader.add_xpath("total_number_of_houses", total_number_of_houses_xpath)

        item_loader.add_value("crawl_time", datetime.now())

        article_item = item_loader.load_item()

        return article_item
