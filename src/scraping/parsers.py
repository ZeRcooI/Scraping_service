import requests
import codecs
from bs4 import BeautifulSoup as Bs
from random import randint


__all__ = ('rabota', 'gorodrabot', 'superjob')


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},

    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def rabota(url):
    jobs = []
    errors = []
    domain = 'https://www.rabota.ru/'
    response = requests.get(url, headers=headers[randint(0, len(headers) - 1)])
    if response.status_code == 200:
        soup = Bs(response.content, 'html.parser')
        main_div = soup.find('div', class_='infinity-scroll')
        if main_div:
            div_list = main_div.find_all('div', attrs={'class': 'vacancy-preview-card__top'})
            for div in div_list:
                title = div.find('h3')
                href = title.a['href']
                content = div.find('div', attrs={'class': 'vacancy-preview-card__short-description'}).text
                company = 'No name'
                company_block = div.find('span', attrs={'class': 'vacancy-preview-card__company-name'})
                if company_block and company_block.a:
                    company = company_block.a.text.strip()

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


def gorodrabot(url):
    jobs = []
    errors = []
    domain = 'https://moskva.gorodrabot.ru/'
    response = requests.get(url, headers=headers[randint(0, len(headers) - 1)])
    if response.status_code == 200:
        soup = Bs(response.content, 'html.parser')
        main_div = soup.find('div', class_='result-list')
        if main_div:
            div_list = main_div.find_all('div', class_ = 'snippet__inner')
            for div in div_list:
                title = div.find('h2')
                href = title.a['href']
                content = div.find('div', attrs={'class': 'snippet__desc'}).text
                company = div.find('span', attrs={'class': 'snippet__meta-value'}).text

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
    domain = 'https://russia.superjob.ru/'
    response = requests.get(url, headers=headers[randint(0, len(headers) - 1)])
    if response.status_code == 200:
        soup = Bs(response.content, 'html.parser')
        main_div = soup.find('div', class_='MokF1')
        if main_div:
            div_list = main_div.find_all('div', class_ = 'qjjga')
            for div in div_list:
                title = div.find('div', attrs={'class': 'T8ZHO'})
                href = title.a['href']

                content_tag = div.find('span', class_='mOvi3 _2BmV8 OAzFF J1J_3 yqr63')
                content = content_tag.text.strip() if content_tag else "Нет описания"

                company_tag = div.find('span', class_='f-test-text-vacancy-item-company-name')
                company_name = company_tag.a.text.strip() if company_tag and company_tag.a else "Нет компании"

                jobs.append({
                    'title': title.text,
                    'url': domain + href,
                    'description': content,
                    'company': company_name,
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


# if __name__ == '__main__':
#     url = 'https://russia.superjob.ru/vacancy/search/?keywords=Python'
#     jobs, errors = superjob(url)
#     h = codecs.open('rabota.txt', 'w', 'utf-8')
#     h.write(str(jobs))
#     h.close()
