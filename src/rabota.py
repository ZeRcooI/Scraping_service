import requests
import codecs
from bs4 import BeautifulSoup as BS

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0',
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://nn.rabota.ru/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        main_div = soup.find('div', class_='home-vacancies__infinity-list')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'vacancy-preview-card__top'})
            for div in div_list:
                title = div.find('h3')
                href = title.a['href']
                content = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'}).text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']

                jobs.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': content,
                    'company': company,
                })
        else:
            errors.append({
                'url': url,
                'title': 'Div does not exist',
            })
    else:
        errors.append({
            'url': url,
            'title': 'Page do not response',
        })

    return jobs, errors


def superjob(url):
    jobs = []
    errors = []
    domain = 'https://moskva.gorodrabot.ru/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        main_div = soup.find('div', class_='result-list')
        if main_div:
            div_list = main_div.find_all('div', class_ = 'snippet__inner')
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                content = div.find('div', attrs={'class': 'snippet__desc'}).text
                company = div.find('span', attrs={'class': 'snippet__meta-value'}).text

                a= 1

                jobs.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': content,
                    'company': company,
                })
        else:
            errors.append({
                'url': url,
                'title': 'Div does not exist',
            })
    else:
        errors.append({
            'url': url,
            'title': 'Page do not response',
        })

    return jobs, errors


if __name__ == '__main__':
    url = 'https://moskva.gorodrabot.ru/'
    jobs, errors = superjob(url)
    h = codecs.open('rabota.json', 'w', 'utf-8')
    h.write(str(jobs))
    h.close()
