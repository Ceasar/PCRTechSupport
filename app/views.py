from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import *

def index(request):
  return HttpResponse("Index!")

def course(request):
  return HttpResponse("Course")

def cart(request):
  return HttpResponse("Cart!")

