import re
from django import template


def cmp_size(X,Y):
#  XSort = {'XXS': 1, 'XS': 2, 'S': 3, 'M': 4, 'L': 5, 'XL': 6, 'XXL': 7}
  XSort = {'XXS': 1, 'XS': 2, 'S': 3, 'S / M': 4,'M': 5, 'M / L': 6, 'L': 7, 'L / XL': 8, 'XL': 9, 'XXL': 10}
  XSortL = {'Short': 1, 'Reg': 2, 'Long': 3, 'Extra Long': 4}

  if not X['size_ru']: X['size_ru'] = ''
  if not Y['size_ru']: Y['size_ru'] = ''

  x = re.search(r'\d+', X['size_ru'])
  if x:
    x = x.group(0)
    y = re.search(r'\d+', Y['size_ru'])
    if y:
      y = y.group(0)
      if x == y:
        xl = re.search(r'Short|Reg|Long|Extra Long', X['size_ru'])
        if xl:
          yl = re.search(r'Short|Reg|Long|Extra Long', Y['size_ru'])
          if yl:
            return cmp(XSortL[xl.group(0)], XSortL[yl.group(0)])
      return cmp(int(x), int(y))
  x = re.search(r'^XXS|^XXL|^XS|^XL|^L$|^S$|^S / M$|^M$|^M / L$|^L / XL$', X['size_ru'])
  if x:
    y = re.search(r'^XXS|^XXL|^XS|^XL|^L$|^S$|^S / M$|^M$|^M / L$|^L / XL$', Y['size_ru'])
    if y:
      return cmp(XSort[x.group(0)], XSort[y.group(0)])
    else:
      return -1
  return cmp(X['size_ru'], Y['size_ru'])

def cmp_size2(X,Y):
  XSort = {'XXS': 1, 'XS': 2, 'S': 3, 'M': 4, 'L': 5, 'XL': 6, 'XXL': 7}
  XSortL = {'Short': 1, 'Reg': 2, 'Long': 3, 'Extra Long': 4}

  x = re.search(r'\d+', X.size_ru)
  if x:
    x = x.group(0)
    y = re.search(r'\d+', Y.size_ru)
    if y:
      if x == y.group(0):
        xl = re.search(r'Short|Reg|Long|Extra Long', X.size_ru)
        if xl:
          yl = re.search(r'Short|Reg|Long|Extra Long', Y.size_ru)
          if yl:
            return cmp(XSortL[xl.group(0)], XSortL[yl.group(0)])
      y = y.group(0)
      return cmp(int(x), int(y))
  x = re.search(r'XXS|XXL|XS|XL|L|S|M', X.size_ru)
  if x:
    y = re.search(r'XXS|XXL|XS|XL|L|S|M', Y.size_ru)
    if y:
      return cmp(XSort[x.group(0)], XSort[y.group(0)])
  else:
    y = ''
  return cmp(x, y)

register = template.Library()

@register.filter
def ssort(l):
  return sorted(list(l), cmp = cmp_size2)

ssort.is_safe = True
