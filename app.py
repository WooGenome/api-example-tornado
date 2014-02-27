#!/usr/bin/env python
#coding=utf-8
# By Chris (nodexy@gmail)

# 23andme api demo by tornado 

import tornado.ioloop
import tornado.web
from tornado import httpclient
import urllib

PORT = 9190
api_url = "https://api.23andme.com"
api_key = "***"
api_secret = "***"
api_scope = "basic"
api_redirect_url = "http://127.0.0.1:%d/receive_code/" %(PORT)


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><br/><a href="login">Login by 23andme</a></body><br/><br/>23andme api demo by tornado</html>')

class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect(url=api_url+'/authorize/?response_type=code&redirect_uri=%s&client_id=%s&scope=%s' %(api_redirect_url,api_key,api_scope))
        
        
class CallbackHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        code = self.get_argument("code",None)
        if code:
            # TODO:  you'd better check the state argument here 
            #state = self.get_argument('state',None)
            #if ...
            
            params = {
            "client_secret":api_secret,
            "grant_type":"authorization_code",
            "code":code,
            "client_id":api_key,
            "redirect_uri":api_redirect_url,
            }
            request = httpclient.HTTPRequest(
                api_url+'/token/',
                method='POST',
                body=urllib.urlencode(params)
            )
            
            client = httpclient.AsyncHTTPClient()
            client.fetch(request,self._on_finish)
        else:
            self.write("ERROR: code is None!")
            return 
            
    def _on_finish(self,resp):
        print "async OK !"
        self.write('%s'%resp.body)
        self.finish()
        
application = tornado.web.Application([
    (r"/",HomeHandler),
    (r"/login",LoginHandler),
    (r"/receive_code/",CallbackHandler),
],)

if __name__ == "__main__":
    print 'Start server ...  127.0.0.1:%d' %(PORT)
    application.listen(PORT)
    tornado.ioloop.IOLoop.instance().start()
    
#end