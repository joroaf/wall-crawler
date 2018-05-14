#!/usr/bin/python3

import concurrent.futures
import requests
from bs4 import BeautifulSoup

pages = 10
download_path = 'wallpapers/'

host = 'https://wallpaperscraft.com'
url = host + '/catalog/nature/2560x1440/page'

store_host = 'https://images.wallpaperscraft.com/image/'

cnt = 0
url_stack = []

def get_pages(n):
    num = n
    while num > 0:
        yield url + str(num)
        num -=1

def download(url):
    global cnt
    cnt += 1
    filename = download_path + 'img' + str(cnt) + '.jpg'
    print('Downloading ' + url + ' into ' + filename + ' ...')
    r = requests.get(url, allow_redirects=True)
    with open(filename, 'wb') as f:
        f.write(r.content)
        print('Saved: ' + filename)

if __name__ == "__main__": 
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for page in get_pages(pages):
            r = requests.get(page, allow_redirects=True)
            soup = BeautifulSoup(r.content, 'html.parser')
            for tag in soup.find_all('a', class_='wallpapers__link'):
                img_location = tag['href'][10:]			# remove /download/ from href
                img_location = img_location.replace('/', '_')	# replace / with _ in the link
                url_stack.append(store_host + img_location + '.jpg')
        executor.map(download, url_stack)
