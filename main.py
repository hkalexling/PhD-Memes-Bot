from selenium import webdriver
from bs4 import BeautifulSoup
from post import Post
import secrets
import twitter
import requests

t = twitter.Twitter(auth=twitter.OAuth(*secrets.twitter))
t_upload = twitter.Twitter(domain='upload.twitter.com', auth=twitter.OAuth(*secrets.twitter))

def tweet_post(post):
    print('Posting', post.post_id)

    with open('posted_ids.txt', 'r') as f:
        ids = [line.strip() for line in f]
    if post.post_id in ids:
        print('Skipped', post.post_id)
        return
    try:
        imgdata = requests.get(post.img_url).content
        img = t_upload.media.upload(media=imgdata)['media_id_string']
        t.statuses.update(status='From {}\n\nSource: {}'.format(post.source, post.post_url), media_ids=img)

        with open('posted_ids.txt', 'a') as f:
            f.write(post.post_id + '\n')

    except Exception as e:
        print('Failed to tweet post with id {}. Error: {}'.format(post.post_id, e))


pages = {
    'artificialintelligencememes': 'Artificial Intelligence Memes for Artificially Intelligent Teens',
    'MemingPhD': 'High impact PhD memes'
}

driver = webdriver.Firefox()
driver.implicitly_wait(30)

posts = []

for page in pages.keys():
    url = 'https://mobile.facebook.com/pg/' + page
    print('Crawling page', url)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('div', role='article')
    ps = list(map(lambda a: Post(pages[page], a, driver), articles))
    ps = filter(lambda p: p.img_url is not None, ps)
    posts += ps

for post in posts:
    tweet_post(post)
