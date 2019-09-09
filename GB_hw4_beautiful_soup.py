# HW3 in GeekBrains "Методы сбора и обработки данных из сети Интернет"
#   1) С помощью BeautifulSoup спарсить новости с https://news.yandex.ru по своему региону.
#           * Заголовок
#           * Краткое описание
#           * Ссылка на новость
#   2) * Разбить новости по категориям
#           * Расположить в хронологическом порядке
#
# Category - link link_theme_normal rubric-label rubric-label_top_incident i-bem
# Subject - link link_theme_black i-bem
# Text - story__text
# Date - story__date
#           link link_theme_normal rubric-label rubric-label_top_sport i-bem
#           link link_theme_black i-bem
#


import requests
from bs4 import BeautifulSoup
import re


def request_to_site():
    headers = {
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/76.0.3809.132 Safari/537.36'
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/5.0.342.5 Safari/533.2',
        }
    url = 'https://yandex.kz/news'
    try:
        request = requests.get(url, headers=headers)
        print('Site request status is :', request.status_code)
        print(request.url)
        return request.text
    except requests.exceptions.ConnectionError:
        print('Please check your Internet connection!')
        exit(1)


def parse_html():
    html_doc = request_to_site()
    with open('text.html', 'w') as myfile:
        myfile.write(html_doc)
    soup = BeautifulSoup(html_doc, "html.parser")
    parse_news = soup.findAll('div', {'class': re.compile('^stories-set.*')})
    news_dict = dict()
    print('Number of news is:', len(parse_news))
    counter = 1
    news_dict.setdefault(counter, [])
    for news in parse_news:
        parse_text = news.find_all(text=True)
        current__topic = ''
        current__text = ''
        current__subject = ''
        for i in range(len(parse_text)):
            current_text = parse_text[i]
            current_tag = str(" ".join(parse_text[i].parent.attrs['class']))
            if 'link link_theme_normal rubric-label' in current_tag:
                current__topic = current_text
                current__text = ''
                current__subject = ''
            if current_tag == 'story__text':
                current__text = current_text
            if current_tag == 'link link_theme_black i-bem':
                current__subject = current_text
            if current_tag == 'story__date':
                current__date = current_text.split()[-1]
                current__source = ' '.join(current_text.split()[:-1])
                news_dict.setdefault(counter, [])
                news_dict[counter].append(current__topic)
                news_dict[counter].append(current__text)
                news_dict[counter].append(current__subject)
                news_dict[counter].append(current__date)
                news_dict[counter].append(current__source)
                counter += 1
    return news_dict


def remove_dublicates(dubl_news):
    nondubl_news = dict()
    new_key = 0
    for key, value in dubl_news.items():
        if value not in nondubl_news.values():
            new_key += 1
            nondubl_news[new_key] = value
    return nondubl_news


def categorize_news(uncategorized_news):
    cated_news = dict()
    for key, value in uncategorized_news.items():
        cated_news.setdefault(value[0], [])
        cated_news[value[0]].append(value[0:])

    for key, value in sorted(cated_news.items()):
        print(key, '\n')
        for v_i in value:
            print('\t\t', v_i, '\n')
    return 0


def time_categ_news(untimed_news, rev_direction=False):
    timed_news = dict()
    for key, value in untimed_news.items():
        timed_news.setdefault(value[3], [])
        timed_news[value[3]].append(value)
    for key, value in sorted(timed_news.items(), reverse=rev_direction):
        print(key, '\n')
        for v_i in value:
            print('\t\t', v_i, '\n')
    return 0


obtained_news = parse_html()
unique_news = remove_dublicates(obtained_news)
user_answer = input('Please choose an option Y if need to categorize by topic '
                    'or choose N if need to categorize by time (Y/N):').rstrip()
if user_answer == 'Y' or user_answer == 'y':
    categorize_news(unique_news)
elif user_answer == 'N' or user_answer == 'n':
    time_categ_news(unique_news)
else:
    print('Sorry but your answer cannot be categorized')
