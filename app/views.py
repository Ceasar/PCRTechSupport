import urllib
import urllib2
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *

from recommend import recommend

API = "http://pennapps.com/courses-demo/"
TOKEN = {'token': 'pennappsdemo'}
def api(*args):
  path = "".join((API, "/".join(args), "?", urllib.urlencode(TOKEN)))
  page = urllib2.build_opener().open(path)
  return json.loads(page.read())['result']

def unpack(recommended):
  return [api('course', str(id)) for id in recommended]

def index(request):
  context = {}
  return render_to_response('index.html', context)

def course(request, id):
  context = api('course', id)
  user = request.user
  context['user'] = user
  context['recommended'] = unpack(recommend(request.user)[:5])
  context['reviews'] = api('course', id, 'reviews')
  return render_to_response('course.html', context)

def cart(request):
  context = {}
  user = request.user
  return render_to_response('cart.html', context)

