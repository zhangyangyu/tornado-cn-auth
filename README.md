tornado-cn-auth
===============

提供中国主流网站的tornado OAuth扩展(待完成)

介绍
===

提供类似于`tornado.auth`模块的接口以供接入中国主流网站

每个网站都提供了`authorize_redirect`和`get_authenticated_user`以及相应的request方法,
每个网站`get_authenticated_user`默认都返回用户id,用户名和用户头像。

相关模块内容可参见[tornado.auth文档](http://www.tornadoweb.org/en/stable/auth.html)

支持网站
=======

*   人人
*   腾讯
*   豆瓣
*   新浪微博
*   网易微博
*   搜狐微博
*   百度
*   开心网

百度
===

`authorize_redirect`跳转到百度授权界面(`redirect_uri`必须在应用安全设置中授权，且必须完全一致，差个/都不行)：

![baidu_auth](https://github.com/zhangyangyu/tornado-cn-auth/raw/master/images/baidu_auth.png)

`get_authenticated_user`获取用以API调用的`access_token`,并且用`baidu_request`获取了部分
用户信息。该方法以字典形式返回`access_token`, `session_expires`, `uid`, `uname`, `portrait`，
其中`portrait`已经是绝对路径，而不是百度返回的item序列号：

![baidu_redirect](https://github.com/zhangyangyu/tornado-cn-auth/raw/master/images/baidu_redirect.png)

`baidu_request`用来调用百度API，应输入 *https://openapi.baidu.com* 之后的相对路径，API列表参见相关文档。

相关文档
-------

[OAuth授权](http://developer.baidu.com/wiki/index.php?title=docs/oauth/authorization)

[REST API](http://developer.baidu.com/wiki/index.php?title=docs/oauth/rest/overview)

人人
===

`authorize_redirect`跳转到人人授权界面(`redirect_uri`必须在应用安全设置中授权):

![renren_auth](https://github.com/zhangyangyu/tornado-cn-auth/raw/master/images/renren_auth.png)

`get_authenticated_user`获取`access_token`,并以字典形式返回`access_token`, `session_expires`, `uid`,
`name`, `headurl`：

![renren_redirect](https://github.com/zhangyangyu/tornado-cn-auth/raw/master/images/renren_redirect.png)

`renren_request`用来调用人人API，人人API只能以POST方法调用，应传入`method`参数指定具体API类型，API列表见相关文档

相关文档
-------

[OAuth授权](http://wiki.dev.renren.com/wiki/Authentication)

[API列表](http://wiki.dev.renren.com/wiki/API)





