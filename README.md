tornado-cn-auth
===============

提供中国主流网站的tornado OAuth扩展

OUTDATED.请不要再使用.Sorry.

介绍
===

提供尽可能类似于`tornado.auth`模块的接口以供接入中国主流网站

每个网站都提供了`authorize_redirect`和`get_authenticated_user`以及相应的request方法,
每个网站`get_authenticated_user`默认都返回用户id,用户名和用户头像(返回并不一致，直接用网站
返回的参数名)。

相关模块内容可参见[tornado.auth文档](http://www.tornadoweb.org/en/stable/auth.html)

安装
===

```bash
pip install tornadocnauth
```

必须先安装[tornado](https://github.com/facebook/tornado)

支持网站
=======

*   [人人](https://github.com/zhangyangyu/tornado-cn-auth#-4)
*   [腾讯](https://github.com/zhangyangyu/tornado-cn-auth#-8)
*   [豆瓣](https://github.com/zhangyangyu/tornado-cn-auth#-10)
*   [新浪微博](https://github.com/zhangyangyu/tornado-cn-auth#-6)
*   [百度](https://github.com/zhangyangyu/tornado-cn-auth#-2)
*   [开心网](https://github.com/zhangyangyu/tornado-cn-auth#-12)

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

腾讯
===

`authorize_redirect`跳转到腾讯授权界面(`redirect_uri`需要在应用中授权)。腾讯在授权时必须传输一个`state`作为状态跟踪标记，
可以为空，默认也为空。

![qq_auth](http://i1345.photobucket.com/albums/p671/zhangyangyu/qq_auth_zpsf68b4bef.png)

`get_authenticated_user`获取`access_token`和`openid`，若想调用腾讯API，则必须先通过`access_token`获取`openid`。
该方法以字典形式返回`openid`, `figureurl`, `nickname`, `access_token`, `session_expires`：

![qq_redirect](http://i1345.photobucket.com/albums/p671/zhangyangyu/ee4ec53b-91db-4ddc-ac05-cced3d88e7ac_zps1423dda4.jpg)

`qq_request`用来调用腾讯API， 应传入 *https://graph.qq.com* 后的相对路径。需要的参数有`access_token`, `openid`,
`client_id`。

相关文档
-------

[OAuth授权](http://wiki.open.qq.com/wiki/website/%E4%BD%BF%E7%94%A8Authorization_Code%E8%8E%B7%E5%8F%96Access_Token)

[API列表](http://wiki.open.qq.com/wiki/website/API%E5%88%97%E8%A1%A8)

豆瓣
===

`authorize_redirect`跳转到豆瓣授权界面(`redirect_uri`需要在应用信息中指定)。

![douban_auth](http://i1345.photobucket.com/albums/p671/zhangyangyu/douban_auth_zps6490de1b.png)

`get_authenticated_user`获取`access_token`，以字典的形式返回`access_token`, `session_expires`, `id`, `uid`,
`name`, `avatar`。

![douban_redirect](http://i1345.photobucket.com/albums/p671/zhangyangyu/douban_redirect_zpsc95c2ee6.png)

`douban_request`用来调用豆瓣API，应传入 *https://api.douban.com/v2* 之后的相对路径。部分豆瓣API不用进行
OAuth认证也可以使用，部分API需要授权，添加`access_token`的Header，并需要在应用设置中选择相应API权限提交审核，
使用`get_authenticated_user`默认至少需要`douban_basic_common`的API权限。

相关文档
-------

[OAuth授权](http://developers.douban.com/wiki/?title=oauth2#server_side_flow)

[API列表](http://developers.douban.com/wiki/?title=api_v2)

开心网
=====

`authorize_redirect`跳转到开心授权界面(`redirect_uri`不要被授权)

![kaixin_auth](http://i1345.photobucket.com/albums/p671/zhangyangyu/kaixin_auth_zpsfbeec889.png)

`get_authenticated_user`获取`access_token`，以字典形式返回`access_token`, `seesion_expires`, `uid`,
`name`, `logo50`。

![kaixin_redirect](http://i1345.photobucket.com/albums/p671/zhangyangyu/kaixin_redirect_zps7a0bb94b.png)

`kaixin_request`用来调用开心API，应传入 *https://api.kaixin001.com* 之后的相对路径。

相关文档
-------

[OAuth授权](http://wiki.open.kaixin001.com/index.php?id=%E4%BD%BF%E7%94%A8Authorization_Code%E8%8E%B7%E5%8F%96Access_Token)

[API列表](http://wiki.open.kaixin001.com/index.php?id=API%E6%96%87%E6%A1%A3)






