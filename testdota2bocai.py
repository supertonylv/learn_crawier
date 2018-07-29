

import requests
import bs4

def get_html(url):
    try:
        r = requests.get(url,timeout=100)
        r.raise_for_status
        r.encoding = ('utf-8')
        return r.text
    except :
        print('Somethine wrong1!')


def get_content(url):
    url_list = []
    html = get_html(url)
    soup = bs4.BeautifulSoup(html,'lxml')

    category_list = soup.find_all('div', class_='index_toplist mright mbottom')

    history_finished_list = soup.find_all('div', class_='index_toplist mbottom')

    for cate in category_list:
        name = cate.find('div',class_='toptab').span.string
        with open('novel_list.csv', 'a+') as f:
            f.write('\n小说种类：{}\n'.format(name))

        general_list = cate.find(style='display: block;')

        book_list = general_list.find_all('li')

        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a') as f:
                f.write('小说名: {:<} \t 小说地址: {:<} \n'.format(title,link))
            
    for cate in history_finished_list:
        name = cate.find('div', class_='toptab').span.string
        with open('novel_list.csv', 'a') as f:
            f.write('\n 小说种类: {}\n'.format(name))
        
        general_list = cate.find(style='display: block;')

        book_list = general_list.find_all('li')
        for book in book_list:
            link = 'http://www.qu.la/' + book.a['href']
            title = book.a['title']
            url_list.append(link)
            with open('novel_list.csv', 'a') as f:
                f.write('小说名: {:<} \t 小说地址: {:<} \n'.format(title,link))

    return url_list

def get_text_url(url):

        url_list = []
        html = get_html(url)
        soup = bs4.BeautifulSoup(html, 'lxml')
        lista = soup.find_all('dd')
        txt_name = soup.find('h1').text
        with open('/Users/lvlu/studio/tmp/Python-crawler/novel/{}.txt'.format(txt_name), 'a+') as f:
            f.write('title of novel: {} \n'.format(txt_name))
            
        for url in lista:
            url_list.append('http://www.qu.la/' + url.a['href'])

        return url_list, txt_name

def get_one_txt(url, txt_name):
        html = get_html(url).replace('<br/>', '\n')
        soup = bs4.BeautifulSoup(html, 'lxml')
        try:
            txt = soup.find('div', id='content').text.replace('chaptererror;', '')
            title = soup.find('title').text

            with open('/Users/lvlu/studio/tmp/Python-crawler/novel/{}.txt'.format(txt_name),'a') as f:
                f.write(title + '\n\n')
                f.write(txt)
                print('current novel : {} current chatper {} downloaded!'.format(txt_name, title))
        except Exception as e:
            print('exception=',e)
            
def get_all_txt(url_list):
        for url in url_list:
            page_list, txt_name = get_text_url(url)

            for page_url in page_list:
                get_one_txt(page_url, txt_name)
                print(' precent {}%'.format(url_list.index(url) / len(url_list) * 100))

def main():
        base_url = 'http://www.qu.la/paihangbang'

        url_list = get_content(base_url)

        url_list = list(set(url_list))
        get_all_txt(url_list)

if __name__ == '__main__':
        main()

    
            