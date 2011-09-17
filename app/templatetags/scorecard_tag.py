from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

register = template.Library()

@tag(register, [])
def scorecard_wiget(context):
  return render_to_string('templates/scorecard/scorecard.html', context)
