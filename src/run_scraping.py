import asyncio
import codecs
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.template.defaulttags import querystring
from django.templatetags.i18n import language

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"


import django
django.setup()
from scraping.parsers import *
from scraping.models import Vacancy, City, Language, Error, Url
User = get_user_model()


parsers = (
    (rabota, 'rabota'),
    (gorodrabot, 'gorodrabot'),
    (superjob, 'superjob'),
)


jobs, errors = [], []
def get_settings():
    queryset = User.objects.filter(send_email=True).values()
    settings_list = set((q['city_id'], q['language_id']) for q in queryset)
    return settings_list


def get_urls(_settings):
    queryset = Url.objects.all().values()
    url_dct = {
        (q['city_id'], q['language_id']): q['url_data'] for q in queryset
    }
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, error  = await loop.run_in_executor(None, func, url, city, language)
    errors.extend(error)
    jobs.extend(job)


settings = get_settings()
url_list = get_urls(settings)


loop = asyncio.get_event_loop()
tmp_task = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_list
             for func, key in parsers]
tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_task])

# for data in url_list:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func(url, city=data['city'], language=data['language'])
#         jobs += j


loop.run_until_complete(tasks)
loop.close()
for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass

if errors:
    er = Error(data=errors).save()


# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()