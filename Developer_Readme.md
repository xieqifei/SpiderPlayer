# 开发说明

## 1 爬虫文件以及添加新曲库
`\spiders`目录下存放了不同音乐平台的爬虫。
1. Youtube：使用了开源pyfa库获取音频链接，音乐的图片标题id等信息直接从youtube网页中提取。若出现youtube的音乐源无法播放，尝试更新pyfa和youtube-dl库，出现音乐信息不全，尝试修改spiders/Youtube.py中的爬虫程序。音乐需翻墙后才能播放。
2. Bilibili：所有的音乐信息包括音频链接均通过爬虫从网页中获取。
3. QQMusci：音乐资料和音频链接来自第三方接口。

如果添加新的曲库，可参照这三个类重写，并在index.py中注册新的api。同时`cdn/js/functions.js`中查找`searchBox()`在前端页面中添加新的搜索源显示。
tips: 如果音乐的封面图片由于跨域原因无法显示，可在后端转为base64格式替代图片url发送给前端。

## 2 Api调用
云函数的入口函数是`index.py`，前端调用的api都在这个py文件里。



- ⭐所有请求必填参数`src=bilibili`或者`src=youtube`

- 参数为`rc=1`并且`type=recom`时，返回bilibili推荐列表

api请求示例：

> https://y.sci.ci/?src=bilibili&rc=1&type=recom

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

- 参数为`kw=搜索关键词`并且`type=search`，返回搜索结果

api请求示例：

> [https://y.sci.ci/?src=bilibili&kw=明天你好&type=search](https://y.sci.ci/?src=bilibili&kw=%E6%98%8E%E5%A4%A9%E4%BD%A0%E5%A5%BD&type=search)

返回一个json列表：

```json
[{"source": "bilibili", "url": "", "name": "\u3010\u8c2d\u6676\u3011", "artist": "", "cover": "", "id": "BV1ao4y197Fn", "duration": "4:28", "expire": ""}, {"source": "bilibili", "url": "", "name": "\u4e00\u5f00\u53e3\u5c31", "artist": "", "cover": "", "id": "BV1xt4y1B7fr", "duration": "3:14", "expire": ""} ]
```

> 参数说明同上

- 参数为`id=视频id`并且`type=minfo`时，返回该视频对应的音频播放链接和音乐信息。

视频id必须和id来源一一对应。

api请求示例：

> https://y.sci.ci/?src=bilibili&id=BV1hX4y1N7b1&type=minfo

返回一个json字典：

```json
{"source": "bilibili", "url": "https://", "name": "\u3010\u5fc3\u534e", "artist": "\u7687\u752b\u9dc7", "cover": "data:image/b09c83df186411.jpg;base64,/9j/4AAQS~~省略若干~~wUV//Z", "id": "BV1hX4y1N7b1", "duration": "", "expire": "1614786149"}
```

> url：音乐播放链接，链接在expire时间戳对应时间到后失效。
>
> cover：音乐封面，图片如果有防盗链，会返回一个base64编码的字符串，可直接放入img标签src展示。

- 参数为`gd=歌单id`并且`type=playlist`时，返回歌单信息

api示例：

> http://y.sci.ci/?src=qqmusic&gd=7586058175&type=playlist

返回json字典

```json
{"source": "qqmusic", "name": "\u674e\u8363\u6d69", "id": "7586058175", "cover": "https://y.gtimg.cn/mediastyle/global/img/cover_playlist.png?max_age=31536000", "creatername": "\u8bf7\u03b7!", "creatercover": "", "items": [{"source": "qqmusic", "url": "", "name": "Victory", "artist": "Two Steps From Hell", "cover": "https://y.gtimg.cn/music/photo_new/T002R180x180M000002hKKCC1LSc8y.jpg", "id": "001xfrlS0fYS3z", "duration": "", "expire": ""}]}
```

> items：一个列表，每个元素都是一个歌曲信息的字典。

- 参数`lrc=歌曲id`并且`type=lyric`，返回歌词

api示例：

> http://y.sci.ci/?src=qqmusic&lyc=001xfrlS0fYS3z&type=lyric

返回json字典

```json
{"source": "qqmusic", "id": "001xfrlS0fYS3z", "lyric": "[ti:Victory]\n[ar:Two Steps From Hell/Thomas Bergersen]\n[al:Battlecry]\n[by:]\n[offset:0]\n[00:00.00]Victory - Two Steps From Hell (\u4e24\u6b65\u9003\u79bb\u5730\u72f1)/Thomas Bergersen\n[01:20.65]\n[02:41.30]From far away\n[02:43.30]In mountains deep\n[02:45.22]The night of blood\n[02:47.23]In twilight sleep\n[02:49.22]The armies fight\n[02:51.23]For king and queen\n[02:53.24]There will be no\n[02:55.24]No victory\n[02:57.21]The swords collide\n[02:59.30]With power and force\n[03:01.27]As mighty men\n[03:03.26]Show no remorse\n[03:05.26]It is the time\n[03:07.30]The snow is melting\n[03:09.29]It is the time\n[03:11.31]Of reckoning\n[04:17.23]From far away\n[04:19.30]In mountains deep\n[04:21.22]The night of blood\n[04:23.19]In twilight sleep\n[04:25.17]The armies fight\n[04:27.21]For king and queen\n[04:29.21]There will be no\n[04:31.23]No victory\n[04:33.20]The swords collide\n[04:35.27]With power and force\n[04:37.22]As mighty men\n[04:39.25]Show no remorse\n[04:41.21]It is the time\n[04:43.33]The snow is melting\n[04:45.27]It is the time\n[04:47.17]Of reckoning"}
```

- 参数`uid=用户id`并且`type=userlist`，返回此用户下的歌单信息。需要设置qq音乐的cookie，并且只支持qq音乐

api示例：

> http://y.sci.ci/?src=qqmusic&uid=975322731&type=userlist

返回用户歌单json字典

```
{"code": 200, "source": "qqmusic", "uid": "975322731", "creatername": "i can fly", "creatercover": "http://thirdqq.qlogo.cn/g?b=sdk&k=P2k08LYcEYMGx5cqmcJzpQ&s=140&t=1592120904", "playlist": [{"source": "qqmusic", "name": "\u70ed\u6b4c", "id": 7861873582, "cover": "", "creatername": "", "creatercover": "", "items": []}, {"source": "qqmusic", "name": "90\u540e\u56de\u5fc6\u7684\u6b4c", "id": 7737241062, "cover": "", "creatername": "", "creatercover": "", "items": []}]}
```

> code：200表示获取成功，没有或者其他的表示失败
>
> uid：用户id，比如qq号
>
> playlist：一个列表，其中每个元素是一个歌单，歌单字典的格式，见参数为gd时的请求结果说明
- 参数为`songid=音乐id`并且`type=vinfo`，返回音乐的mv信息

- 参数为`vid=视频id`并且`type=vurl`，返回MV的播放地址

- 参数错误，或者无参数

返回json，且状态码为`status_code=400`

```json
{"err_code":1,"err_msg":"query incorrect"}
```

- 其他说明

当设置来源为YouTube时，返回的音乐播放链接需要翻墙才能播放。