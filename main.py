from selenium import webdriver
from bs4 import BeautifulSoup
from post import Post

pages = ['artificialintelligencememes', 'MemingPhD']

driver = webdriver.Firefox()
driver.implicitly_wait(30)

posts = []

for page in pages:
    url = 'https://mobile.facebook.com/pg/' + page
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.find_all('div', role='article')
    ps = list(map(lambda a: Post(page, a, driver), articles))
    ps = filter(lambda p: p.img_url is not None, ps)
    posts += ps

print(posts)
