import requests
import bs4

class Movie(object):
    def __init__(self,movie_name,movie_time,movie_url,movie_actor,description,image_url,paihang):
        self.movie_name = movie_name
        self.movie_time = movie_time
        self.movie_url = movie_url
        self.movie_actor = movie_actor
        self.descrition = description
        self.image_url = image_url
        self.paihang = paihang
    
def get_html(url):
    try:
        r = requests.get(url,timeout=30)
        r.raise_for_status
        r.encoding = 'gbk'
        return r.text
    except:
        print(' error ')

def download_image(url, name):
    pic_content = requests.get(url, stream=True).content
    open('/Users/lvlu/dev/data/movie/{}.jpg'.format(name), 'wb+').write(pic_content)

def get_moive_list(url):
    movie_html =  get_html(url)
    soup = bs4.BeautifulSoup(movie_html, 'lxml')
    movie_content = soup.find('ul',attrs={'class': 'picList clearfix'})
    movie_list_content = movie_content.find_all('li')
    movie_list = []
    for movie in movie_list_content:
        image_content = movie.find('div',class_='pic')
        image_url = 'http:'+image_content.img['src']
        movie_name = image_content.img['title']
        download_image(image_url, movie_name)
        paihang = image_content.i.text
        movie_txt = movie.find('div', class_='txt')
        movie_top_html = movie_txt.find('p',class_='pTit')
        movie_tile_html = movie_top_html.find('span',class_='sTit')
        movie_name = movie_tile_html.a.text
        movie_url = movie_tile_html.a['href']
        movie_time = 'not pubish'
        try:
            movie_time = movie_top_html.find('span',class_='sIntro').text
        except:
            print('not publish')
        movie_actors_html = movie_txt.find('p',class_='pActor').find_all('a')
        movie_actors = ''
        for movie_actor_html in movie_actors_html:
            movie_actors = movie_actors + ',' +movie_actor_html.text
        movie_des = movie_txt.find('p', class_='pTxt pIntroShow').text
        movie_list.append(Movie(movie_name,movie_time,movie_url,movie_actors,movie_des,image_url,paihang))
        with open('/Users/lvlu/dev/data/movie/{}.txt'.format(movie_name), 'w+') as f:
            f.write('movie: {}\n'.format(movie_name))
            f.write('time: {} \n'.format(movie_time))
            f.write('actors: {} \n'.format(movie_actors))
            f.write('paihang: {} \n'.format(paihang))
            f.write('image_url: {} \n'.format(image_url))
            f.write('decription: {}\n'.format(movie_des))
    return movie_list

def main():
    url = 'http://dianying.2345.com/top/'
    get_moive_list(url)

if __name__ == '__main__':
    main()