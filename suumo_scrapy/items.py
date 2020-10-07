# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
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


def _to_int(value):
    return int(float(value[0:-2]) * 10)


def _transfer_year(value):
    if value == '新築':
        return 2018
    else:
        return 2018 - int(value[1:-1])


def _transfer_area(value):
    return float(value[0:-2])


def _stations_formatter(value):
    res = []
    stations = value.split()
    for station in stations:
        data = station.split('/')
        dis = re.search('(\d+)分', data[1].split('駅')[1])
        res.append({
            'line': data[0],
            'station': data[1].split('駅')[0],
            'distance': int(dis.group()[0:-1])
        })

    return res


class SuumoScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace)
    )
    price = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace, _to_int)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()

    address = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace)
    )
    stations = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_tab, _remove_space, _whitespace_to_space,
                                   _stations_formatter)
    )
    size = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace)
    )
    area = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace, _transfer_area)
    )

    build_year = scrapy.Field(
        input_processor=MapCompose(remove_tags, _remove_whitespace, _transfer_year)
    )
    floor = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )

    crawl_time = scrapy.Field()
