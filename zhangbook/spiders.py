# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from collections import OrderedDict
from widow.utils.spiders import SpiderHelper
from widow.utils.parsers import SoupHelper
from widow.interfaces.interfaces import BookSpiderInterface
import re

helper = SpiderHelper()
parser = SoupHelper()

class ZhangBookSpider(BookSpiderInterface):
    exclude_before = [
        u'（手机.*com）',
        u'【请务必.*网址】',
        u'【请务必收藏圈子库<[\.]+',
        ]

    exclude_after = [
        u'（手机.*com）',
        u'【请务必.*网址】',
        u'【请务必收藏圈子库<[\.]+',
        u'br/>',
        u'r/>'
    ]
    def get_all_books(self, limit=10, *args, **kwargs):
        books = OrderedDict()
        for page in range(1, limit+1):
            url = lambda  page:\
            "http://zhangbook.com/book/bookTop.aspx?uid=u0&ctg=0&pn=%d&top=1&stype=0&gl=0&st=2" %page
            content = helper.get(url(page), cache=False)
            soup = SoupHelper.get_soup(content)
            tag_as = soup.find_all('a')

            def is_book(href):
                return "book=" in href

            book_url_lambda =lambda book_id: "http://zhangbook.com/book/bookinfo.aspx?book=%s" %book_id

            for tag in tag_as:
                href = tag.attrs.get('href', "")
                if is_book(href):
                    book_name = tag.text
                    m = re.search("book=(\d+)", href)
                    book_id = m.group(1)
                    book_url = book_url_lambda(book_id)
                    books[book_name] = {
                        "name": book_name,
                        "src_name": "ZhangBook",
                        "src_url": book_url,
                        "src_id": book_id
                    }
        return books

    def get_book_detail(self, book_id, cache=False, *args, **kwargs):
        url = lambda x: "http://zhangbook.com/book/bookinfo.aspx?book=%s" %x
        content = helper.get(url(book_id), cache=cache)
        root = SoupHelper.get_root(content)

        book_name_xpath = "./body/wml/card//strong[0]"
        book_score_xpath = "./body/wml/card//a[3]"
        book_chapters_xpath = "./body/wml/card//a[8]"
        description_xpath = "./body/wml/card//br[16]"
        is_over_xpath = "./body/wml/card//br[9]"

        book_name = root.find(book_name_xpath).text
        book_score_tag = root.find(book_score_xpath)
        book_last_chapter_tag = root.find(book_chapters_xpath)
        m = re.search("chapter=(\d+)", book_last_chapter_tag.attrib['href'])
        book_last_chapter = int(m.group(1))
        author_name = root.find('./body/wml/card//postfield').attrib['value']
        description = root.find(description_xpath).tail
        is_over_text = root.find(is_over_xpath).tail

        def see_is_over(is_over_text):
            is_over_m = re.search(":(.*)", is_over_text)
            if not is_over_m:
                return False
            else:
                text = is_over_m.group(1)
            if text == "完成":
                return True
            return False

        is_over = see_is_over(is_over_text)

        score_m = re.search("(\d+)", book_score_tag.text)
        score = int(score_m.group(1)) if score_m else 0

        book_info = {
            "author": author_name,
            "score": score,
            "description": description,
            "is_over": is_over,
        }
        return book_info

    def get_chapters(self, name, book_id="0", start=1, *args, **kwargs):
        if not book_id:
            raise Exception

        book_list_url_lmd = lambda book_id, page: "http://zhangbook.com/book/list.aspx?book=%s&pn=%d" %(book_id,page)
        url = book_list_url_lmd(book_id, page=1)
        content = helper.get(url, cache=False)

        pattern = u"共\d+章,\d+/(\d+)页".encode("utf-8")
        regex = re.compile(pattern)
        page_total = int(regex.search(content).group(1))

        name_pattern = u"\d+章\s*(\S*)\s*"
        name_regex = re.compile(name_pattern)

        number_pattern = "chapter=(\d+)"
        number_regex = re.compile(number_pattern)

        def parse_name(name):
            try:
                cleaned_name = name_regex.search(name).group(1)
            except :
                cleaned_name = name
            return cleaned_name

        def parse_number(chapter_url):
            try:
                number = int(number_regex.search(chapter_url).group(1))
            except:
                number = 0
            return number

        def parse_page_list(url, page=1, cache=True):
            content = helper.get(url, cache=cache)
            root = SoupHelper.get_root(content)

            tag_as = root.findall('.//a')
            chapters = []
            for tag_a in tag_as:
                href = tag_a.attrib.get("href", "")
                if href.startswith("read.aspx"):
                    name = tag_a.text
                    cleaned_name = parse_name(name)
                    chapter_url = "http://zhangbook.com/book/%s" %href
                    number = parse_number(chapter_url)
                    info = {
                        "title": cleaned_name,
                        "number": number,
                        "src_url": chapter_url,
                    }
                    chapters.append(info)
            return chapters

        start_page = max(start, 1)
        for page in range(start_page, page_total+1):
            page_url = book_list_url_lmd(book_id, page)
            if not page == page_total + 1:
                chapters = parse_page_list(page_url, page)
            else:
                chapters = parse_page_list(page_url, page, cache=False)
            for chapter in chapters:
                yield chapter

    def get_chapter_content(self, book_id, number_id, *args, **kwargs):
        url = lambda book_id, chapter:\
        "http://zhangbook.com/book/read.aspx?book=%s&page=1&chapter=%d" %(book_id, chapter)
        query = "./body/wml/card/p//br"
        book_url = url(book_id, number_id)
        content = helper.get(book_url)
        root = SoupHelper.get_root(content)

        tags = root.findall(query)
        contents = [tag.tail for tag in tags if tag.tail]
        page_content = contents[-4]
        pattern = u"共(\d+)页"
        m = re.search(pattern, page_content)
        try:
            page_last = int(m.group(1))
        except:
            return ""

        content = ""
        for page in range(1, page_last+1):
            page_content = self.page_detail(book_id, number_id, page)
            if page_content:
                content = content + "\n" + page_content if content else page_content
        return content

    def page_detail(self, book_id, number_id, page):
        url = lambda book_id, page, chapter:\
        "http://zhangbook.com/book/read.aspx?book=%s&page=%s&chapter=%d" %(book_id, page, chapter)

        query = "./body/wml/card/p//br"
        book_url = url(book_id, page, number_id)
        old_content = helper.get(book_url)
        old_content = old_content.decode("utf-8")
        for exclude_content in self.exclude_before:
            old_content = re.sub(exclude_content, "", old_content)

        root = SoupHelper.get_root(old_content)
        tags = root.findall(query)
        contents_all = [tag.tail for tag in tags if tag.tail]
        contents = contents_all[1:-4] # may be wrong
        content = "\n".join(contents)
        if content.endswith("......"):
            content = content[:-6]

        for after_content in self.exclude_after:
            content = re.sub(after_content, "", content)
        return content