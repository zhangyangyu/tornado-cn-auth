import tornado.ioloop
import tornado.web
import tornadocnauth.Kaixin

from tornado import gen

class AuthHandler(tornado.web.RequestHandler, tornadocnauth.Kaixin.KaixinMixin):
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_argument('code', None):
            user = yield self.get_authenticated_user(
                redirect_uri='YOUR_REDIRECT_URI',
                client_id=self.settings['kaixin_api_key'],
                client_secret=self.settings['kaixin_api_secret'],
                code=self.get_argument('code'))
            self.render('kaixin.html', user=user)
        else:
            self.authorize_redirect(
                redirect_uri='YOUR_REDIRECT_URI',
                client_id=self.settings['kaixin_api_key']
                )

app = tornado.web.Application([
        ('/', AuthHandler),
        ], kaixin_api_key='YOUR_API_KEY',
                              kaixin_api_secret='YOUR_API_SECRET')

if __name__ == '__main__':
    app.listen(80)
    tornado.ioloop.IOLoop.instance().start()
