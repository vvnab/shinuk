import re
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()

@register.filter
@stringfilter
def infoformat(text):
  text = '<p>' + text + '</p>'
  text = re.sub(r'[\r\n]+ *\r\n', '</p><p>', text)
  text = re.sub(r'<p>(.+)\r\n', '<p><b>\g<1></b><br/>', text)
  text = re.sub(r'\n', '<br/>', text)
  return text

infoformat.is_safe = True
