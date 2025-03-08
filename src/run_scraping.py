import codecs
import os, sys
from django.db import DatabaseError


proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"


import django
django.setup()
from scraping.parsers import *
from scraping.models import Vacancy, City, Language


parsers = (
    (rabota, 'https://www.rabota.ru/vacancy/?query=Developer%20python'),
    (gorodrabot, 'https://moskva.gorodrabot.ru/python'),
    (superjob, 'https://www.superjob.ru/vacancy/search/?keywords=Python&without_resume_send_on_vacancy=1&geo%5Bt%5D%5B0%5D=4&click_from=facet'),
)


city = City.objects.filter(slug='moskva').first()
language = Language.objects.filter(slug='python').first()


jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j


for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass


# h = codecs.open('work.txt', 'w', 'utf-8')
# h.write(str(jobs))
# h.close()