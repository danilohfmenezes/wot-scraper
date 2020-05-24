# -*- coding: utf-8 -*-
import scrapy

# class Book():
#     title = Field()
#     title_abbr = Field()
#     chapters = Field()

# class Chapter():
#     title = Field()
#     title_abbr = Field()

# class POV():
#     character = Field()
#     word_count = Field()
#     weight = Field()
#     sex = Field()

# Learn Fields Later

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

char_db = {}


class ChapterInformationSpider(scrapy.Spider):
    name = 'chapter_information'
    allowed_domains = ['wot.fandom.com']
    start_urls = ['https://wot.fandom.com/wiki/Statistical_analysis']
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):
        for book in response.xpath('(//h2/span)[position()<last()]'):
            chapters = book.xpath(
                './/following::table[1]/tr[position() > 1]')
            book_name = book.xpath('.//text()').get()
            book_name = book_name.strip()
            book_abbr = self.get_book_abbr(book_name)
            # if book_abbr == 'TEOTW':
            for chapter in chapters:
                attributes = chapter.xpath(".//td")
                if len(attributes) > 3:
                    chapter_name = self.get_text(attributes[0])
                    chapter_url = self.get_url(attributes[0])
                else:
                    continue

                chapter_name = chapter_name.strip()
                yield response.follow(url=chapter_url, callback=self.parse_chapter, meta={
                    'book': {
                        'book': book_name,
                        'book_abbr': book_abbr,
                        'chapter': chapter_name,
                        'chapter_abbr': self.get_chapter_abbr(chapter_name)
                    }
                })

    def parse_chapter(self, response):
        # section = "Characters"
        # book = response.request.meta["book"]

        # section_header = response.xpath(f'//h2[span/@id="{section}"]')
        # if len(section_header) == 0:
        #     section_header = response.xpath(f'//h3[span/@id="{section}"]')

        # if len(section_header):
        #     siblings = section_header.xpath(
        #         './/following-sibling::*')

        #     section_ul = None
        #     for sibling in siblings:
        #         tag = sibling.xpath('name()').get()
        #         if tag == 'ul':
        #             section_ul = sibling
        #             break
        #         elif tag == 'h4' or tag == 'h3' or tag == 'h2':
        #             break

        #     if section_ul:
        #         elements = section_ul.xpath(
        #             './/li')
        #         for element in elements:
        #             txt = self.get_text(element)
        #             if txt:
        #                 character_url = self.get_url(element)
        #                 if character_url is None:
        #                     yield {
        #                         **book,
        #                         'type': f'Character',
        #                         'name': txt,
        #                         'name_join': txt,
        #                         'character_url': character_url
        #                     }
        #                 elif character_url in char_db.keys():
        #                     yield {
        #                         **book,
        #                         'type': f'Character',
        #                         'name': txt,
        #                         'name_join': char_db[character_url],
        #                         'character_url': character_url
        #                     }
        #                 else:
        #                     yield response.follow(url=character_url, callback=self.parse_character, meta={
        #                         'character': {
        #                             **book,
        #                             'type': f'Character',
        #                             'name': txt,
        #                             'name_join': txt,
        #                             'character_url': character_url
        #                         }
        #                     })

        #     referenced_section_header = None
        #     for sibling in siblings:
        #         tag = sibling.xpath('name()').get()
        #         text = sibling.xpath('.//text()').get()
        #         if tag == 'h3' and text == 'Referenced':
        #             referenced_section_header = sibling
        #             break
        #         elif tag == 'h2' or tag == 'h4':
        #             break

        #     if referenced_section_header:
        #         siblings = referenced_section_header.xpath(
        #             './/following-sibling::*')
        #         section_ul = None
        #         for sibling in siblings:
        #             tag = sibling.xpath('name()').get()
        #             if tag == 'ul':
        #                 section_ul = sibling
        #                 break
        #             elif tag == 'h4' or tag == 'h3' or tag == 'h2':
        #                 break

        #         if section_ul:
        #             elements = section_ul.xpath(
        #                 './/li')
        #             for element in elements:
        #                 txt = self.get_text(element)
        #                 if txt:
        #                     character_url = self.get_url(element)
        #                     if character_url is None:
        #                         yield {
        #                             **book,
        #                             'type': f'Referenced Character',
        #                             'name': txt,
        #                             'name_join': txt,
        #                             'character_url': character_url
        #                         }
        #                     elif character_url in char_db.keys():
        #                         yield {
        #                             **book,
        #                             'type': f'Referenced Character',
        #                             'name': txt,
        #                             'name_join': char_db[character_url],
        #                             'character_url': character_url
        #                         }
        #                     else:
        #                         yield response.follow(url=character_url, callback=self.parse_character, meta={
        #                             'character': {
        #                                 **book,
        #                                 'type': f'Referenced Character',
        #                                 'name': txt,
        #                                 'name_join': txt,
        #                                 'character_url': character_url
        #                             }
        #                         })


        for concept in self.parse_section(response, section='One_Power', type='Concept'):
            yield concept
        
        # for place in self.parse_section(response, section='Places', type='Place'):
        #     yield place

        # for item in self.parse_section(response, section='Items', type='Item'):
        #     yield item

        # for event in self.parse_section(response, section='Events', type='Event'):
        #     yield event

        # for concept in self.parse_section(response, section='Concepts', type='Concept'):
        #     yield concept

        # for group in self.parse_section(response, section='Groups', type='Group'):
        #     yield group

        # songs
        # stories

    def get_text(self, node):
        attr = node.xpath('.//a/text()').get()
        if attr is None:
            attr = node.xpath('.//i/a/text()').get()

        return self.strip(attr)

    def get_url(self, node):
        attr = node.xpath('.//a/@href').get()
        if attr is None:
            attr = node.xpath('.//i/a/@href').get()

        return attr

    def get_book_abbr(self, book):
        words = book.split(" ")
        first_letters = map(lambda w: w[0].upper(), words)
        return "".join(first_letters)

    def get_chapter_abbr(self, chapter):
        start = 2 if chapter.find("Ch") == 0 else 0
        end = len(chapter) if chapter.find(":") == -1 else chapter.find(":")
        return chapter[start:end]

    def strip(self, attribute):
        return None if attribute is None else attribute.strip()

    def parse_section(self, response, section, type):
        book = response.request.meta["book"]

        section_header = response.xpath(f'//h2[span/@id="{section}"]')
        if len(section_header) == 0:
            section_header = response.xpath(f'//h3[span/@id="{section}"]')

        if len(section_header):
            siblings = section_header.xpath(
                './/following-sibling::*')

            section_ul = None
            for sibling in siblings:
                tag = sibling.xpath('name()').get()
                if tag == 'ul':
                    section_ul = sibling
                    break
                elif tag == 'h4' or tag == 'h3' or tag == 'h2':
                    break

            if section_ul:
                elements = section_ul.xpath(
                    './/li')
                for element in elements:
                    txt = self.get_text(element)
                    if txt:
                        yield {
                            **book,
                            'type': f'{type}',
                            'name': txt,
                            'name_join': None,
                            'character_url': None
                        }

            referenced_section_header = None
            for sibling in siblings:
                tag = sibling.xpath('name()').get()
                text = sibling.xpath('.//text()').get()
                if tag == 'h3' and text == 'Referenced':
                    referenced_section_header = sibling
                    break
                elif tag == 'h2' or tag == 'h4':
                    break

            if referenced_section_header:
                siblings = referenced_section_header.xpath(
                    './/following-sibling::*')
                section_ul = None
                for sibling in siblings:
                    tag = sibling.xpath('name()').get()
                    if tag == 'ul':
                        section_ul = sibling
                        break
                    elif tag == 'h4' or tag == 'h3' or tag == 'h2':
                        break

                if section_ul:
                    elements = section_ul.xpath(
                        './/li')
                    for element in elements:
                        txt = self.get_text(element)
                        if txt:
                            yield {
                                **book,
                                'type': f'Referenced {type}',
                                'name': txt,
                                'name_join': None,
                                'character_url': None
                            }

    def parse_character(self, response):
        character = response.request.meta["character"]
        name_join = self.get_attribute(response, 'name')
        if name_join is not None:
            char_db[character['character_url']] = name_join
        yield {
            **character,
            'name_join': name_join if name_join else character['name_join']
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
