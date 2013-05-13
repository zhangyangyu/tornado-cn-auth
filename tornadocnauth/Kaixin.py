# -*- coding: utf-8 -*-

from tornado import gen
from tornado import httpclient
from tornado import escape
from tornado.httputil import url_concat
from tornado.concurrent import Future
from tornado.auth import OAuth2Mixin, _auth_return_future, AuthError

try:
    import urlparse  
except ImportError:
    import urllib.parse as urlparse  

try:
    import urllib.parse as urllib_parse  
except ImportError:
    import urllib as urllib_parse  

class KaixinMixin(OAuth2Mixin):
    _OAUTH_ACCESS_TOKEN_URL = 'https://api.kaixin001.com/oauth2/access_token?'
    _OAUTH_AUTHORIZE_URL = 'http://api.kaixin001.com/oauth2/authorize?'

    def authorize_redirect(self, redirect_uri=None, client_id=None, 
                           response_type='code', extra_params=None):
        args = {
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'response_type': response_type,
            }

        if extra_params:
            args.update(extra_params)
        
        self.redirect(url_concat(self._OAUTH_AUTHORIZE_URL, args))

    @_auth_return_future
    def  get_authenticated_user(self, redirect_uri, client_id, client_secret, code,
                                callback, grant_type='authorization_code', extra_fields=None):
        http = self.get_auth_http_client()
        args = {
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
            }

        fields = set(['uid', 'name', 'logo50'])

        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._oauth_request_token_url(**args),
                   self.async_callback(self._on_access_token, redirect_uri, client_id,
                                       client_secret, callback, fields))

    def _oauth_request_token_url(self, redirect_uri=None, client_id=None,
                              client_secret=None, code=None,
                              grant_type=None, extra_params=None):
        url = self._OAUTH_ACCESS_TOKEN_URL
        args = {
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
            }
        
        if extra_params:
            args.update(extra_params)
            
        return url_concat(url, args)

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('Kaixin auth error: %s' % str(response)))
            return 
        
        args = escape.json_decode(escape.native_str(response.body))
        session = {
            'access_token': args['access_token'],
            'expires': args.get('expires_in'),
            'refresh_token': args.get('refresh_token'),
            'scope': args['scope'],
            }

        self.kaixin_request(
            path='/users/me.json',
            callback=self.async_callback(
                self._on_get_user_info, future, session, fields),
            access_token=session['access_token']
            )

    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update({'access_token': session['access_token'], 'session_expires': session.get('expires')})

        future.set_result(fieldmap)

    @_auth_return_future
    def kaixin_request(self, path, callback, access_token=None, 
                       post_args=None, **args):
        url = 'https://api.kaixin001.com' + path
        all_args = {}
        if access_token:
            all_args['access_token'] = access_token
        if args:
            all_args.update(args)

        if all_args:
            url += '?' + urllib_parse.urlencode(all_args)
        callback = self.async_callback(self._on_kaixin_request, callback)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_kaixin_request(self, future, response):
        if response.error:
            future.set_exception(AuthError('Error response %s fetching %s',
                                           response.error, response.request.url))
            return

        future.set_result(escape.json_decode(response.body))

    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()
        

