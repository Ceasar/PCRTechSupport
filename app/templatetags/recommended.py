from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parseer import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()

@tag(register, [Variable()])
def table(context, recommended):
  new_context = {'recommended': recommended}
  return render_to_string('templates/recommended.html', new_context)
