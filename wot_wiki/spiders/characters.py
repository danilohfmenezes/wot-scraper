# -*- coding: utf-8 -*-
import scrapy
import logging


class CharactersSpider(scrapy.Spider):
    name = 'characters'
    allowed_domains = ['wot.fandom.com']
    start_urls = ['https://wot.fandom.com/wiki/Rand_al%27Thor',
                  'https://wot.fandom.com/wiki/Aginor',
                  'https://wot.fandom.com/wiki/El%27Nynaeve_ti_al%27Meara_Mandragoran']

    def parse(self, response):
        first_metioned = self.splitBookChapter(
            self.getAttribute(response, 'mentioned'))
        first_appeared = self.splitBookChapter(
            self.getAttribute(response, 'appeared'))
        last_appeared = self.splitBookChapter(
            self.getAttribute(response, 'lastappeared'))

        yield {
            'name': self.getAttribute(response, 'name'),
            'nationality': self.getAttribute(response, 'nationality'),
            'gender': self.getAttribute(response, 'gender'),
            'hair_color': self.getAttribute(response, 'hair'),
            'eye_color': self.getAttribute(response, 'eyes'),
            'first_mentioned_book': first_metioned['book'],
            'first_mentioned_chapter': first_metioned['chapter'],
            'first_appeared_book': first_appeared['book'],
            'first_appeared_chapter': first_appeared['chapter'],
            'last_appeared_book': last_appeared['book'],
            'last_appeared_chapter': last_appeared['chapter'],
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

    def splitBookChapter(self, attribute):
        if attribute is None:
            return {
                'book': None,
                'chapter': None
            }

        book, chapter = attribute.split("\xa0")

        return {
            'book': book,
            'chapter': chapter
        }
