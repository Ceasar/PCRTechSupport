from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parseer import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()

@tag(register, [Variable()])
def list(context, list):
  new_context = {'list': list}
  return render_to_string('templates/list.html', new_context)
