SpiderPlayer

基于MKOnlineMusicPlayer和网络爬虫的播放器。海量的免费曲库，本地储存歌单，基于无服务构架，响应式布局。

# 1：简介

![image-20210309235105178](https://i.loli.net/2021/03/10/IB8psHLQERTmjeo.png)

demo：https://service-qz679lns-1258461674.hk.apigw.tencentcs.com/release/spiderplayer

曲库：Python爬虫爬取B站和Youtube资源。

前端：基于MKOnlineMusicPlayer。

## 更新：

### v2.1

1. 添加QQ音乐支持
2. 支持添加QQ音乐歌单
3. QQ音乐图片http改为https
4. 修复qq音乐歌单音乐播放时图片不显示问题
5. 支持同步qq歌单

### v2.0

1. 在MKOnlineMusicPlayer的UI基础上更新功能
2. 修复白色背景虚化后，文字不清晰问题
3. 支持添加youtube播放列表到歌单
4. 保存新添加的歌单到本地
5. 图片转base64，js、css静态资源替换到html代码中
6. 支持添加bilibili播放列表到歌单
7. 修复由于base64图片本地缓存导致浏览器容量超标

### v1.1

1. 支持在youtube播放列表之前加入自己的域名来构造搜索

> 例：`https://www.youtube.com/playlist?list=PLP4YsIi6aT_Le7Lgzs_JzRRC4LD2OugHa`
>
> 加入自己的播放器url，构造链接为：
>
> `https://y.sci.ci/https://www.youtube.com/playlist?list=PLP4YsIi6aT_Le7Lgzs_JzRRC4LD2OugHa`
>
> 直接返回播放列表搜索结果

2. 修改搜索结果中btn样式
3. 支持点击歌曲名播放
4. 支持下载歌曲

### v1.0

1. 支持B站和Youtube资源
4. 支持添加歌曲到收藏，收藏上限受浏览器限制，在几十首内
5. 支持一键全部播放
4. 支持选中操作
5. 支持退出重进后，自动加载上次的播放列表
6. 支持搜索Youtube播放列表id和播放列表链接


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

## 2.2 域名设置

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

## 2.3 自定义

### 2.3.1 自定义默认歌单

修改和说明都在`/cdn/js/musicList.js`中

### 2.3.2 QQ歌单同步

qq歌单同步需要修改qq音乐的cookie。

1. 获取cookie

- 登录网页版qq音乐，https://y.qq.com/portal/profile.html 
- 在网页里按下`F12`，打开浏览器开发者工具箱
- 点击`console`，输入`document.cookie`回车

![image-20210312000727375](https://i.loli.net/2021/03/12/zKPN1FoLgCVj9kU.png)

如图红色字体为qq登录cookie

- 复制红色字体部分，不包含红色字体外的双引号。
- 修改`spiders/QQMusic.py`里的`cookie =""`为复制的cookie。
- 保存后重新上传到云函数

2. 同步歌单

当cookie设置成功后，在网页 `播放列表`->`点击同步`，输入任意qq号就可以同步qq歌单了。

这里之所以要设置cookie，是因为搜索一个qq的歌单的api，必须使用登录的qq音乐账号才能使用。

# 3：开发说明

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
>
> 以下参数为不一定携带
>
> albummid：id
>
> albumname：专辑名称

- 参数为`kw=搜索关键词`，返回搜索结果

api请求示例：

> [https://y.sci.ci/?src=bilibili&kw=明天你好](https://y.sci.ci/?src=bilibili&kw=%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD)

返回一个json列表：

```json
[{"source": "bilibili", "url": "", "name": "\u3010\u8c2d\u6676\u3011", "artist": "", "cover": "", "id": "BV1ao4y197Fn", "duration": "4:28", "expire": ""}, {"source": "bilibili", "url": "", "name": "\u4e00\u5f00\u53e3\u5c31", "artist": "", "cover": "", "id": "BV1xt4y1B7fr", "duration": "3:14", "expire": ""} ]
```

> 参数说明同上

- 参数为`id=视频id`时，返回该视频对应的音频播放链接。

视频id必须和id来源一一对应。bilibili的id和youtube id不能混用。

api请求示例：

> https://y.sci.ci/?src=bilibili&id=BV1hX4y1N7b1

返回一个json字典：

```json
{"source": "bilibili", "url": "https://", "name": "\u3010\u5fc3\u534e", "artist": "\u7687\u752b\u9dc7", "cover": "data:image/b09c83df186411.jpg;base64,/9j/4AAQS~~省略若干~~wUV//Z", "id": "BV1hX4y1N7b1", "duration": "", "expire": "1614786149"}
```

> url：音乐播放链接，链接在expire时间戳对应时间到后失效。
>
> cover：音乐封面，图片如果有防盗链，会返回一个base64编码的字符串，可直接放入img标签src展示。

- 参数为`gd=歌单id`时，返回歌单

api示例：

> http://y.sci.ci/?src=qqmusic&gd=7586058175

返回json字典

```json
{"source": "qqmusic", "name": "\u674e\u8363\u6d69", "id": "7586058175", "cover": "https://y.gtimg.cn/mediastyle/global/img/cover_playlist.png?max_age=31536000", "creatername": "\u8bf7\u03b7!", "creatercover": "", "items": [{"source": "qqmusic", "url": "", "name": "Victory", "artist": "Two Steps From Hell", "cover": "https://y.gtimg.cn/music/photo_new/T002R180x180M000002hKKCC1LSc8y.jpg", "id": "001xfrlS0fYS3z", "duration": "", "expire": ""}]}
```

> items：一个列表，每个元素都是一个歌曲信息的字典。

- 参数`lrc=歌曲id`，返回歌词

api示例：

> http://y.sci.ci/?src=qqmusic&lyc=001xfrlS0fYS3z

返回json字典

```json
{"source": "qqmusic", "id": "001xfrlS0fYS3z", "lyric": "[ti:Victory]\n[ar:Two Steps From Hell/Thomas Bergersen]\n[al:Battlecry]\n[by:]\n[offset:0]\n[00:00.00]Victory - Two Steps From Hell (\u4e24\u6b65\u9003\u79bb\u5730\u72f1)/Thomas Bergersen\n[01:20.65]\n[02:41.30]From far away\n[02:43.30]In mountains deep\n[02:45.22]The night of blood\n[02:47.23]In twilight sleep\n[02:49.22]The armies fight\n[02:51.23]For king and queen\n[02:53.24]There will be no\n[02:55.24]No victory\n[02:57.21]The swords collide\n[02:59.30]With power and force\n[03:01.27]As mighty men\n[03:03.26]Show no remorse\n[03:05.26]It is the time\n[03:07.30]The snow is melting\n[03:09.29]It is the time\n[03:11.31]Of reckoning\n[04:17.23]From far away\n[04:19.30]In mountains deep\n[04:21.22]The night of blood\n[04:23.19]In twilight sleep\n[04:25.17]The armies fight\n[04:27.21]For king and queen\n[04:29.21]There will be no\n[04:31.23]No victory\n[04:33.20]The swords collide\n[04:35.27]With power and force\n[04:37.22]As mighty men\n[04:39.25]Show no remorse\n[04:41.21]It is the time\n[04:43.33]The snow is melting\n[04:45.27]It is the time\n[04:47.17]Of reckoning"}
```

- 参数`uid=用户id`，返回此用户下的歌单信息

api示例：

> http://y.sci.ci/?src=qqmusic&uid=975322731

返回用户歌单json字典

```
{"code": 200, "source": "qqmusic", "uid": "975322731", "creatername": "i can fly", "creatercover": "http://thirdqq.qlogo.cn/g?b=sdk&k=P2k08LYcEYMGx5cqmcJzpQ&s=140&t=1592120904", "playlist": [{"source": "qqmusic", "name": "\u70ed\u6b4c", "id": 7861873582, "cover": "", "creatername": "", "creatercover": "", "items": []}, {"source": "qqmusic", "name": "90\u540e\u56de\u5fc6\u7684\u6b4c", "id": 7737241062, "cover": "", "creatername": "", "creatercover": "", "items": []}]}
```

> code：200表示获取成功，没有或者其他的表示失败
>
> uid：用户id，比如qq号
>
> playlist：一个列表，其中每个元素是一个歌单，歌单字典的格式，见参数为gd时的请求结果说明

- 参数错误，或者无参数

返回json，且状态码为`status_code=400`

```json
{"err_code":1,"err_msg":"query incorrect"}
```

- 其他说明

当设置来源为YouTube时，返回的音乐播放链接需要翻墙才能播放。

# 4：TODO

2. ~~分享~~
3. ~~下载~~
4. ~~歌单添加音乐~~
6. 主题修改

# 5：鸣谢以下开源项目

[MKOnlineMusicPlayer](https://github.com/mengkunsoft/MKOnlineMusicPlayer)

[Pytube](https://github.com/pytube/pytube)