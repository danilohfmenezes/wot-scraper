# -*- coding: utf-8 -*-
import scrapy


class CharactersSpider(scrapy.Spider):
    name = 'characters'
    allowed_domains = ['wot.fandom.com']
    start_urls = ['https://wot.fandom.com/wiki/Rand_al%27Thor',
                  'https://wot.fandom.com/wiki/Aginor',
                  'https://wot.fandom.com/wiki/El%27Nynaeve_ti_al%27Meara_Mandragoran']

    def parse(self, response):
        yield {
            'name': self.getAttribute(response, 'name'),
            'nationality': self.getAttribute(response, 'nationality'),
            'gender': self.getAttribute(response, 'gender'),
            'hair_color': self.getAttribute(response, 'hair'),
            'eye_color': self.getAttribute(response, 'eyes'),
            'first_mentioned': self.getAttribute(response, 'mentioned'),
            'first_appeared': self.getAttribute(response, 'appeared'),
            'last_appeared': self.getAttribute(response, 'lastappeared'),
            'ajah': self.getAttribute(response, 'ajah')
        }

    def getAttribute(self, response, attribute):
        if attribute == 'name':
            return response.xpath(
                '//aside/descendant::*[@data-source="name"]/text()').get()
        else:
            attr = response.xpath(
                f'.//descendant::*[@data-source="{attribute}"]/div/a/text()').get()

            if attr is None:
                attr = response.xpath(
                    f'.//descendant::*[@data-source="{attribute}"]/div/text()').get()

            return attr
