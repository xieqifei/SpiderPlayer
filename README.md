# SpiderPlayer

基于Aplayer播放器和网络爬虫的播放器。海量的免费曲库，本地储存歌单，基于无服务构架，响应式布局。

# 1：简介

![image-20210227121211210](https://i.loli.net/2021/02/27/dVsSwG3nMY8bBC9.png)

demo：https://y.sci.ci

曲库：音乐曲库来自B站的视频资源，通过爬虫程序直接爬取到b站视频的音频链接。

前端：Mdui库开发Web前端页面。更改样式可学习[Mdui库](https://www.mdui.org/docs/)

# 2：部署说明

此项目部署在云函数上，这里只有腾讯云函数的部署教程，其他云函数可能需要修改程序入口函数。

腾讯云函数提供一定的免费资源。对于个人这个量已经远远够了。了解报价：[云函数报价](https://cloud.tencent.com/product/scf/pricing)

| 资源类型   | 每月免费额度 |
| :--------- | :----------- |
| 资源使用量 | 40 万 GBs    |
| 调用次数   | 100 万次     |

1. 你需要一个腾讯云账号。登录后，新建一个腾讯scf云函数。了解云函数https://cloud.tencent.com/product/scf
2. 进入github仓库下载SpiderPlayer库为zip文件。https://github.com/xieqifei/SpiderPlayer



4. 现在你应该可以使用api2打开你的网站了。Enjoy it！

# 3：TODO

1. Api签名验证
2. 分享
3. 下载？看情况吧
4. 歌单添加音乐
5. 我的收藏 分类