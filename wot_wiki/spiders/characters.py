# -*- coding: utf-8 -*-
import scrapy
import string
import logging


class CharactersSpider(scrapy.Spider):
    name = 'characters'
    allowed_domains = ['wot.fandom.com']
    start_urls = ['https://wot.fandom.com']

    def parse(self, response):
        alphabet = list(string.ascii_uppercase)

        for letter in alphabet:
            relative_url = f'/wiki/Category:Men?from={letter}'
            yield response.follow(url=relative_url, callback=self.parse_letter, meta={'letter': letter})

    def parse_letter(self, response):
        letter = response.request.meta['letter']
        characters = response.xpath(
            f'//div[@class="category-page__first-char" and contains(text(),"{letter}")]/following-sibling::ul[1]/li/a')

        for character in characters:
            character_url = character.xpath(".//@href").get()
            yield response.follow(url=character_url, callback=self.parse_character)

    def parse_character(self, response):
        first_metioned = self.splitBookChapter(
            self.getAttribute(response, 'mentioned'))
        first_appeared = self.splitBookChapter(
            self.getAttribute(response, 'appeared'))
        last_appeared = self.splitBookChapter(
            self.getAttribute(response, 'lastappeared'))

        yield {
            'name': self.getAttribute(response, 'name'),
            'birth': self.getAttribute(response, 'birth'),
            'nationality': self.getAttribute(response, 'nationality'),
            'gender': self.getAttribute(response, 'gender'),
            'height': self.getAttribute(response, 'height'),
            'weight': self.getAttribute(response, 'weight'),
            'hair_color': self.getAttribute(response, 'hair'),
            'eye_color': self.getAttribute(response, 'eyes'),
            'build': self.getAttribute(response, 'build'),
            'race': self.getAttribute(response, 'race'),
            'first_mentioned_book': first_metioned['book'],
            'first_mentioned_chapter': first_metioned['chapter'],
            'first_appeared_book': first_appeared['book'],
            'first_appeared_chapter': first_appeared['chapter'],
            'last_appeared_book': last_appeared['book'],
            'last_appeared_chapter': last_appeared['chapter'],
            'affiliation': self.getAttribute(response, 'affiliation'),
            'title': self.getAttribute(response, 'title'),
            'rank': self.getAttribute(response, 'rank'),
            'status': self.getAttribute(response, 'status'),
            'death': self.getAttribute(response, 'death'),
            'occupation': self.getAttribute(response, 'occupation'),
            'ajah': self.getAttribute(response, 'ajah'),
            'clan': self.getAttribute(response, 'clan'),
            'sept': self.getAttribute(response, 'sept'),
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

        splitted = attribute.split("\xa0")

        return {
            'book': splitted[0],
            'chapter': splitted[1] if len(splitted) > 1 else None
        }
