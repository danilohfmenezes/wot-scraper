# -*- coding: utf-8 -*-
import scrapy


class StatisticsSpider(scrapy.Spider):
    name = 'statistics'
    allowed_domains = ['wot.fandom.com']
    start_urls = ['https://wot.fandom.com/wiki/Statistical_analysis']

    def parse(self, response):
        for book in response.xpath('(//h2/span)[position()<last()]'):
            chapters = book.xpath(
                './/following::table[1]/tr[position() > 1]')
            book_name = book.xpath('.//text()').get()
            book_name = book_name.strip()
            book_abbr = self.get_book_abbr(book_name)

            for chapter in chapters:
                attributes = chapter.xpath(".//td")
                if len(attributes) > 3:
                    chapter_name = self.get_text(attributes[0])
                    character = self.get_text(attributes[1])
                    word_count = self.get_text(attributes[2])
                else:
                    character = self.get_text(attributes[0])
                    word_count = self.get_text(attributes[1])

                chapter_name = chapter_name.strip()
                yield {
                    'book': book_name,
                    'book_abbr': book_abbr,
                    'chapter': chapter_name,
                    'chapter_abbr': self.get_chapter_abbr(chapter_name),
                    'character': character.strip(),
                    'word_count': word_count.replace(',', '').strip()
                }

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
        start = 2 if chapter.find("Ch") == 0 else 0
        end = len(chapter) if chapter.find(":") == -1 else chapter.find(":")
        return chapter[start:end]
