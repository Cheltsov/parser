from django.shortcuts import render
from django.http import HttpResponse

import requests
from bs4 import BeautifulSoup as BS

# Create your views here.
def index(request):
    max_page = 6
    pages = []
    for x in range(1, max_page + 1):
        pages.append(requests.get('https://stopgame.ru/review/new/stopchoice/p' + str(x)))
    titles = []
    for r in pages:
        html = BS(r.content, 'html.parser')
        for el in html.select('.lent-block'):
            title = el.select('.lent-title > a')
            titles.append(title[0].text)
    return HttpResponse(titles)

def autorize(request):
    s = requests.Session()
    auth_html = s.get('https://smartprogress.do/')
    auth_bs = BS(auth_html.content, 'html.parser')
    csrf = auth_bs.select('input[name=YII_CSRF_TOKEN]')[0]['value']

    payload = {
        'YII_CSRF_TOKEN': csrf,
        'returnUrl': '/',
        'UserLoginForm[email]': 'test54321@test.ru',
        'UserLoginForm[password]': '12345',
        'UserLoginForm[rememberMe]': 1
    }

    answ = s.post('https://smartprogress.do/user/login/', data=payload)
    anw_bs = BS(answ.content, 'html.parser')

    print('имя - ' + anw_bs.select('.user-menu__name')[0].text.strip())
    print('уровень - ' + anw_bs.select('.user-menu__info-text--lvl')[0].text.strip())
    print('опыт - ' + anw_bs.select('.user-menu__info-text--exp')[0].text.strip())

    return HttpResponse('1')
