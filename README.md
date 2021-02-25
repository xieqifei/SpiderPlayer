# FHtmlPlayer

一个音乐播放器的前后端程序，后端采集歌曲链接，音乐前端播放器。适用于Serverless构架。Demo部署于腾讯云函数。

# 1：简介

<img src="https://i.loli.net/2021/02/25/cGLwOmRdDesaFr2.png" alt="image-20210225142758699" style="zoom: 25%;" />

demo：https://y.sci.ci

后端：由Python程序，爬取B站资源，分为搜索结果爬取和音频直链爬取。搜索结果，包括视频名称、时长、bv（每个视频独一无二的id）。音频直链，通过bv构造的链接从返回的网页代码中提取。

前端：基于Mdui库完成界面设计。基于Aplayer播放器拓展音频控制。

# 2：部署说明

前后端程序分别部署到两个云函数中。

1. 创建腾讯云函数，Python版本3+。

2. 后端程序目录为`back`将py文件和其依赖打包为一个zip包，上传腾讯云函数，修改函数入口为`back-api.main_handler`，并添加激活方式为自定义api1，之后需要修改前端程序中的api1。

3. 前端程序放在`front`文件夹下。需要修改`index.html`中的js代码，将`baseUrl`变量改为你后端程序的api1。最后将`index.html`和`player.py`打包成一个zip包，上传到腾讯云函数，并修改入口为`player.main_handler`。激活方式为自定义的api2。

```js
 //请修改为自己的api
  var baseUrl="https://service-if****************ntcs.com/release/music-api";

```



4. 现在你应该可以使用api2打开你的网站了。Enjoy it！