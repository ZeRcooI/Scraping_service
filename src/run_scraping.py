import codecs
from scraping.parsers import *


parsers = (
    (rabota, 'https://nn.rabota.ru/vacancy/?query=Developer%20python'),
    (gorodrabot, 'https://moskva.gorodrabot.ru/python'),
    (superjob, 'https://russia.superjob.ru/vacancy/search/?keywords=Python')
)

jobs, errors = [], []
for func, url in parsers:
    jobs, errors = func(url)
    jobs += jobs
    errors += errors

h = codecs.open('work.txt', 'w', 'utf-8')
h.write(str(jobs))
h.close()