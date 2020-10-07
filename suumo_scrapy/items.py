# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def _remove_whitespace(value):
    return re.sub('\s+', '', value)


def _remove_tab(value):
    return re.sub('\t', '', value)


def _remove_space(value):
    return re.sub(' ', '', value)


def _whitespace_to_space(value):
    return re.sub('\s+', ' ', value)


def _transfer_area(value):
    return float(value[0:-2])


def _stations_formatter(value):
    sep = '\r\n'
    return value.lstrip(sep).rstrip(sep)


class SuumoScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:

    field_and_default_processor = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace, _remove_space)
    )
    name = field_and_default_processor
    price = field_and_default_processor
    url = scrapy.Field()
    address = field_and_default_processor
    stations = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_tab, _remove_space, _stations_formatter)
    )
    common_charges = field_and_default_processor
    size = field_and_default_processor
    area = field_and_default_processor
    build_year = field_and_default_processor
    floor = field_and_default_processor
    direction = field_and_default_processor
    building_type = field_and_default_processor
    # 敷金/礼金
    deposit_and_gratuity_fee = field_and_default_processor
    # 保証金
    security_deposit = field_and_default_processor
    # 敷引・償却
    expense_deposits = field_and_default_processor
    # 部屋の特徴・設備
    others = field_and_default_processor
    # 仲介手数料
    brokerage_fee = field_and_default_processor
    # 損保
    damage_insurance = field_and_default_processor
    # 入居可能か
    is_move_in = field_and_default_processor
    # 間取り詳細
    floor_plan_details = field_and_default_processor
    # 条件
    requirement = field_and_default_processor
    # SUUMO物件コード
    suumo_code = field_and_default_processor
    # ほか諸費用
    other_expenses = field_and_default_processor
    # 備考
    note = field_and_default_processor
    # 構造
    structure = field_and_default_processor
    # 駐車場
    parking_lot = field_and_default_processor
    # 取引態様
    business_transactions = field_and_default_processor
    # 取り扱い店舗物件コード
    stores_code = field_and_default_processor
    # 総戸数
    total_number_of_houses = field_and_default_processor
    crawl_time = scrapy.Field()
