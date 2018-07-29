# -*- coding: utf-8 -*-
import scrapy
import codecs
from w3lib.html import remove_tags
from kid_story.items import KidStoryItem


class StorySpider(scrapy.Spider):
    name = 'story'
    allowed_domains = ['gsdaquan.com']
    start_urls = ['http://www.gsdaquan.com/erjiye/tonghua_list.asp?f_id=32&Page=1']

    def parse(self, response):

        xpath_str = '//a[contains(@class, "liebiao")][contains(@href, "th_detail")]/@href'
        current_story_urls = response.xpath(xpath_str).extract()

        # get root url
        final_split_index = response.url.rfind('/')
        root_url = response.url[:final_split_index] + '/'

        for url in current_story_urls:
            page_index = response.url.rfind('Page=')
            page_num = int(response.url[page_index + 5:])
            print 'Page=%d'%page_num, url
            request = scrapy.Request(root_url + url,
                                 callback=self.parse_page)
            yield request

        xpath_str = '//td[contains(@align, "right")][contains(@class, "font10ptblue")]/p/a//text()'
        page_index = response.url.rfind('Page=')
        page_num = int(response.url[page_index + 5:])

        page_indictors = response.xpath(xpath_str).extract()
        if u'尾页' in page_indictors:
            next_page_url = response.url[:page_index] + 'Page=' + str(page_num + 1)

            request_next_page = scrapy.Request(next_page_url,
                                 callback=self.parse)
            yield request_next_page

    def parse_page(self, response):

        # print response.url
        # xpath_str = '//div[contains(@class, "nr_1")]/text()'
        xpath_str = '//*[@id="body_area"]/div[1]/div[5]/div[1]/text()'
        content = '\n'.join(response.xpath(xpath_str).extract())
        # content = self.remove_space(remove_tags(content))

        # xpath_str = '//div[contains(@class, "left_title2")]/text()'
        xpath_str = '//*[@id="body_area"]/div[1]/div[2]/h1/text()'
        title = '\n'.join(response.xpath(xpath_str).extract())
        # title = self.remove_space(remove_tags(title))
        print title

        item = KidStoryItem()
        item['title'] = title
        item['content'] = content
        return item

    def remove_space(self, s):
        return s.replace('\t', '').replace(' ', '')\
                .replace(u'　', '').replace('\r\n\r\n', '\n')






