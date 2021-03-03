SpiderPlayer

基于Aplayer播放器和网络爬虫的播放器。海量的免费曲库，本地储存歌单，基于无服务构架，响应式布局。

# 1：简介

![image-20210303142932744](https://i.loli.net/2021/03/03/dZhYX1IvpzLGceS.png)

demo：https://y.sci.ci

曲库：爬虫爬取B站和Youtube资源。

前端：Mdui库开发Web前端页面。

### 特色：

1. 现支持B站和Youtube资源
2. 海量曲库，几乎所有音乐都有
3. 可利用腾讯云函数免费额度，实现完全免费
4. 添加歌曲到收藏，收藏保存到本地，由于浏览器储存限制，一般收藏数量为几十首。
5. 一键播放列表歌曲
6. 退出重进后，自动加载上次的播放列表
7. 支持搜索Youtube播放列表id和播放列表链接

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

4. 你需要一个腾讯云账号。登录后，新建一个腾讯scf云函数。了解云函数https://cloud.tencent.com/product/scf

5. 自定义创建，函数名称随意，地域最好选择中国香港，国内的话添加自定义可能需要域名备案。如果直接使用函数提供的api就无所谓了。

![image-20210227124111666](https://i.loli.net/2021/02/27/KafqnWOzxMRkp1v.png)

6. 函数代码里点击`本地上传zip`，然后点击上传，将步骤3中重新压缩的zip文件传入。

7. 触发器配置选择自定义创建。触发方式，选择`api网关`

![image-20210227124323892](https://i.loli.net/2021/02/27/9lDrgchtbpvdUmL.png)

8. 点击`完成`并在`触发管理`中找到访问路径

![image-20210227124511208](https://i.loli.net/2021/02/27/d39vhuLeEbWVySp.png)

例如：`https://service-q3l564rw-1258461674.hk.apigw.tencentcs.com/release/`

打开后应当有播放器界面了。并且能够听歌，搜歌。

这个网址是否太冗长了？现在添加自定义域名

## 2.2 自定义域名

需要你自己购买了域名，任何域名都可以。无需备案。

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

云函数的入口函数是`index.py`，前端调用的api都在这个py文件里。

如果你想为你的安卓或者桌面应用安装后端api，在项目目录里，有一个名为[back-api.py](https://github.com/xieqifei/SpiderPlayer/blob/main/back-api.py)的python文件，你可以将它部署到你的云函数上，通过api调用，返回推荐列表、搜索结果列表和音乐信息。如果函数入口是`index.py`文件，当没有参数或者参数错误时，会返回html文本，而`back-api.py`没有html返回。

- ⭐所有请求必填参数`src=bilibili`或者`src=youtube`

- 参数为`rc=1`时，返回bilibili推荐列表

api请求示例：

> https://y.sci.ci/?src=bilibili&rc=1

返回一个json列表

```json
[{"source": "bilibili", "url": "", "name": "\u3010\u8c2d\u6676\u3011", "artist": "", "cover": "", "id": "BV1ao4y197Fn", "duration": "4:28", "expire": ""}, {"source": "bilibili", "url": "", "name": "\u4e00\u5f00\u53e3\u5c31", "artist": "", "cover": "", "id": "BV1xt4y1B7fr", "duration": "3:14", "expire": ""} ]
```

> source：音乐来源
>
> url：音乐url
>
> name：音乐名称
>
> artist：歌手，实际上是up主或者youtuber
>
> cover：音乐封面
>
> id：音乐id
>
> duration：时长
>
> expire：音乐url有效时间戳

- 参数为`kw=搜索关键词`，返回搜索结果

api请求示例：

> [https://y.sci.ci/?src=bilibili&kw=明天你好](https://y.sci.ci/?src=bilibili&kw=%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD)

返回一个json列表：

```json
[{"source": "bilibili", "url": "", "name": "\u3010\u8c2d\u6676\u3011", "artist": "", "cover": "", "id": "BV1ao4y197Fn", "duration": "4:28", "expire": ""}, {"source": "bilibili", "url": "", "name": "\u4e00\u5f00\u53e3\u5c31", "artist": "", "cover": "", "id": "BV1xt4y1B7fr", "duration": "3:14", "expire": ""} ]
```

> 参数说明同上

- 参数为`id=视频id`时，返回该视频对应的音频播放链接。

视频id必须和id来源一一对应。bilibili的id和youtubeid不能混用。

api请求示例：

> https://y.sci.ci/?src=bilibili&id=BV1hX4y1N7b1

返回一个json字典：

```json
{"source": "bilibili", "url": "https://upos-hz-mirrorakam.akamaized.net/upgcxcode/32/69/288886932/288886932-1-30232.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1614786149&gen=playurlv2&os=akam&oi=2179117609&trid=1dbccebd1b4c44569ca99e388c8df8bdu&platform=pc&upsig=445e87297a7e81f8f135b49826cc1c0d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&hdnts=exp=1614786149~hmac=68112df0a94503e32ceac091400fc1a57f6c6beb719ba797a2bf53278875469e&mid=0&orderid=0,1&agrr=0&logo=80000000", "name": "\u3010\u5fc3\u534e\u7ffb\u5531\u3011\u660e\u5929\u4f60\u597d\uff08cover\uff1a\u725b\u5976\u5496\u5561\uff09", "artist": "\u7687\u752b\u9dc7", "cover": "data:image/48ad11d1d8a1e8f46cc8924a7db09c83df186411.jpg;base64,/9j/4AAQS~~省略若干~~wUV//Z", "id": "BV1hX4y1N7b1", "duration": "", "expire": "1614786149"}
```

> url：音乐播放链接，链接在expire时间戳对应时间到后失效。
>
> cover：base64编码的up主头像图片。由于图像设有防盗链，直接传图像地址img标签无法加载，而且云函数无法返回文件(二进制代码)，因此通过python程序直接将图像资源转为base64编码格式的字符串。此字符串添加到img标签的src中可以直接显示

- 参数错误，或者无参数

返回json，且状态码为`status_code=400`

```json
{"err_code":1,"err_msg":"query incorrect"}
```

- 其他说明

当设置来源为YouTube时，返回的音乐播放链接需要翻墙才能播放。

# 4：TODO

1. Api签名验证
2. ~~分享~~
3. 下载？看情况吧
4. ~~歌单添加音乐~~
5. 我的收藏里添加分类
6. 主题修改

# 5：受以下开源项目启发

[Aplayer](https://github.com/DIYgod/APlayer)

[Mdui](https://github.com/zdhxiong/mdui)

[Pytube](https://github.com/pytube/pytube)