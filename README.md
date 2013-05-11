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

![baidu_auth](http://i1345.photobucket.com/albums/p671/zhangyangyu/baidu_auth_zps68d9a401.png)

`get_authenticated_user`获取用以API调用的`access_token`,并且用`baidu_request`获取了部分
用户信息。该方法以字典形式返回`access_token`, `session_expires`, `uid`, `uname`, `portrait`，
其中`portrait`已经是绝对路径，而不是百度返回的item序列号：

![baidu_redirect](http://i1345.photobucket.com/albums/p671/zhangyangyu/baidu_redirect_zpsfb3ec87b.png)

`baidu_request`用来调用百度API，应输入 *https://openapi.baidu.com* 之后的相对路径，API列表参见相关文档。

相关文档
-------

[OAuth授权](http://developer.baidu.com/wiki/index.php?title=docs/oauth/authorization)

[REST API](http://developer.baidu.com/wiki/index.php?title=docs/oauth/rest/overview)

人人
===

`authorize_redirect`跳转到人人授权界面(`redirect_uri`必须在应用安全设置中授权):

![renren_auth](http://i1345.photobucket.com/albums/p671/zhangyangyu/renren_auth_zpsc8d4f7a4.png)

`get_authenticated_user`获取`access_token`,并以字典形式返回`access_token`, `session_expires`, `uid`,
`name`, `headurl`：

![renren_redirect](http://i1345.photobucket.com/albums/p671/zhangyangyu/renren_redirect_zpsd4686cc5.png)

`renren_request`用来调用人人API，人人API只能以POST方法调用，应传入`method`参数指定具体API类型，API列表见相关文档。

相关文档
-------

[OAuth授权](http://wiki.dev.renren.com/wiki/Authentication)

[API列表](http://wiki.dev.renren.com/wiki/API)

新浪微博
=======

`authorize_redirect`跳转到微博授权界面(`redirect_uri`必须在应用高级设置中授权)

![weibo_auth](http://i1345.photobucket.com/albums/p671/zhangyangyu/weibo_auth_zpsa3c37561.png)

`get_authenticated_user`获取`access_token`,并以字典的形式返回`id`, `screen_name`,`profile_image_url`,
`access_token`, `session_expires`：

![renren_redirect](http://i1345.photobucket.com/albums/p671/zhangyangyu/weibo_redirect_zps084e7697.png)

`weibo_request`用来调用微博API，应传入 *https://api.weibo.com/2* 后的相对路径，部分API必须用POST方法，除了
`access_token`外，还必须传入`uid`和`screen_name`中的一个，有且仅有一个，API列表参见相关文档。

相关文档
-------

[OAuth授权](http://open.weibo.com/wiki/%E6%8E%88%E6%9D%83%E6%9C%BA%E5%88%B6%E8%AF%B4%E6%98%8E)

[API列表](http://open.weibo.com/wiki/%E5%BE%AE%E5%8D%9AAPI)





