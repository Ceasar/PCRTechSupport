import urllib
import urllib2
import json
import pickle

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

def get_depts():
  print "getting depts"
  raw_depts = api('depts')
  depts = []
  for dept in raw_depts['values']:
    print dept
    print dept['id']
    depts.append(dept['id'])
    print depts
  return depts

def get_courses():
  print "getting courses"
  try:
    courses = pickle.load(open("coursehistory.p", "r"))
    print "found pickle.."
  except:
    print "no pickle"
    i = 1
    courses = []
    while True:
      print i
      try:
        courses.append(api('coursehistory', str(i)))
      except:
        break
      i += 1
    pickle.dump(courses, open("coursehistory.p", "wb"))
  return courses

def dept_courses(dept):
  raw_data = api('dept', dept)
  courses = []
  for history in raw_data['histories']:
    courses.append(history['name'])
  return courses

def options(request):
  dept = request.GET['dept']
  context = {'courses': [c.name for c in dept_courses(dept)]}
  return render_to_response(options.html, context)

def index(request):
  context = RequestContext(request, {})
  user = request.user
  context['courses'] = get_depts()
  context['recommended'] = unpack(recommend(user)[:5])
  return render_to_response('index.html', context)

def course(request, id):
  context = RequestContext(request, api('course', id))
  user = request.user
  context['courses'] = get_depts()
  context['user'] = user
  context['recommended'] = unpack(recommend(user)[:5])
  context['reviews'] = api('course', id, 'reviews')
  return render_to_response('course.html', context)

@login_required
def cart(request):
  context = {}
  user = request.user
  context['courses'] = get_depts()
  context['user'] = user
  context['recommended'] = unpack(recommend(user)[:5])
  return render_to_response('cart.html', context)

@login_required
def semester(request, year, semester):
  context = {}
  user = request.user
  context['courses'] = get_depts()
  context['user'] = user
  semester = Semester.objects.get(owner=user, year=year, semester=semester)

  context['semester'] = semester
  context['courses'] = unpack([s.course_id for s in semester.courses.all()])
  context['recommended'] = unpack(recommend(user)[:5])
  context = RequestContext(request, context)
  return render_to_response('semester.html', context)


@login_required
def transcript_import(request):
  context = RequestContext(request, {})
  return render_to_response('transcript_import.html', context)

@login_required
def transcript_import_submit(request):
  return HttpResponse(request.POST['courses'])

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
