import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1]
    return int(total_pages)

def write_csv(data):
    with open('avito.csv','a') as f:
        writer=csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['url']))
def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
        try:
            title =ad.find('div', class_='description').find('h3').text.strip()
        except:
            title= ''
        try:
            url='www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
        except:
            url= ''
        try:
            price=ad.find('div',class_='about').text.strip()
        except:
            price=''

        data={'title':title,
              'price':price,
               'url':url}
        write_csv(data)

def main():
    url = 'https://www.avito.ru/sankt-peterburg/komnaty?p=2'
    base_url = 'https://www.avito.ru/sankt-peterburg/komnaty?p='
    total_pages = get_total_pages(get_html(url))
    for i in range(1, total_pages):
        url_gen = base_url + str(i)
        html =get_html(url_gen)
        get_page_data(html)
if __name__== '__main__':
    main()