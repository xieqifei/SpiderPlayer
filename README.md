SpiderPlayer

基于MKOnlineMusicPlayer和网络爬虫的播放器。海量的免费曲库，本地储存歌单，基于无服务构架，响应式布局。

# 1：简介

![image-20210309235105178](https://i.loli.net/2021/03/10/IB8psHLQERTmjeo.png)

demo：https://y.sci.ci

曲库：Python爬虫爬取B站、Youtube和qq音乐资源。

前端：基于MKOnlineMusicPlayer。


※如果你想发展或学习本项目，请浏览->[开发者文件](https://github.com/xieqifei/SpiderPlayer/Developer_Readme.md)



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

### 2.3.1 自定义首页歌单

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
- 将复制的cookie粘贴到`index.py`中`qqm.set_cookie('')`部分。
- 保存后重新上传到云函数
- cookie有效期比较短，不建议设置。

2. 同步歌单

当cookie设置成功后，在网页 `播放列表`->`点击同步`，输入任意qq号就可以同步qq歌单了。

这里之所以要设置cookie，是因为搜索一个qq的歌单的api，必须使用登录的qq音乐账号才能使用。


# 3：版本特性：

### v2.1

1. 添加QQ音乐支持
2. 支持添加QQ音乐歌单
3. QQ音乐图片http改为https
4. 修复qq音乐歌单音乐播放时图片不显示问题
5. 支持同步qq歌单
6. 修改弹窗样式
7. 支持点击专辑图片播放MV。
8. 修复mv链接为http协议时主站无法嵌入播放问题
9. 优化专辑图片提醒有MV的体验

### v2.0

1. 在MKOnlineMusicPlayer的UI基础上更新功能
2. 修复白色背景虚化后，文字不清晰问题
3. 支持添加youtube播放列表到歌单
4. 保存新添加的歌单到本地
5. 图片转base64，js、css静态资源替换到html代码中
6. 支持添加bilibili播放列表到歌单
7. 修复由于base64图片本地缓存导致浏览器容量超标

### v1.1(功能已废弃)

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


# 4：TODO

2. ~~分享~~
3. ~~下载~~
4. ~~歌单添加音乐~~
6. 主题修改

# 5：鸣谢以下开源项目

[MKOnlineMusicPlayer](https://github.com/mengkunsoft/MKOnlineMusicPlayer)

[Pytube](https://github.com/pytube/pytube)

youtube_dl