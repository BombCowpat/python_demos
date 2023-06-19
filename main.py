import logging
import time
import urllib.parse
import requests
import re
import csv


def get_list():
    url = 'https://m.ting55.com/book/'
    page_id = '10028'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    }
    r = requests.get(url=url + page_id, headers=headers)
    pattern = re.compile('<a class="f" href="/book/(.*?)">.*?</a>', re.S)
    play_list = re.findall(pattern, r.text)

    for i in range(len(play_list)):
        play_list[i] = url + play_list[i]
    return play_list


def get_detail(bookId, page):
    headers_page = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    }
    try:
        detail_url = 'https://m.ting55.com/book/' + bookId + '-' + page
        r_page = requests.get(detail_url, headers=headers_page)
        xt = re.findall(r'name=\"_c\" content=\"(.*?)\"', r_page.text)
    except requests.RequestException:
        logging.error('获取页面失败')
        return

    headers_info = {
        'Connection': 'close',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'mhting55=d14337821065f521; JSESSIONID=3887A0FAADDB3D8886144DEA3228AAC9; __gads=ID=9c3cfafc95056c08-22a20d25b9e100de:T=1687143230:RT=1687164718:S=ALNI_Mbs5_VRDG9lwHGJOVr1FtjvvKf7DQ; __gpi=UID=00000c516ac7db06:T=1687143230:RT=1687164718:S=ALNI_MZlZLTW85fIrbNgATQrzWKGnAMqcA',
        'Referer': 'https://m.ting55.com/book/' + bookId + '-' + page,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Xt': xt[0],
    }
    data = 'bookId=' + bookId + '&isPay=0' + '&page=' + page
    try:
        r_info = requests.post('https://m.ting55.com/glink', headers=headers_info, data=data)
        res = r_info.json()
        title = page + '.' + urllib.parse.unquote(res['title'])
        url = res['url'] + '?v=' + str(round(time.time() * 1000))
        print({
            'title': title,
            'url': url
        })
        download_flag = download(url, title)
        if download_flag == 1:
            page_list.remove(page)
            res_list[int(page) - 1] = [title, url]
            print('下载成功')
    except requests.RequestException:
        logging.error('获取info失败')


def download(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    }
    try:
        res = requests.get(url, headers=headers)
        with open('./mp3/'+filename + '.mp3', 'ab') as file:  # 保存到本地的文件名
            file.write(res.content)
            file.flush()
    except requests.RequestException:
        logging.error('下载失败')
        return 2

    return 1

bookId = '10028'
total = 20
# total = 725
page_list = [0] * total
res_list = [[]] * total


def get_all():
    for i in range(0, total):
        page_list[i] = str(i + 1)

    while len(page_list):
        for page in page_list:
            get_detail(bookId, page)

    with open('./mp3/list.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in res_list:
            writer.writerow(row)


get_all()

# get_detail(bookId, '2')

