from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from django.shortcuts import render_to_response

from .models import Greeting

# Create your views here.
def not_using_right_now(request):
    r = requests.get('http://httpbin.org/status/418')
    print r.text
    return HttpResponse('<pre>' + r.text + '</pre>')
    # return HttpResponse('Hello from Python!')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def index(request):
    url1 = "https://fantasy.icc-cricket.com/loginajax"
    url2 = "https://fantasy.icc-cricket.com/cwc/leagues/view/21387"
    url3 = "https://fantasy.icc-cricket.com/cwc/leagues/get_league_members.json?l_id=21387"
    EMAIL = "sauravraj@outlook.com"
    PASS = "saurav123"

    header = {
        'Host': 'fantasy.icc-cricket.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/41.0.2272.76 Chrome/41.0.2272.76 Safari/537.36',
        'DNT': '1',
        'Referer': 'https://fantasy.icc-cricket.com/cwc/leagues/view/21387',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8'
    }

    s = requests.Session()
    login_data = dict(username=EMAIL, password=PASS)
    req = s.post(url1, data = login_data)
    # print req
    # r = s.get(url2)
    t = s.get(url3, headers=header)
    # r = requests.get(url1, auth=HTTPBasicAuth(EMAIL, PASS))
    # print t.content
    parsed = json.loads(t.content)
    # print parsed
    TG_uid = [254881,298787,295731,162555,161085,143482,496205,317337,244620,493908,179791]
    HG_uid = [225039,248672,298586,491691,233286,493566,230876,180577,164438]
    TG = []
    HG = []
    TG_scores = {254881:23752,298787:25696,295731:26639,162555:25361,161085:25022,143482:22522,496205:17562,317337:24743,244620:22686,493908:17649,179791:23857}
    HG_scores = {225039:24231,248672:28102,298586:23558,491691:15790,233286:25682,493566:16571,230876:26983,180577:20130,164438:24039}

    m = len(TG_uid)
    n = len(HG_uid)
    p = len(parsed['members'])

    for x in xrange(m):
        for y in xrange(p):
            if TG_uid[x] == parsed['members'][y]['u_id']:
                parsed['members'][y]['score'] = parsed['members'][y]['score'] - TG_scores[TG_uid[x]]
                TG.append(parsed['members'][y])

    for x in xrange(n):
        for y in xrange(p):
            if HG_uid[x] == parsed['members'][y]['u_id']:
                parsed['members'][y]['score'] = parsed['members'][y]['score'] - HG_scores[HG_uid[x]]
                HG.append(parsed['members'][y])

    total = [0, 0, 0, 0]

    for i in xrange(m):
        total[0] += TG[i]['score']

    for j in xrange(n):
        total[1] += HG[j]['score']

    total[2] = total[0]/m
    total[3] = total[1]/n
    # for i in xrange(n):
    #     print parsed['members'][i]['f_name']
    #     print parsed['members'][i]['t_name']
    #     print parsed['members'][i]['score']
    #     print parsed['members'][i]['rank']
    #     print "----------------"
    return render_to_response('tghg.html', {'data': parsed['members'], 'tg':TG, 'hg':HG, 'sum': total});