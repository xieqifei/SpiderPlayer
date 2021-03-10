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
        cover: "data:image/png;base64,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",          // 播放列表封面
        creatorName: "",        // 列表创建者名字
        creatorAvatar: "",      // 列表创建者头像
        item: []
    },  
    // 以上三个系统预留列表请勿更改，否则可能导致程序无法正常运行！
    //*********************************************
    // 自定义列表开始，您可以自由添加您的自定义列表
    
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
    },{
        source: "youtube",
        id: "PLP4YsIi6aT_Le7Lgzs_JzRRC4LD2OugHa"     //youtube播放列表
    }
    // 方式二：直接提供网易云歌单ID
    // {
    //     id: 440103454   // 网易云歌单ID
    // }   // 播放列表的最后一项大括号后面不要加逗号
];