# -*- coding: UTF-8 -*-
""" News Module
"""

from lib import DEBUG
from lib.Web import Web

import xml.dom.minidom
import HTMLParser
import json


class News(object):
    """ News object
    """

    MAX_NEWS = 10
    NEWS_URL = 'http://feeds.foxnews.com/foxnews/latest?format=xml'
    NEWS_FILE = './tests/news.xml'

    number_news = 0

    def __init__(self, number=10):
        """ Constructor
            :param number: The number of news to display
        """
        self.number_news = number

    def get_latest_news(self):
        """ Get the latest news
            :return: string
        """
        if not DEBUG:
            Web.download(
                News.NEWS_URL,
                News.NEWS_FILE
            )

        news = self.get_news()

        return json.dumps(news, sort_keys=True, indent=4)

    def get_news(self):
        """ Get the News
            :return: Dict
        """
        dom_tree = xml.dom.minidom.parse(News.NEWS_FILE)
        collection = dom_tree.documentElement

        html_parser = HTMLParser.HTMLParser()

        xml_document = collection.getElementsByTagName("item")

        current = 0
        items = {}

        for num in range(0, min(self.number_news, News.MAX_NEWS)):

            current += 1

            dom_element = xml_document[num].getElementsByTagName('title')[0]
            text = str(dom_element.firstChild.wholeText)

            items[current] = html_parser.unescape(text)

        return items

