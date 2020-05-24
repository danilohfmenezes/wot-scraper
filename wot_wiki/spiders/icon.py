# -*- coding: utf-8 -*-
import scrapy


class Book(scrapy.Item):
    book = scrapy.Field()
    book_abbr = scrapy.Field()
    book_order = scrapy.Field()
    chapter = scrapy.Field()
    chapter_abbr = scrapy.Field()
    chapter_order = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug-icon.log"),
        logging.StreamHandler()
    ]
)


class IconSpider(scrapy.Spider):
    name = 'icon'
    allowed_domains = ['library.tarvalon.net']
    start_urls = [
        'https://library.tarvalon.net/index.php?title=Chapter_Icons_(By_Book)']

    def parse(self, response):
        book_order = 0
        chapter_order = 0
        for book in response.xpath('//h2/span'):
            book_order += 1
            chapters = book.xpath(
                './/following::table[1]/tr[position() > 1]')
            book_name = book.xpath('.//text()').get()
            book_name = book_name.strip()
            book_abbr = self.get_book_abbr(book_name)

            for chapter in chapters:
                chapter_order += 1
                attributes = chapter.xpath(".//td")
                chapter_name = self.get_text(attributes[0])

                chapter_url = chapter.xpath('.//a/@href').get()

                chapter_name = chapter_name.strip()
                yield response.follow(url=chapter_url, callback=self.parse_chapter, meta={
                    'book': {
                        'book': book_name,
                        'book_abbr': book_abbr,
                        'book_order': book_order,
                        'chapter': chapter_name,
                        'chapter_abbr': self.get_chapter_abbr(chapter_name),
                        'chapter_order': chapter_order
                    }
                })

    def parse_chapter(self, response):
        book = response.request.meta["book"]
        book_obj = Book(book=book['book'], book_abbr=book['book_abbr'], book_order=book['book_order'],
                        chapter=book['chapter'], chapter_abbr=book['chapter_abbr'], chapter_order=book['chapter_order'])
        book_obj["image_urls"] = ['https://library.tarvalon.net' + response.xpath(
            './/a/img[1]/@src').get()]

        yield book_obj

    def get_text(self, node):
        attr = node.xpath('.//a/text()').get()
        if attr is None:
            attr = node.xpath('.//text()').get()

        return attr

    def get_book_abbr(self, book):
        words = book.split(" ")
        first_letters = map(lambda w: w[0].upper(), words)
        return "".join(first_letters)

    def get_chapter_abbr(self, chapter):
        start = 8 if chapter.find("Chapter ") == 0 else 0
        end = len(chapter) if chapter.find(":") == -1 else chapter.find(":")
        return chapter[start:end]
