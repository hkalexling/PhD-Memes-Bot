from selenium import webdriver
from bs4 import BeautifulSoup
import json

class Post:
    source = None
    html = None
    post_id = None
    img_url = None
    post_url = None
    driver = None

    def __init__(self, source, html, driver):
        self.driver = driver

        self.source = source
        self.html = html

        try:
            self.post_id = self.get_id()
            self.img_url = self.get_img_url()
            self.post_url = self.get_post_url()
        except Exception:
            return None

    def get_id(self):
        if self.post_id:
            return self.id
        id_str = self.html['data-ft']
        j = json.loads(id_str)
        self.post_id = j.get('mf_story_key')
        return self.post_id

    def get_img_url(self):
        if self.img_url:
            return self.img_url
        img_lst = self.html.find_all('img')
        if len(img_lst) != 1:
            return
        parent = img_lst[0].parent
        if parent.name == 'a':
            href = parent['href']
            self.driver.get('https://mobile.facebook.com' + href)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            full_btn = soup.find('a', text='View full size')
            if full_btn is None:
                full_btn = soup.find('a', text='View Full Size')
            self.img_url = full_btn['href']
            return self.img_url

    def get_post_url(self):
        if self.post_url:
            return self.post_url
        href = self.html.find('a', text='Full Story')['href']
        self.post_url = 'https://mobile.facebook.com' + href
        return self.post_url

    def __str__(self):
        j = {
            'source': self.source,
            'id': self.post_id,
            'img_url': self.img_url,
            'post_url': self.post_url
                }
        return str(j)

    def __repr__(self):
        return str(self)
