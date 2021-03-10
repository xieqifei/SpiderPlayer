/**************************************************
 * MKOnlinePlayer v2.32
 * 播放列表配置模块
 * 编写：mengkun(http://mkblog.cn)
 * 时间：2017-9-15
 *************************************************/
// 建议修改前先备份一下
// 获取 歌曲的网易云音乐ID 或 网易云歌单ID 的方法：
// 先在 js/player.js 中开启调试模式，然后按 F12 打开浏览器的控制台。播放歌曲或点开歌单即可看到相应信息

var musicList = [
    // 以下三个系统预留列表请勿更改，否则可能导致程序无法正常运行！
    // 预留列表：搜索结果
    {
        name: "搜索结果",   // 播放列表名字
        cover: "",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: []
    },
    // 预留列表：正在播放
    {
        name: "正在播放",   // 播放列表名字
        cover: "",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: []
    },
    // 预留列表：播放历史
    {
        name: "播放历史",   // 播放列表名字
        cover: "https://qn.xieqifei.com/spiderplayer/images/history.png",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: []
    },  
    // 以上三个系统预留列表请勿更改，否则可能导致程序无法正常运行！
    //*********************************************
    // 自定义列表开始，您可以自由添加您的自定义列表
    // {
    //     id: 3778678     // 云音乐热歌榜
    // },
    // {
    //     id: 3779629     // 云音乐新歌榜
    // },
    // {
    //     id: 4395559     // 华语金曲榜
    // },
    // {
    //     id: 64016     // 中国TOP排行榜（内地榜）
    // },
    // {
    //     id: 112504     // 中国TOP排行榜（港台榜）
    // },
    // {
    //     id: 19723756     // 云音乐飙升榜
    // },
    // {
    //     id: 2884035     // "网易原创歌曲榜"
    // },
    // 自定义列表教程开始！
    // 方式一：手动创建列表并添加歌曲信息
    // 温馨提示：各大音乐平台获取到的外链有效期均较短，因此 url 值应该设置为空，以让程序临时抓取
    {
        name: "自定义列表",   // 播放列表名字
        cover: "https://p3.music.126.net/34YW1QtKxJ_3YnX9ZzKhzw==/2946691234868155.jpg", // 播放列表封面图像
        creatorName: "",        // 列表创建者名字(暂时没用到，可空)
        creatorAvatar: "",      // 列表创建者头像(暂时没用到，可空)
        item: [                 // 这里面放歌曲
            {
                id: "s5FOS0rffn8",  // 音乐ID
                name: "生生世世愛",  // 音乐名字
                artist: "吳雨霏", // 艺术家名字
                album: "Youtube",    // 专辑名字
                source: "youtube",     // 音乐来源
                url_id: "",  // 链接ID
                pic_id: "",  // 封面ID
                lyric_id: "",  // 歌词ID
                pic: "",    // 专辑图片
                url: ""   // mp3链接（此项建议不填，除非你有该歌曲的比较稳定的外链）
            },
            // 下面演示插入各个平台的音乐。。。
            {
                id: "VN8ZstX7_Vg",
                name: "此生不换",
                artist: "青鳥飛魚",
                album: "Youtube",
                source: "youtube",      
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""
            },
            {
                id: "BV1Rs411f7tJ",
                name: "我的天空",
                artist: "南征北战",
                album: "Bilibili",
                source: "bilibili",      
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""     
            },
            {
                id: "BV1Rx411g7w1",
                name: "成都",
                artist: "赵雷",
                album: "Bilibili",
                source: "bilibili",    // 虾米
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""     
            },
            {
                id: "BV1BW411h7rp",
                name: "小幸运",
                artist: "田馥甄",
                album: "Bilibili",
                source: "bilibili",       
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""    
            },
            {
                id: "BV1hs411D74w",
                name: "走在冷风中",
                artist: "刘思涵",
                album: "Bilibili",
                source: "bilibili",        
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""        
            },{
                id: "BV12W411a7sU",
                name: "恋爱循环",
                artist: "花泽香菜",
                album: "Bilibili",
                source: "bilibili",       
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""         
            },{
                id: "BV1Ft411C7b7",
                name: "素颜",
                artist: "许嵩",
                album: "Bilibili",
                source: "bilibili",        
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""        
            },{
                id: "BV1sJ41127wK",
                name: "父亲写的散文诗",
                artist: "许飞",
                album: "Bilibili",
                source: "bilibili",        
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""        
            },{
                id: "BV1G7411o7qe",
                name: "美丽的神话",
                artist: "成龙、金喜善",
                album: "Bilibili",
                source: "bilibili",        
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""        
            },{
                id: "BV1tx411p7hy",
                name: "稻香",
                artist: "周杰伦",
                album: "Bilibili",
                source: "bilibili",       
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""     
            },{
                id: "BV1ST4y1N7YP",
                name: "青鸟",
                artist: "生物股长",
                album: "Bilibili",
                source: "bilibili",       
                url_id: "",
                pic_id: "",
                lyric_id: "",
                pic: "",
                url: ""        
            }  // 列表中最后一首歌大括号后面不要加逗号
        ]
    }
    // 方式二：直接提供网易云歌单ID
    // {
    //     id: 440103454   // 网易云歌单ID
    // }   // 播放列表的最后一项大括号后面不要加逗号
];