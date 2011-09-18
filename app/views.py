import urllib
import urllib2
import json
import pickle

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required

from collections import defaultdict
from operator import itemgetter
from math import log
from django.db.models import Sum

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
    depts.append(dept['id'])
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
  context = {'courses': dept_courses(dept)}
  return render_to_response("options.html", context)

@login_required
def index(request):
  context = RequestContext(request, {})
  user = request.user
  context['courses'] = get_depts()
  context['recommended'] = unpack(recommend(user)[:5])
  return render_to_response('index.html', context)

def recommended(request):
  context = {}
  context['courses'] = unpack(recommend(request.user)[:5])
  return render_to_response('recommended.html', context)


def add(request, dept, code):
  try:
    semester, _ = Semester.objects.get_or_create(owner=request.user, defaults={'year': 2011, 'semester': 'F'})
    print "semester", semester
    try:
      int(dept)
    except:
      user = request.user
      name = " ".join([dept, code])
      print 'name', name
      course = Course.objects.get(name=name)
      print 'course', course
      semester.courses.add(course)
    context = {'semester': Semester.objects.get(owner=request.user)}
    return render_to_response('add.html', context)
  except Exception as e:
    print e
    return HttpResponse("%s Failed!" % request.user)



def course(request, *args):
  try:
    id = int(arg[1])
  except:
    #must be a name
    try:
      name = " ".join(request.path[1:-1].split("/")[1:])
      print name
      course = Course.objects.get(name=name)
      print course
    except:
      return HttpResponse("Error!")
    id = course.course_id
  context = RequestContext(request, api('course', str(id)))
  user = request.user
  context['courses'] = get_depts()
  context['user'] = user
  context['recommended'] = unpack(recommend(user)[:5])
  context['reviews'] = api('course', str(id), 'reviews')
  return render_to_response('course.html', context)

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
  user = request.user

  alldata = request.POST['courses']
  data = []
  errors = []
  successes = []
  for line in alldata.split("\n"):
    if line and (line.strip() != "(parsed)"):
      try:
        semester, coursesdata = line.split(":")
        semester = semester.strip()
        courses = []
        for x in coursesdata.split(","):
          try:
            dept, num = x.strip().split()
            courses.append("%s %d" % (dept, int(num)))
          except:
            errors.append("<b>Could not parse course:</b> " + x)
        semester_year = int(semester[:4])
        semester_season = dict(zip('abc','SUF'))[semester[4].lower()]
        data.append((semester_year, semester_season, courses))
      except:
        errors.append("<b>Could not parse line:</b> " + line)

  Semester.objects.filter(owner=user).delete()
  for (year, season, courses) in data:
    found_courses = Course.objects.filter(name__in=courses)
    found_courses_names = [c.name for c in found_courses]
    sem = Semester(owner=user, year=year, semester=season)
    sem.save()
    sem.courses.add(*found_courses)
    sem.save()
    successes.append("<b>Added:</b> (semester %d%s) %s" %
                     (year, season, found_courses_names))
    lost_courses = list(set(courses) - set(found_courses_names))
    if lost_courses:
      errors.append("<b>Could not find courses:</b> (semester %d%s) %s" %
                    (year, season, lost_courses))
    
  return HttpResponse("<br>".join(successes) + "<hr>" + "<br>".join(errors))

@login_required
def recommendations_admin_clear(request):
  CourseLogProb.objects.all().delete()
  return HttpResponse("Recommendation probabilities cleared.")

@login_required
def recommendations_admin_generate(request):
  CourseLogProb.objects.all().delete()
  print "calculating counts"
  counts = defaultdict(int) # predicate
  condcounts = defaultdict(int) # (predicate, given)
  for user in User.objects.all():
    courses = [c.course_id for c in Course.objects.filter(semester__owner=user)]
    for course in courses:
      counts[course] += 1
      for course2 in courses:
        condcounts[course2, course] += 1

  print "filling database (be patient...)"
  n_users = User.objects.count()
  for (course, count) in counts.iteritems():
    CourseLogProb(predicate_cid=course, given_cid=-1,
                  logprob = log(count * 1.0 / n_users)).save()

  for ((course_pred, course_given), count) in condcounts.iteritems():
    CourseLogProb(predicate_cid=course_pred, given_cid=course_given,
                  logprob = log(count * 1.0 / counts[course_given])).save()

  print "done!"
  user = request.user
  mycourses = [c.course_id for c in Course.objects.filter(semester__owner=user)]
  logprobforme = [] # (id, name, prob)
  
  prior_probs = dict((c.predicate_cid, c.logprob)
                     for c in CourseLogProb.objects.filter(given_cid=-1))
  summed_probs = dict((d['given_cid'],d['logprob'])
                      for d in CourseLogProb.objects.filter(predicate_cid__in=mycourses).values('given_cid').annotate(logprob=Sum('logprob')))
  for (idx, course) in enumerate(Course.objects.all()):
    cid = course.course_id
    p0 = prior_probs.get(cid,0)
    ps = summed_probs.get(cid,0)
    logprobforme.append((cid, course.name, p0 + ps))
  mycourses_set = set(mycourses)
  recommendations = sorted(((name, prob) for (cid,name,prob) in logprobforme
                            if cid not in mycourses_set),
                           key=itemgetter(1))[:10]
  return HttpResponse("<br>".join("%s (%f)" % t for t in recommendations))
  
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
