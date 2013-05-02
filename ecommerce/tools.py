import hmac, binascii, hashlib, time
from django.contrib.auth.models import User

def mac(text, salt):
  return hmac.new(binascii.unhexlify(salt), text, hashlib.sha1).hexdigest()

def nonce(l = 64):
  return User.objects.make_random_password(length = l,  allowed_chars = '0123456789abcdef')

def timestamp(t = None):
  if not t:
    t = time.gmtime()
  return time.strftime('%Y%m%d%H%M%S', t)

def prepstr(s):
  tmp = ''
  for i in s: 
    if i == '':
      tmp += '-'
    else:
      tmp += str(len(str(i))) + str(i)
  return tmp