#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ' ERROR '

def get_content(url):
    comments = []
    html = get_html(url)

    soup = BeautifulSoup(html,'lxml')

    liTags = soup.find_all('li', attrs={'class':' j_thread_list clearfix'})

    for li in liTags:
        comment = {}
        try:
            comment['title'] = li.find('a', attrs={'class': 'j_th_tit '}).text.strip()
            comment['link'] = 'http://tieba.baidu.com/' + li.find('a', attrs={'class': 'j_th_tit '})['href']
            autor = li.find('span', attrs={'class': 'tb_icon_author'})
            if autor is None:
               autor = li.find('span', attrs={'class': 'no_icon_author'})
            if autor is not None:
                comment['name'] = autor
            comment['time'] = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()
            comment['replyNum'] = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()
            comments.append(comment)
        except Exception as e:
            print('Exception:',e)

    return comments

def Out2File(dict):

    with open('TTBT.log','a+') as f:
        for comment in dict:
            f.write('title: {} \t link: {} \t author: {} \t time: {} \t replyNum: {} \n'.format(comment['title'],comment['link'],comment['name'],comment['time'],comment['replyNum']))

        print('**********************************************')

def main(base_url, deep):
    url_list = []

    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50*i))
    
    print('download end!')

    for url in url_list:
        content = get_content(url)
        Out2File(content)

    print('save all!')

base_url = 'https://tieba.baidu.com/f?kw=%E5%88%A9%E7%89%A9%E6%B5%A6&ie=utf-8'
deep = 1

if __name__ == '__main__':
    main(base_url,deep)