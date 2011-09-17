from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parseer import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()

@tag(register, [Variable()])
def table(context, table):
  new_context = {'table': table}
  return render_to_string('templates/course_table.html', new_context)
