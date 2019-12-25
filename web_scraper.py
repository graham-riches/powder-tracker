# -*- coding: utf-8 -*-
"""
@brief
@author: Graham Riches
@date: Sat Dec 21 07:59:33 2019
@description
"""

import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, _url):
        """ initialize a scraper for a specific URL """
        self._url = _url
        self.page = requests.get(self._url)
        self.page_data = BeautifulSoup(self.page.content, 'html.parser')

    def query_by_field(self, field):
        """ query a url by html field """
        data = self.page_data.find(name=field)
        return data

    def query_by_id(self, id_tag):
        """ query a url by an html id """
        data = self.page_data.find(id=id_tag)
        return data


if __name__ == '__main__':
    url = 'https://www.wrh.noaa.gov/mso/avalanche/sagktn.php'
    scraper = WebScraper(url)
    forecast = scraper.query_by_field('pre')
    print(forecast)
