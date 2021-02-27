SpiderPlayer

基于Aplayer播放器和网络爬虫的播放器。海量的免费曲库，本地储存歌单，基于无服务构架，响应式布局。

# 1：简介

![image-20210227121211210](https://i.loli.net/2021/02/27/dVsSwG3nMY8bBC9.png)

demo：https://y.sci.ci

曲库：音乐曲库来自B站的视频资源，通过爬虫程序直接爬取到b站视频的音频链接。

前端：Mdui库开发Web前端页面。

### 特色：

1. 完全免费的曲库
2. 本地安装无服务框架，可不依赖服务器运行
3. 可利用腾讯云函数免费额度，实现完全免费
4. 添加歌曲到收藏，收藏保存到本地
5. 一键播放全部收藏、推荐歌曲
6. 退出重进后，自动加载上次的播放列表

# 2：部署说明

此项目部署在云函数上，这里只有腾讯云函数的部署教程，其他云函数可能需要修改程序入口函数。

腾讯云函数提供一定的免费资源。对于个人这个量已经远远够了。了解报价：[云函数报价](https://cloud.tencent.com/product/scf/pricing)

| 资源类型   | 每月免费额度 |
| :--------- | :----------- |
| 资源使用量 | 40 万 GBs    |
| 调用次数   | 100 万次     |

## 2.1 SpiderPlayer部署

1. 进入github仓库下载SpiderPlayer库为zip文件。https://github.com/xieqifei/SpiderPlayer

![屏幕截图 2021-02-27 123414](https://i.loli.net/2021/02/27/fuDKBPWAFjYSZtX.png)

2. 解压文件。如果你想修改网站名称和标题，打开`index.html`搜索`SpiderPlayer`。一共两处，修改为你喜欢的名称就可以了。
3. 选中全部文件，重新压缩为zip格式。⭐即使你不修改`index,html`也必须先解压，再选中全部文件重新压缩。

![image-20210227134133413](https://i.loli.net/2021/02/27/aVIjhNsvw7EdnCK.png)

3. 你需要一个腾讯云账号。登录后，新建一个腾讯scf云函数。了解云函数https://cloud.tencent.com/product/scf
4. 自定义创建，函数名称随意，地域最好选择中国香港，国内的话添加自定义可能需要域名备案。如果直接使用函数提供的api就无所谓了。

![image-20210227124111666](https://i.loli.net/2021/02/27/KafqnWOzxMRkp1v.png)

5. 函数代码里点击`本地上传zip`，然后点击上传，将步骤1中下载的zip文件传入。

6. 触发器配置选择自定义创建。触发方式，选择`api网关`

![image-20210227124323892](https://i.loli.net/2021/02/27/9lDrgchtbpvdUmL.png)

7. 点击`完成`并在`触发管理`中找到访问路径

![image-20210227124511208](https://i.loli.net/2021/02/27/d39vhuLeEbWVySp.png)

例如：`https://service-q3l564rw-1258461674.hk.apigw.tencentcs.com/release/`

打开后应当由播放器界面了。并且能够听歌，搜歌。

这个网址是否太冗长了？现在添加自定义域名

## 2.2 自定义域名

1. 点击上图中的`Api服务名`

2. 点击`自定义域名`

![image-20210227124930418](https://i.loli.net/2021/02/27/k9XxHeyDgfT1J83.png)

3. 点击`新建`。填入你的域名信息，支持二级域名。然后到dns服务商那里，设置cname解析，解析地址为你的云函数二级域名，比如下图中给出的：`https://service-q3l564rw-1258461674.hk.apigw.tencentcs.com`

![image-20210227125154565](https://i.loli.net/2021/02/27/3mNFdnVtDcO2vKu.png)

解析完成后，你应当可以通过例如:`http:yourdomain.com/release`来访问你的网站了，

你现在需要将域名进一步缩短，比如直接使用`yourdomain.com`不带路径来访问你的网站。

4. 依次点击`服务`，点击你刚才建的那个api服务的名称

![image-20210227125910994](https://i.loli.net/2021/02/27/TJ3feW29YyPEbmR.png)

5. 点击`编辑`。⭐上一步不能跳过，不然点击`编辑`出来的页面是不一样的。

![image-20210227130044903](https://i.loli.net/2021/02/27/FnKcwArTEkC6uyM.png)

6. 修改路径为`/`

![image-20210227130224442](https://i.loli.net/2021/02/27/JdMT3tVX8fIkjue.png)

保存后即可使用短域名访问你的网站了

# 3：开发说明

1. 前端界面

前端基于mdui。更改样式可学习[Mdui文档](https://www.mdui.org/docs/)

音乐播放器基于Aplayer。修改播放功能，学习[Aplayer文档](https://aplayer.js.org/#/zh-Hans/)

2. 后端api

在项目目录里，有一个名为[back-api.py](https://github.com/xieqifei/SpiderPlayer/blob/main/back-api.py)的python文件，你可以将它部署到你的云函数上，通过api调用，返回推荐列表、搜索结果列表和音乐信息。如果部署`index.py`文件，当没有参数或者参数错误时，会返回html文本，而`back-api.py`没有html返回。参数错误时，会返回错误信息。

- 参数为`rc=1`时，返回推荐列表

api请求示例：

> https://y.sci.ci/?rc=1

返回json格式数据

```json
[{"name": "\u3010\u8c2d\u6676\u3011\u300a\u8d64\u4f36\u300b\u6765\u4e86\uff01\u7ecf\u5178\u541f\u5531\u518d\u73b0\uff0c\u6781\u9650\u58f0\u538b\u642d\u914d\u7edd\u7f8e\u620f\u8154\u5531\u5c3d\u7c89\u58a8\u60b2\u6b22\uff01", "duration": "4:28", "bv": "BV1ao4y197Fn"}, {"name": "\u6c6a\u5cf0Feat.\u5f20\u827a\u5174&amp;GAI\u5468\u5ef6\u300a\u6ca1\u6709\u4eba\u5728\u4e4e\u300b", "duration": "4:33", "bv": "BV1DV411q7dv"}]
```

> name：视频名称
>
> duration：时长
>
> bv：B站视频的id

- 参数为`kw=搜索关键词`，返回搜索结果

api请求示例：

> [https://y.sci.ci/?kw=明天你好](https://y.sci.ci/?kw=明天你好)

返回JSON格式数据：

```json
[{"bvurl": "https://www.bilibili.com/video/BV13s411Z7xk?from=search", "bv": "BV13s411Z7xk", "name": "\u660e\u5929\u4f60\u597d\u2014\u2014\u725b\u5976\u5496\u5561", "duration": "04:29"}, {"bvurl": "https://www.bilibili.com/video/BV19J411N7L5?from=search", "bv": "BV19J411N7L5", "name": "\u300a\u660e\u5929\u4f60\u597d\u300b\u725b\u5976\u5496\u5561\u539f\u58f0\u73b0\u573a\u7248", "duration": "04:25"}]
```

> bvurl：视频链接
>
> name：视频名称
>
> bv：视频id
>
> duration：时长

- 参数为`bv=视频id`时，返回该视频对应的音频播放链接

api请求示例：

> https://y.sci.ci/?bv=BV19J411N7L5

返回json格式数据：

```json
{"url":"https://upos-hz-mirrorakam.akamaized.net/upgcxcode/79/75/116567579/116567579-1-30216.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1614435871&gen=playurlv2&os=akam&oi=2090631651&trid=aaac08032c2840198f006b980da60e95u&platform=pc&upsig=44ca9272ea24c842257094bb7cbcb666&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&hdnts=exp=1614435871~hmac=9f070f7624757a85e5c3850236ba722646d2a3ce7269a5280f9e2cfde8055d7f&mid=0&orderid=0,1&agrr=0&logo=80000000","name":"《明天你好》牛奶咖啡原声现场版","cover":"data:image/ab0e63c58c8c29f4b05c1179cfc5866644e72d8e.jpg;base64,/9j/4AAQSkZJRgABAQAAAQ~~~内容截断~~~ABAAD/4gIoSUNDXqSE3NNUPY47j//2Q==","artist":"張老师不是老师"}
```

> url：音频地址，可直接在aplayer播放器上播放，其他播放器不知道能不能播放，没有防盗链
>
> name：视频名称
>
> cover：base64编码的up主头像图片。由于图像设有防盗链，直接传图像地址img标签无法加载，而且云函数无法返回文件(二进制代码)，因此通过python程序直接将图像资源转为base64编码格式的字符串。此字符串添加到img标签的src中可以直接显示
>
> artist：up主昵称

- 参数错误，或者无参数

返回json，且状态码为`status_code=404`

```json
{'msg':'query incorrect'}
```

# 4：TODO

1. Api签名验证
2. ~~分享~~
3. 下载？看情况吧
4. ~~歌单添加音乐~~
5. 我的收藏里添加分类
6. 主题修改

# 5：项目基于开源

[Aplayer](https://github.com/DIYgod/APlayer)

[Mdui](https://github.com/zdhxiong/mdui)