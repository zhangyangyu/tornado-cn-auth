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

class DoubanMixin(OAuth2Mixin):
    _OAUTH_ACCESS_TOKEN_URL = 'https://www.douban.com/service/auth2/token'
    _OAUTH_AUTHORIZE_URL = 'https://www.douban.com/service/auth2/auth?'

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
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, 
                               callback, grant_type='authorization_code', extra_fields=None):
        http = self.get_auth_http_client()
        args = {
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
            }

        fields = set(['id', 'name', 'avatar'])

        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._OAUTH_ACCESS_TOKEN_URL, method="POST",
                   body=urllib_parse.urlencode(args),
                   callback=self.async_callback(self._on_access_token, redirect_uri, 
                                                client_id, client_secret, callback, fields))

    def _oauth_requeset_token_url(self, rediret_uri=None, client_id=None,
                                  client_secret=None, code=None, 
                                  grant_type=None, extra_params=None):
       pass

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                         future, fields, response):
        if response.error:
            future.set_exception(AuthError('Douban auth error %s' % str(response)))
            return

        args = escape.json_decode(escape.native_str(response.body))
        session = {
            'access_token': args['access_token'],
            'expires': args['expires_in'],
            'refresh_token': args['refresh_token'],
            'douban_user_id': args['douban_user_id'],
            }

        self.douban_request(
            path='/user/~me',
            callback=self.async_callback(
                self._on_get_user_info, future, session, fields),
            access_token=session['access_token'],
            )

    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update({'access_token': session['access_token'], 'session_expires': session['expires'], 
                         'douban_user_id': session['douban_user_id']})

        future.set_result(fieldmap)

    @_auth_return_future
    def douban_request(self, path, callback, access_token=None, post_args=None, **args):
        url = "https://api.douban.com/v2" + path
        all_args = {}
        if args:
            all_args.update(args)

        callback = self.async_callback(self._on_douban_request, callback)
        http = self.get_auth_http_client()
        
        if post_args is not None:
            request = httpclient.HTTPRequest(url, method='POST', headers={'Authorization':'Bearer %s' % access_token}, body=urllib_parse.urlencode(post_args))
        elif all_args:
            url += '?' + urllib_parse.urlencode(all_args)
            request = httpclient.HTTPRequest(url, headers={'Authorization':'Bearer %s' % access_token})
        else:
            request = httpclient.HTTPRequest(url, headers={'Authorization':'Bearer %s' % access_token})

        http.fetch(request, callback=callback)

    def _on_douban_request(self, future, response):
        if response.error:
            future.set_exception(AuthError('Error response % fetching %s',
                                           response.error, response.request.url))

            return
        
        future.set_result(escape.json_decode(response.body))

    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()
