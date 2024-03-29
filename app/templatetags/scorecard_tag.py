from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

register = template.Library()

class ScoreBox(object):
  def __init__(self, description, number):
    self.number = number
    self.description = description

class ScoreBoxRow(list):
  def __init__(self, title, subtitle, boxes):
    super(ScoreBoxRow, self).__init__(boxes)
    self.title = title
    self.subtitle = subtitle

class ScoreCard(list):
  pass

@tag(register, [])
def scorecard_wiget(context):
  return render_to_string('templates/scorecard.html', context)
