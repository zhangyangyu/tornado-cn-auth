# -*- coding: utf-8 -*-
import re

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

class QQMixin(OAuth2Mixin):
    _OAUTH_ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token?'
    _OAUTH_AUTHORIZE_URL = 'https://graph.qq.com/oauth2.0/authorize?'

    def authorize_redirect(self, redirect_uri=None, client_id=None, 
                           response_type='code', state=None, extra_params=None):
        args = {
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'response_type': response_type,
            'state': state,
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

        fields = set(['nickname', 'figureurl'])

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
                         callback, fields, response):
        if response.error:
            future.set_exception(AuthError('QQ auth error %s' % str(response)))
            return

        args = escape.native_str(response.body).split('&')
        session = {
            'access_token': args[0].split('=')[1],
            'expires': args[1].split('=')[1],
            }

        http = self.get_auth_http_client()
        http.fetch(url_concat('https://graph.qq.com/oauth2.0/me?', {'access_token': session['access_token']}), 
                   self.async_callback(self._on_access_openid, redirect_uri, client_id,
                                       client_secret, session, callback, fields))

    def _on_access_openid(self, redirect_uri, client_id, client_secret, session,
                          future, fields, response):
        if response.error:
            future.set_exception(AuthError('Error response % fetching %s',
                                           response.error, response.request.url))
            return
        
        res = re.search(r'"openid":"([a-zA-Z0-9]+)"', escape.native_str(response.body))

        session['openid'] = res.group(1)
        session['client_id'] = client_id

        self.qq_request(
            path='/user/get_user_info',
            callback=self.async_callback(
                self._on_get_user_info, future, session, fields),
            access_token=session['access_token'],
            openid=session['openid'],
            client_id=session['client_id'],
            )

    def _on_get_user_info(self, future, session, fields, user):
        if user is None:
            future.set_result(None)
            return

        fieldmap = {}
        for field in fields:
            fieldmap[field] = user.get(field)

        fieldmap.update({'access_token': session['access_token'], 'session_expires': session.get('expires'), 
                         'openid': session['openid']})

        future.set_result(fieldmap)

    @_auth_return_future
    def qq_request(self, path, callback, access_token=None, openid=None, client_id=None, 
                   format='json', post_args=None, **args):
        url = 'https://graph.qq.com' + path
        all_args = {}
        if access_token:
            all_args['access_token'] = access_token
        if openid:
            all_args['openid'] = openid
        if client_id:
            all_args['oauth_consumer_key'] = client_id
        if args:
            all_args.update(args)

        if all_args:
            all_args.update({'format': format})
            url += '?' + urllib_parse.urlencode(all_args)
        callback = self.async_callback(self._on_qq_request, callback)
        http = self.get_auth_http_client()
        if post_args is not None:
            http.fetch(url, method="POST", body=urllib_parse.urlencode(post_args),
                       callback=callback)
        else:
            http.fetch(url, callback=callback)

    def _on_qq_request(self, future, response):
        if response.error:
            future.set_exception(AuthError('Error response %s fetching %s', 
                                           response.error, response.request.url))
            return

        future.set_result(escape.json_decode(response.body))

    def get_auth_http_client(self):
        return httpclient.AsyncHTTPClient()
