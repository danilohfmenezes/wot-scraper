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
            relative_url = f'/wiki/Category:Women?from={letter}'
            yield response.follow(url=relative_url, callback=self.parse_letter, meta={'letter': letter})

    def parse_letter(self, response):
        letter = response.request.meta['letter']
        characters = response.xpath(
            f'//div[@class="category-page__first-char" and contains(text(),"{letter}")]/following-sibling::ul[1]/li/a')

        for character in characters:
            character_url = character.xpath(".//@href").get()
            yield response.follow(url=character_url, callback=self.parse_character)

    def parse_character(self, response):
        first_metioned = self.split_book_chapter(
            self.get_attribute(response, 'mentioned'))
        last_mentioned = self.split_book_chapter(
            self.get_attribute(response, 'lastmentioned'))
        first_appeared = self.split_book_chapter(
            self.get_attribute(response, 'appeared'))
        last_appeared = self.split_book_chapter(
            self.get_attribute(response, 'lastappeared'))

        yield {
            'name': self.get_attribute(response, 'name'),
            'birth': self.get_attribute(response, 'birth'),
            'nationality': self.get_attribute(response, 'nationality'),
            'gender': self.get_attribute(response, 'gender'),
            'height': self.get_attribute(response, 'height'),
            'weight': self.get_attribute(response, 'weight'),
            'hair_color': self.get_attribute(response, 'hair'),
            'eye_color': self.get_attribute(response, 'eyes'),
            'build': self.get_attribute(response, 'build'),
            'race': self.get_attribute(response, 'race'),
            'first_mentioned_book': first_metioned['book'],
            'first_mentioned_chapter': first_metioned['chapter'],
            'last_mentioned_book': last_mentioned['book'],
            'last_mentioned_chapter': last_mentioned['chapter'],
            'first_appeared_book': first_appeared['book'],
            'first_appeared_chapter': first_appeared['chapter'],
            'last_appeared_book': last_appeared['book'],
            'last_appeared_chapter': last_appeared['chapter'],
            'affiliation': self.get_attribute(response, 'affiliation'),
            'title': self.get_attribute(response, 'title'),
            'rank': self.get_attribute(response, 'rank'),
            'status': self.get_attribute(response, 'status'),
            'death': self.get_attribute(response, 'death'),
            'occupation': self.get_attribute(response, 'occupation'),
            'ajah': self.get_attribute(response, 'ajah'),
            'clan': self.get_attribute(response, 'clan'),
            'sept': self.get_attribute(response, 'sept'),
        }

    def get_attribute(self, response, attribute):
        if attribute == 'name':
            attr = response.xpath(
                '//aside/descendant::*[@data-source="name"]/text()').get()
        else:
            attr = response.xpath(
                f'.//descendant::*[@data-source="{attribute}"]/div/a/text()').get()

            if attr is None:
                attr = response.xpath(
                    f'.//descendant::*[@data-source="{attribute}"]/div/text()').get()

        return self.strip(attr)

    def split_book_chapter(self, attribute):
        if attribute is None:
            return {
                'book': None,
                'chapter': None
            }

        splitted = attribute.split("\xa0")

        return {
            'book': self.strip(splitted[0]),
            'chapter':  self.strip(splitted[1]) if len(splitted) > 1 else None
        }

    def strip(self, attribute):
        return None if attribute is None else attribute.strip()
