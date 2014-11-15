import os
import re
import urllib
import logging
import urlparse
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template

def guess_charset(data): 
   f = lambda d, enc: d.decode(enc) and enc  
  
   try: return f(data, 'utf-8')  
   except: pass  
   try: return f(data, 'shift-jis')  
   except: pass  
   try: return f(data, 'euc-jp')  
   except: pass  
   try: return f(data, 'iso2022-jp')  
   except: pass  
   return None  

class MainPage(webapp.RequestHandler):
  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, {}))

class PageProxy(webapp.RequestHandler):
  def get(self):
    url=""
    if(self.request.get("url")):
      if re.compile("^\s*http://").match(self.request.get("url")):
        url = self.request.get("url").strip()
      else:
        url = "http://"+self.request.get("url").strip()
    else:
      if 'host' in self.request.cookies:
        if re.compile('image.*').match(self.request.headers['Accept']):
          if self.request.cookies['absolute_path'] == "" or re.compile("^" + self.request.cookies['absolute_path']).match(self.request.path):
            url = self.request.cookies['host'] + self.request.path
          else:
            url = self.request.cookies['host'] + self.request.cookies['absolute_path'] + self.request.path
        else:
          url = self.request.cookies['host'] + self.request.path
    if url!="" :
      result = urlfetch.fetch(url)
      if re.compile('image.*').match(self.request.headers['Accept']):
        if self.request.cookies['img_proxy'] == "false":
          self.response.out.write("")
          return
      else:
        enc=guess_charset(result.content)
        if enc == None or enc == "shift_jis":
          enc="cp932"
        dec_content = result.content.decode(enc)
        enc_content = dec_content.encode("utf_8")
        result.content = re.sub("charset=([a-zA-Z0-9_]*)","charset=UTF-8",enc_content,1)
      parseString=urlparse.urlparse(url)
      if result.status_code == 200:
        for k,v in result.headers.iteritems():
          self.response.headers.add_header(k, v)
        if(self.request.get("url")):
          cookie_val = 'host' + '=' + parseString[0]+"://"+parseString[1] + ";"
          self.response.headers.add_header('Set-Cookie',cookie_val)
          cookie_val = 'absolute_path' + '=' + re.sub("/[^/]*$","",parseString[2]) + ";"
          self.response.headers.add_header('Set-Cookie',cookie_val)
          cookie_val = 'img_proxy' + '=' + self.request.get("img_proxy") + ";"
          self.response.headers.add_header('Set-Cookie',cookie_val)
        self.response.out.write(result.content)
    else:
      self.response.out.write("")

application = webapp.WSGIApplication(
                                     [('/main', MainPage),(r'/[^?]*',PageProxy)],
                                     debug=True)
def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
