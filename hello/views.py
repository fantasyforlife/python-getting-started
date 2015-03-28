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
    n = len(parsed['members'])
    # for i in xrange(n):
    #     print parsed['members'][i]['f_name']
    #     print parsed['members'][i]['t_name']
    #     print parsed['members'][i]['score']
    #     print parsed['members'][i]['rank']
    #     print "----------------"
    return render_to_response('tghg.html', {'data': parsed['members']});