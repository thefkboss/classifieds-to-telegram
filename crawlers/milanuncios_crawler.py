# coding=utf-8

import re

import requests
from bs4 import BeautifulSoup

from crawlers.crawler_base import Crawler
from db.models import Post

id_regex = re.compile('(\d+).htm')


class MilanunciosCrawler(Crawler):
    """
    Crawler specific to gather the information from the web www.milanuncios.com
    """
    crawler_url = 'https://www.milanuncios.com'
    web_type = 'MILANUNCIOS'

    def __init__(self, target_url, *args, **kwargs):
        super(MilanunciosCrawler, self).__init__(*args, **kwargs)
        self.target_url = target_url

    def get_last_posts(self):
        """
        Specific implementation of the generic get_last_posts to gather the last
        post in the web
        :return: [Post]
        """
        last_posts = []
        r = requests.get(self.target_url)
        html = BeautifulSoup(r.content, 'html.parser')
        raw_posts = html.findAll("div", {"class": "aditem-detail-image-container"})

        for post in raw_posts:
            title_element = post.find("a", {"class": "aditem-detail-title"})
            title = title_element.text
            description = post.find("div", {"class": "tx"}).text
            href = title_element['href']
            id_post = id_regex.search(href).group(1)
            type_rent = post.find("div", {"class": "pillDiv"}).text
            price = post.find("div", {"class": "aditem-price"}).text
            image_element = post.find("img", {"class": "ee"})
            image = image_element['src'] if image_element else ''
            other_info = ' '.join([tag.text for tag in post.findAll("div", {"class": "tag-mobile"})])
            description = '\n'.join([title, description, type_rent, other_info, price])
            complete_href = self.crawler_url + href
            last_posts.append(Post(id=id_post, href=complete_href, description=description, image=image))
        return last_posts
