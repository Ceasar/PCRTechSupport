import urllib
import urllib2
import json

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required

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
  context['recommended'] = unpack(recommend(user)[:5])
  context['reviews'] = api('course', id, 'reviews')
  return render_to_response('course.html', context)

@login_required
def cart(request):
  context = {}
  user = request.user
  return render_to_response('cart.html', context)

@login_required
def semester(request, year, semester):
  context = {}
  user = request.user
  context['user'] = user
  context['semester'] = Semester.objects.get(owner=user, year=year, semester=semester)
  context['recommended'] = unpack(recommend(user)[:5])
  context = RequestContext(request, context)
  return render_to_response('semester.html', context)

from django.contrib.auth import authenticate, login

def user_login(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(username=username, password=password)
  if user is not None:
    if user.is_active:
      login(request, user)
      # Redirect to a success page.
    else:
      pass
      # Return a 'disabled account' error message
  else:
    pass
    # Return an 'invalid login' error message.
