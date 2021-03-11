/**************************************************
 * MKOnlinePlayer v2.4
 * 封装函数及UI交互模块
 * 编写：mengkun(https://mkblog.cn)
 * 时间：2018-3-11
 *************************************************/
// 判断是否是移动设备
var isMobile = {  
    Android: function() {  
        return navigator.userAgent.match(/Android/i) ? true : false;  
    },  
    BlackBerry: function() {  
        return navigator.userAgent.match(/BlackBerry/i) ? true : false;  
    },  
    iOS: function() {  
        return navigator.userAgent.match(/iPhone|iPad|iPod/i) ? true : false;  
    },  
    Windows: function() {  
        return navigator.userAgent.match(/IEMobile/i) ? true : false;  
    },  
    any: function() {
        return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Windows());  
    }
};

$(function(){
    if(mkPlayer.debug) {
        console.warn('播放器调试模式已开启，正常使用时请在 js/player.js 中按说明关闭调试模式');
    }
    
    rem.isMobile = isMobile.any();      // 判断是否是移动设备
    rem.webTitle = document.title;      // 记录页面原本的标题
    rem.errCount = 0;                   // 连续播放失败的歌曲数归零
    
    initProgress();     // 初始化音量条、进度条（进度条初始化要在 Audio 前，别问我为什么……）
    initAudio();    // 初始化 audio 标签，事件绑定
    
    
    if(rem.isMobile) {  // 加了滚动条插件和没加滚动条插件所操作的对象是不一样的
        rem.sheetList = $("#sheet");
        rem.mainList = $("#main-list");
    } else {
        // 滚动条初始化(只在非移动端启用滚动条控件)
        $("#main-list,#sheet").mCustomScrollbar({
            theme:"minimal",
            advanced:{
                updateOnContentResize: true // 数据更新后自动刷新滚动条
            }
        });
        
        rem.sheetList = $("#sheet .mCSB_container");
        rem.mainList = $("#main-list .mCSB_container");  
    }
    
    addListhead();  // 列表头
    addListbar("loading");  // 列表加载中
    
    // 顶部按钮点击处理
    $(".btn").click(function(){
        switch($(this).data("action")) {
            case "player":    // 播放器
                dataBox("player");
            break;
            case "search":  // 搜索
                searchBox();
            break;
            
            case "playing": // 正在播放
                loadList(1); // 显示正在播放列表
            break;
            
            case "sheet":   // 播放列表
                dataBox("sheet");    // 在主界面显示出音乐专辑
            break;
        }
    });
    
    // 列表项双击播放
    $(".music-list").on("dblclick",".list-item", function() {
        var num = parseInt($(this).data("no"));
        if(isNaN(num)) return false;
        listClick(num);
    });
    
    // 移动端列表项单击播放
    $(".music-list").on("click",".list-item", function() {
        if(rem.isMobile) {
            var num = parseInt($(this).data("no"));
            if(isNaN(num)) return false;
            listClick(num);
        }
    });
    
    // 小屏幕点击右侧小点查看歌曲详细信息
    $(".music-list").on("click",".list-mobile-menu", function() {
        var num = parseInt($(this).parent().data("no"));
        musicInfo(rem.dislist, num);
        return false;
    });
    
    // 列表鼠标移过显示对应的操作按钮
    $(".music-list").on("mousemove",".list-item", function() {
        var num = parseInt($(this).data("no"));
        if(isNaN(num)) return false;
        // 还没有追加菜单则加上菜单
        if(!$(this).data("loadmenu")) {
            var target = $(this).find(".music-name");
            var html = '<span class="music-name-cult">' + 
            target.html() + 
            '</span>' +
            '<div class="list-menu" data-no="' + num + '">' +
                '<span class="list-icon icon-play" data-function="play" title="点击播放这首歌"></span>' +
                '<span class="list-icon icon-download" data-function="download" title="点击下载这首歌"></span>' +
                '<span class="list-icon icon-share" data-function="share" title="点击分享这首歌"></span>' +
            '</div>';
            target.html(html);
            $(this).data("loadmenu", true);
        }
    });
    
    // 列表中的菜单点击
    $(".music-list").on("click",".icon-play,.icon-download,.icon-share", function() {
        var num = parseInt($(this).parent().data("no"));
        if(isNaN(num)) return false;
        switch($(this).data("function")) {
            case "play":    // 播放
                listClick(num);     // 调用列表点击处理函数
            break;
            case "download":    // 下载
                ajaxUrl(musicList[rem.dislist].item[num], download);
            break;
            case "share":   // 分享
                // ajax 请求数据
                ajaxUrl(musicList[rem.dislist].item[num], ajaxShare);
            break;
        }
        return true;
    });
    
    // 点击加载更多
    $(".music-list").on("click",".list-loadmore", function() {
        $(".list-loadmore").removeClass('list-loadmore');
        $(".list-loadmore").html('加载中...');
        ajaxSearch();
    });
    
    // 点击专辑显示专辑歌曲
    $("#sheet").on("click",".sheet-cover,.sheet-name", function() {
        var num = parseInt($(this).parent().data("no"));
        // 是用户列表，但是还没有加载数据
        if(musicList[num].item.length === 0 && musicList[num].creatorID) {
            layer.msg('列表读取中...', {icon: 16,shade: 0.01,time: 500}); // 0代表加载的风格，支持0-2
            // ajax加载数据
            ajaxPlayList(musicList[num].id, num,loadList);
            return true;
        }
        loadList(num);
    });
    
    // 点击同步云音乐
    $("#sheet").on("click",".login-in", function() {
        var tmpHtml = '<form onsubmit="return userlistSubmit()"><div id="search-area">' + 
        '    <div class="search-group">' + 
        '        <input type="text" name="uid" id="uid" placeholder="请输入用户号码" autofocus required>' + 
        '        <button class="search-submit" type="submit">添加</button>' + 
        '    </div>' + 
        '    <div class="radio-group" id="list-source">' + 
        '       <label><input type="radio" name="source" value="qqmusic" checked=""> QQ号</label>' + 
        // '       <label><input type="radio" name="source" value="youtube" > Youtube</label>' + 
        // '       <label><input type="radio" name="source" value="bilibili"> B站</label>' + 
        '   </div>' + 
        '</div></form>';
        layer.open({
            type: 1,
            shade: false,
            title: false, // 不显示标题
            shade: 0.5,    // 遮罩颜色深度
            shadeClose: true,
            content: tmpHtml,
            cancel: function(){
            }
        });

        // layer.prompt(
        // {
        //     title: '请输入您的网易云 UID',
        //     // value: '',  // 默认值
        //     btn: ['确定', '取消', '帮助'],
        //     btn3: function(index, layero){
        //         layer.open({
        //             title: '如何获取您的网易云UID？'
        //             ,shade: 0.6 //遮罩透明度
        //             ,anim: 0 //0-6的动画形式，-1不开启
        //             ,content: 
        //             '1、首先<a href="http://music.163.com/" target="_blank">点我(http://music.163.com/)</a>打开网易云音乐官网<br>' +
        //             '2、然后点击页面右上角的“登录”，登录您的账号<br>' + 
        //             '3、点击您的头像，进入个人中心<br>' + 
        //             '4、此时<span style="color:red">浏览器地址栏</span> <span style="color: green">/user/home?id=</span> 后面的<span style="color:red">数字</span>就是您的网易云 UID'
        //         });  
        //     }
        // },
        // function(val, index){   // 输入后的回调函数
        //     if(isNaN(val)) {
        //         layer.msg('uid 只能是数字',{anim: 6});
        //         return false;
        //     }
        //     layer.close(index);     // 关闭输入框
        //     ajaxUserList('qqmusic',val);
        // });
    });

    

    //点击添加播放列表
    $("#sheet").on("click","#add-playlist",function (){
        console.log("点击了添加播放列表")
        var tmpHtml = '<form onsubmit="return playlistSubmit()"><div id="search-area">' + 
        '    <div class="search-group">' + 
        '        <input type="text" name="listid" id="listid" placeholder="输入歌单id" autofocus required>' + 
        '        <button class="search-submit" type="submit">添加</button>' + 
        '    </div>' + 
        '    <div class="radio-group" id="list-source">' + 
        '       <label><input type="radio" name="source" value="qqmusic" checked=""> QQ音乐</label>' + 
        '       <label><input type="radio" name="source" value="youtube" > Youtube</label>' + 
        '       <label><input type="radio" name="source" value="bilibili"> B站</label>' + 
        '   </div>' + 
        '</div></form>';
        layer.open({
            type: 1,
            shade: false,
            title: false, // 不显示标题
            shade: 0.5,    // 遮罩颜色深度
            shadeClose: true,
            content: tmpHtml,
            cancel: function(){
            }
        });
    });
    
   

    // 刷新用户列表
    $("#sheet").on("click",".login-refresh", function() {
        playerSavedata('ulist', '');
        layer.msg('刷新歌单');
        clearUserlist();
    });
    
    // 退出登录
    $("#sheet").on("click",".login-out", function() {
        playerSavedata('uid', '');
        playerSavedata('ulist', '');
        layer.msg('已退出');
        clearUserlist();
    });
    
    // 播放、暂停按钮的处理
    $("#music-info").click(function(){
        if(rem.playid === undefined) {
            layer.msg('请先播放歌曲');
            return false;
        }
        
        musicInfo(rem.playlist, rem.playid);
    });
    
    // 播放、暂停按钮的处理
    $(".btn-play").click(function(){
        pause();
    });
    
    // 循环顺序的处理
    $(".btn-order").click(function(){
        orderChange();
    });
    // 上一首歌
    $(".btn-prev").click(function(){
        prevMusic();
    });
    
    // 下一首
    $(".btn-next").click(function(){
        nextMusic();
    });
    
    // 静音按钮点击事件
    $(".btn-quiet").click(function(){
        var oldVol;     // 之前的音量值
        if($(this).is('.btn-state-quiet')) {
            oldVol = $(this).data("volume");
            oldVol = oldVol? oldVol: (rem.isMobile? 1: mkPlayer.volume);  // 没找到记录的音量，则重置为默认音量
            $(this).removeClass("btn-state-quiet");     // 取消静音
        } else {
            oldVol = volume_bar.percent;
            $(this).addClass("btn-state-quiet");        // 开启静音
            $(this).data("volume", oldVol); // 记录当前音量值
            oldVol = 0;
        }
        playerSavedata('volume', oldVol); // 存储音量信息
        volume_bar.goto(oldVol);    // 刷新音量显示
        if(rem.audio[0] !== undefined) rem.audio[0].volume = oldVol;  // 应用音量
    });
    
    if((mkPlayer.coverbg === true && !rem.isMobile) || (mkPlayer.mcoverbg === true && rem.isMobile)) { // 开启了封面背景
    
        if(rem.isMobile) {  // 移动端采用另一种模糊方案
            $('#blur-img').html('<div class="blured-img" id="mobile-blur"></div><div class="blur-mask mobile-mask"></div>');
        } else {
            // 背景图片初始化
            $('#blur-img').backgroundBlur({
                // imageURL : '', // URL to the image that will be used for blurring
                blurAmount : 50, // 模糊度
                imageClass : 'blured-img', // 背景区应用样式
                overlayClass : 'blur-mask', // 覆盖背景区class，可用于遮罩或额外的效果
                // duration: 0, // 图片淡出时间
                endOpacity : 1 // 图像最终的不透明度
            });
        }
        
        $('.blur-mask').fadeIn(1000);   // 遮罩层淡出
    }
    
    // 图片加载失败处理
    $('img').error(function(){
        $(this).attr('src', 'data:image/png;base64,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');
    });
    
    // 初始化播放列表
    initList(); 
});

//提交歌单搜索
function playlistSubmit(){
    var music = {}
    var listid = $("#listid").val();
    if(!listid) {
        layer.msg('歌单id不能为空', {anim:6, offset: 't'});
        $("#listid").focus();
        return false;
    }
    localid = musicList.length;
    music.id = listid;
    music.source = $("#list-source input[name='source']:checked").val();
    musicList[localid]=JSON.parse(JSON.stringify(music));
    ajaxPlayList(listid,localid,(id)=>{
        addSheet(id,musicList[id].name,musicList[id].cover);
        pushPLintoLocal(musicList[id].source,musicList[id].id);
    });
    layer.closeAll('page');     // 关闭搜索框
    return false;
}

//提交uid搜索
function userlistSubmit(){
    var uid = $("#uid").val();
    if(!uid) {
        layer.msg('用户id不能为空', {anim:6, offset: 't'});
        $("#uid").focus();
        return false;
    }
    source = $("#list-source input[name='source']:checked").val();
    if(isNaN(uid)) {
        layer.msg('uid 只能是数字',{anim: 6});
        return false;
    }
    ajaxUserList(source,uid);
    layer.closeAll('page');     // 关闭搜索框
    return false;
}

//将添加的音乐歌单添加到localstorage
function pushPLintoLocal(src,listid){
    var addedlists = playerReaddata('addedlists')?playerReaddata('addedlists'):[];
    addedlists.push({'source':src,'id':listid});
    playerSavedata('addedlists',addedlists);
}

// 展现系统列表中任意首歌的歌曲信息
function musicInfo(list, index) {
    var music = musicList[list].item[index];
    var tempStr = '<span class="info-title">歌名：</span>' + music.name + 
    '<br><span class="info-title">歌手：</span>' + music.artist + 
    '<br><span class="info-title">专辑：</span>' + music.album;
    
    if(list == rem.playlist && index == rem.playid) {   // 当前正在播放这首歌，那么还可以顺便获取一下时长。。
        tempStr += '<br><span class="info-title">时长：</span>' + formatTime(rem.audio[0].duration);
    }
    
    tempStr += '<br><span class="info-title">操作：</span>' + 
    '<span class="info-btn" onclick="thisDownload(this)" data-list="' + list + '" data-index="' + index + '">下载</span>' + 
    '<span style="margin-left: 10px" class="info-btn" onclick="thisShare(this)" data-list="' + list + '" data-index="' + index + '">外链</span>';
    
    layer.open({
        type: 0,
        shade: false,
        title: false, //不显示标题
        btn: false,
        content: tempStr
    });
    
    if(mkPlayer.debug) {
        console.info('id: "' + music.id + '",\n' + 
        'name: "' + music.name + '",\n' +
        'artist: "' + music.artist + '",\n' +
        'album: "' + music.album + '",\n' +
        'source: "' + music.source + '",\n' +
        'url_id: "' + music.url_id + '",\n' + 
        'pic_id: "' + music.pic_id + '",\n' + 
        'lyric_id: "' + music.lyric_id + '",\n' + 
        'pic: "' + music.pic + '",\n' +
        'url: ""');
        // 'url: "' + music.url + '"');
    }
}

// 展现搜索弹窗
function searchBox() {
    var tmpHtml = '<form onSubmit="return searchSubmit()"><div id="search-area">' + 
    '    <div class="search-group">' + 
    '        <input type="text" name="wd" id="search-wd" placeholder="搜索歌手、歌名、专辑" autofocus required>' + 
    '        <button class="search-submit" type="submit">搜 索</button>' + 
    '    </div>' + 
    '    <div class="radio-group" id="music-source">' + 
    '       <label><input type="radio" name="source" value="qqmusic" checked=""> QQ音乐</label>' + 
    '       <label><input type="radio" name="source" value="youtube"> Youtube</label>' + 
    '       <label><input type="radio" name="source" value="bilibili"> B站</label>' + 
    
    '   </div>' + 
    '</div></form>';
    layer.open({
        type: 1,
        shade: false,
        title: false, // 不显示标题
        shade: 0.5,    // 遮罩颜色深度
        shadeClose: true,
        content: tmpHtml,
        cancel: function(){
        }
    });
    
    // 恢复上一次的输入
    $("#search-wd").focus().val(rem.wd);
    $("#music-source input[name='source'][value='" + rem.source + "']").prop("checked", "checked");
}

// 搜索提交
function searchSubmit() {
    var wd = $("#search-wd").val();
    if(!wd) {
        layer.msg('搜索内容不能为空', {anim:6, offset: 't'});
        $("#search-wd").focus();
        return false;
    }
    rem.source = $("#music-source input[name='source']:checked").val();
    
    layer.closeAll('page');     // 关闭搜索框
    
    rem.loadPage = 1;   // 已加载页数复位
    rem.wd = wd;    // 搜索词
    ajaxSearch();   // 加载搜索结果
    return false;
}

// 下载正在播放的这首歌
function thisDownload(obj) {
    ajaxUrl(musicList[$(obj).data("list")].item[$(obj).data("index")], download);
}

// 分享正在播放的这首歌
function thisShare(obj) {
    ajaxUrl(musicList[$(obj).data("list")].item[$(obj).data("index")], ajaxShare);
}

// 下载歌曲
// 参数：包含歌曲信息的数组
function download(music) {
    if(music.url == 'err' || music.url == "" || music.url == null) {
        layer.msg('这首歌不支持下载');
        return;
    }
    openDownloadDialog(music.url, music.name + ' - ' + music.artist);
}

/**
 * 通用的打开下载对话框方法，没有测试过具体兼容性
 * @param url 下载地址，也可以是一个blob对象，必选
 * @param saveName 保存文件名，可选
 * http://www.cnblogs.com/liuxianan/p/js-download.html
 */
function openDownloadDialog(url, saveName)
{
    if(typeof url == 'object' && url instanceof Blob)
    {
        url = URL.createObjectURL(url); // 创建blob地址
    }
    var aLink = document.createElement('a');
    aLink.href = url;
    aLink.target = "_blank";
    aLink.download = saveName || ''; // HTML5新增的属性，指定保存文件名，可以不要后缀，注意，file:///模式下不会生效
    var event;
    if(window.MouseEvent) event = new MouseEvent('click');
    else
    {
        event = document.createEvent('MouseEvents');
        event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
    }
    aLink.dispatchEvent(event);
}

// 获取外链的ajax回调函数
// 参数：包含音乐信息的数组
function ajaxShare(music) {
    if(music.url == 'err' || music.url == "" || music.url == null) {
        layer.msg('这首歌不支持外链获取');
        return;
    }
    
    var tmpHtml = '<p>' + music.artist + ' - ' + music.name + ' 的外链地址为：</p>' + 
    '<input class="share-url" onmouseover="this.focus();this.select()" value="' + music.url + '">' + 
    '<p class="share-tips">* 获取到的音乐外链有效期较短，请按需使用。</p>';
    
    layer.open({
        title: '歌曲外链分享'
        ,content: tmpHtml
    });
}

// 改变右侧封面图像
// 新的图像地址
function changeCover(music) {
    var img = music.pic;    // 获取歌曲封面
    var animate = false,imgload = false;
    
    if(!img) {  // 封面为空
        ajaxPic(music, changeCover);    // 获取歌曲封面图
        img == "err";    // 暂时用无图像占个位...
    }
    
    if(img == "err") {
        img = "data:image/png;base64,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";
    } else {
        if(mkPlayer.mcoverbg === true && rem.isMobile)      // 移动端封面
        {    
            $("#music-cover").load(function(){
                $("#mobile-blur").css('background-image', 'url("' + img + '")');
            });
        } 
        else if(mkPlayer.coverbg === true && !rem.isMobile)     // PC端封面
        { 
            $("#music-cover").load(function(){
                if(animate) {   // 渐变动画也已完成
                    $("#blur-img").backgroundBlur(img);    // 替换图像并淡出
                    $("#blur-img").animate({opacity:"1"}, 2000); // 背景更换特效
                } else {
                    imgload = true;     // 告诉下面的函数，图片已准备好
                }
                
            });
            
            // 渐变动画
            $("#blur-img").animate({opacity: "0.2"}, 1000, function(){
                if(imgload) {   // 如果图片已经加载好了
                    $("#blur-img").backgroundBlur(img);    // 替换图像并淡出
                    $("#blur-img").animate({opacity:"1"}, 2000); // 背景更换特效
                } else {
                    animate = true;     // 等待图像加载完
                }
            });
        }
    }
    
    $("#music-cover").attr("src", img);     // 改变右侧封面
    $(".sheet-item[data-no='1'] .sheet-cover").attr('src', img);    // 改变正在播放列表的图像
}


// 向列表中载入某个播放列表
function loadList(list) {
    if(musicList[list].isloading === true) {
        layer.msg('列表读取中...', {icon: 16,shade: 0.01,time: 500});
        return true;
    }
    
    rem.dislist = list;     // 记录当前显示的列表
    
    dataBox("list");    // 在主界面显示出播放列表
    
    // 调试信息输出
    if(mkPlayer.debug) {
        if(musicList[list].id) {
            console.log('加载播放列表 ' + list + ' - ' + musicList[list].name + '\n' +
            'id: ' + musicList[list].id + ',\n' +
            'name: "' + musicList[list].name + '",\n' +
            'cover: "' + musicList[list].cover + '",\n' +
            'item: []');
        } else {
            console.log('加载播放列表 ' + list + ' - ' + musicList[list].name);
        }
    }
    
    rem.mainList.html('');   // 清空列表中原有的元素
    addListhead();      // 向列表中加入列表头
    
    if(musicList[list].item.length == 0) {
        addListbar("nodata");   // 列表中没有数据
    } else {
        
        // 逐项添加数据
        for(var i=0; i<musicList[list].item.length; i++) {
            var tmpMusic = musicList[list].item[i];
            
            addItem(i + 1, tmpMusic.name, tmpMusic.artist, tmpMusic.album);
            
            // 音乐链接均有有效期限制,重新显示列表时清空处理
            if(list == 1 || list == 2) tmpMusic.url = "";
        }
        
        // 列表加载完成后的处理
        if(list == 1 || list == 2) {    // 历史记录和正在播放列表允许清空
            addListbar("clear");    // 清空列表
        }
        
        if(rem.playlist === undefined) {    // 未曾播放过
            if(mkPlayer.autoplay == true) pause();  // 设置了自动播放，则自动播放
        } else {
            refreshList();  // 刷新列表，添加正在播放样式
        }
        
        listToTop();    // 播放列表滚动到顶部
    }
}

// 播放列表滚动到顶部
function listToTop() {
    if(rem.isMobile) {
        $("#main-list").animate({scrollTop: 0}, 200);
    } else {
        $("#main-list").mCustomScrollbar("scrollTo", 0, "top");
    }
}

// 向列表中加入列表头
function addListhead() {
    var html = '<div class="list-item list-head">' +
    '    <span class="music-album">' +
    '        专辑' +
    '    </span>' +
    '    <span class="auth-name">' +
    '        歌手' +
    '    </span>' +
    '    <span class="music-name">' +
    '        歌曲' +
    '    </span>' +
    '</div>';
    rem.mainList.append(html);
}

// 列表中新增一项
// 参数：编号、名字、歌手、专辑
function addItem(no, name, auth, album) {
    var html = '<div class="list-item" data-no="' + (no - 1) + '">' +
    '    <span class="list-num">' + no + '</span>' +
    '    <span class="list-mobile-menu"></span>' +
    '    <span class="music-album">' + album + '</span>' +
    '    <span class="auth-name">' + auth + '</span>' +
    '    <span class="music-name">' + name + '</span>' +
    '</div>'; 
    rem.mainList.append(html);
}

// 加载列表中的提示条
// 参数：类型（more、nomore、loading、nodata、clear）
function addListbar(types) {
    var html
    switch(types) {
        case "more":    // 还可以加载更多
            html = '<div class="list-item text-center list-loadmore list-clickable" title="点击加载更多数据" id="list-foot">点击加载更多...</div>';
        break;
        
        case "nomore":  // 数据加载完了
            html = '<div class="list-item text-center" id="list-foot">全都加载完了</div>';
        break;
        
        case "loading": // 加载中
            html = '<div class="list-item text-center" id="list-foot">播放列表加载中...</div>';
        break;
        
        case "nodata":  // 列表中没有内容
            html = '<div class="list-item text-center" id="list-foot">可能是个假列表，什么也没有</div>';
        break;
        
        case "clear":   // 清空列表
            html = '<div class="list-item text-center list-clickable" id="list-foot" onclick="clearDislist();">清空列表</div>';
        break;
    }
    rem.mainList.append(html);
}

// 将时间格式化为 00:00 的格式
// 参数：原始时间
function formatTime(time){    
	var hour,minute,second;
	hour = String(parseInt(time/3600,10));
	if(hour.length == 1) hour='0' + hour;
	
	minute=String(parseInt((time%3600)/60,10));
	if(minute.length == 1) minute='0'+minute;
	
	second=String(parseInt(time%60,10));
	if(second.length == 1) second='0'+second;
	
	if(hour > 0) {
	    return hour + ":" + minute + ":" + second;
	} else {
	    return minute + ":" + second;
	}
}

// url编码
// 输入参数：待编码的字符串
function urlEncode(String) {
    return encodeURIComponent(String).replace(/'/g,"%27").replace(/"/g,"%22");	
}

// 在 ajax 获取了音乐的信息后再进行更新
// 参数：要进行更新的音乐
function updateMinfo(music) {
    // 不含有 id 的歌曲无法更新
    if(!music.id) return false;
    
    // 循环查找播放列表并更新信息
    for(var i=0; i<musicList.length; i++) {
        for(var j=0; j<musicList[i].item.length; j++) {
            // ID 对上了，那就更新信息
            if(musicList[i].item[j].id == music.id && musicList[i].item[j].source == music.source) {
                musicList[i].item[j] == music;  // 更新音乐信息
                j = musicList[i].item.length;   // 一个列表中只找一首，找到了就跳出
            }
        }
    }
}

// 刷新当前显示的列表，如果有正在播放则添加样式
function refreshList() {
    // 还没播放过，不用对比了
    if(rem.playlist === undefined) return true;
    
    $(".list-playing").removeClass("list-playing");        // 移除其它的正在播放
    
    if(rem.paused !== true) {   // 没有暂停
        for(var i=0; i<musicList[rem.dislist].item.length; i++) {
            // 与正在播放的歌曲 id 相同
            if((musicList[rem.dislist].item[i].id !== undefined) && 
              (musicList[rem.dislist].item[i].id == musicList[1].item[rem.playid].id) && 
              (musicList[rem.dislist].item[i].source == musicList[1].item[rem.playid].source)) {
                $(".list-item[data-no='" + i + "']").addClass("list-playing");  // 添加正在播放样式
                
                return true;    // 一般列表中只有一首，找到了赶紧跳出
            }
        }
    }
    
}
// 添加一个歌单
// 参数：编号、歌单名字、歌单封面
function addSheet(no, name, cover) {
    if(!cover) cover = "data:image/png;base64,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";
    if(!name) name = "读取中...";
    
    var html = '<div class="sheet-item" data-no="' + no + '">' +
    '    <img class="sheet-cover" src="' +cover+ '">' +
    '    <p class="sheet-name">' +name+ '</p>' +
    '</div>'; 
    $('#add-playlist').before(html);
}


//添加“添加歌单”按钮
function addPlaylistBtn(){
    //base64格式的图片
    var cover = "data:image/png;base64,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";
    var name = "添加歌单";
    var html = '<div class="sheet-item" id="add-playlist" >' +
    '    <img class="sheet-addBtn" src="' +cover+ '">' +
    '    <p class="sheet-name">' +name+ '</p>' +
    '</div>'; 
    rem.sheetList.append(html);
}


// 清空歌单显示
function clearSheet() {
    rem.sheetList.html('');
}

// 歌单列表底部登陆条
function sheetBar() {
    var barHtml;
    if(playerReaddata('uid')) {
        barHtml = '已同步 ' + rem.uname + ' 的歌单 <span class="login-btn login-refresh">[刷新]</span> <span class="login-btn login-out">[退出]</span>';
    } else {
        barHtml = '我的歌单 <span class="login-btn login-in">[点击同步]</span>';
    }
    barHtml = '<span id="sheet-bar"><div class="clear-fix"></div>' +
    '<div id="user-login" class="sheet-title-bar">' + barHtml + 
    '</div></span>'; 
    rem.sheetList.append(barHtml);
}

// 选择要显示哪个数据区
// 参数：要显示的数据区（list、sheet、player）
function dataBox(choose) {
    $('.btn-box .active').removeClass('active');
    switch(choose) {
        case "list":    // 显示播放列表
            if($(".btn[data-action='player']").css('display') !== 'none') {
                $("#player").hide();
            } else if ($("#player").css('display') == 'none') {
                $("#player").fadeIn();
            }
            $("#main-list").fadeIn();
            $("#sheet").fadeOut();
            if(rem.dislist == 1 || rem.dislist == rem.playlist) {  // 正在播放
                $(".btn[data-action='playing']").addClass('active');
            } else if(rem.dislist == 0) {  // 搜索
                $(".btn[data-action='search']").addClass('active');
            }
        break;
        
        case "sheet":   // 显示专辑
            if($(".btn[data-action='player']").css('display') !== 'none') {
                $("#player").hide();
            } else if ($("#player").css('display') == 'none') {
                $("#player").fadeIn();
            }
            $("#sheet").fadeIn();
            $("#main-list").fadeOut();
            $(".btn[data-action='sheet']").addClass('active');
        break;
        
        case "player":  // 显示播放器
            $("#player").fadeIn();
            $("#sheet").fadeOut();
            $("#main-list").fadeOut();
            $(".btn[data-action='player']").addClass('active');
        break;
    }
}

// 将当前歌曲加入播放历史
// 参数：要添加的音乐
function addHis(music) {
    if(rem.playlist == 2) return true;  // 在播放“播放记录”列表则不作改变
    
    if(musicList[2].item.length > 300) musicList[2].item.length = 299; // 限定播放历史最多是 300 首
    
    if(music.id !== undefined && music.id !== '') {
        // 检查历史数据中是否有这首歌，如果有则提至前面
        for(var i=0; i<musicList[2].item.length; i++) {
            if(musicList[2].item[i].id == music.id && musicList[2].item[i].source == music.source) {
                musicList[2].item.splice(i, 1); // 先删除相同的
                i = musicList[2].item.length;   // 找到了，跳出循环
            }
        }
    }
    
    // 再放到第一位
    musicList[2].item.unshift(music);
    
    //由于浏览器本地储存限制
    //判断图片字符串大小，如果大于200，说明不是链接而是base64编码的图片
    //清除url，为了再次播放时重新加载图片
    var items = musicList[2].item
    for( i in items){
        if(i != 0 && items[i].pic){
            //pic不为null才能使用.length
            if(items[i].pic.length>200){
                items[i].pic=null;
                items[i].url=null;
            }
            
        }
        
        //如果播放列表超过60，则删除超过60的歌曲信息
        //否则将无法添加新歌曲到播放列表
        if(i>60){
            items.splice(i,1);
        }
    }
    playerSavedata('his', items);  // 保存播放历史列表
}

// 初始化播放列表
function initList() {
    // 登陆过，那就读取出用户的歌单，并追加到系统歌单的后面
    if(playerReaddata('uid')) {
        rem.uid = playerReaddata('uid');
        rem.uname = playerReaddata('uname');
        // musicList.push(playerReaddata('ulist'));
        var tmp_ulist = playerReaddata('ulist');    // 读取本地记录的用户歌单
        
        if(tmp_ulist) musicList.push.apply(musicList, tmp_ulist);   // 追加到系统歌单的后面
    }
    //添加“添加歌单”按钮
    addPlaylistBtn();
    
    // 显示所有的歌单
    for(var i=1; i<musicList.length; i++) {
        
        if(i == 1) {    // 正在播放列表
            // 读取正在播放列表
            var tmp_item = playerReaddata('playing');
            if(tmp_item) {  // 读取到了正在播放列表
                musicList[1].item = tmp_item;
                mkPlayer.defaultlist = 1;   // 默认显示正在播放列表
            }
            
        } else if(i == 2) { // 历史记录列表
            // 读取历史记录
            var tmp_item = playerReaddata('his');
            if(tmp_item) {
                musicList[2].item = tmp_item;
            }
            
         // 列表不是用户列表，并且信息为空，需要ajax读取列表
        }else if(!musicList[i].creatorID && (musicList[i].item == undefined || (i>2 && musicList[i].item.length == 0))) {   
            musicList[i].item = [];
            if(musicList[i].id) {   // 列表ID已定义
                // ajax获取列表信息
                ajaxPlayList(musicList[i].id, i);
            } else {    // 列表 ID 未定义
                if(!musicList[i].name) musicList[i].name = '未命名';
            }
        }
        
        // 在前端显示出来
        addSheet(i, musicList[i].name, musicList[i].cover);
    }

    //额外添加的歌单
    if(playerReaddata('addedlists')){
        //读取本地歌单
        var addedlists = playerReaddata('addedlists');
        for(i=0;i<addedlists.length;i++){
            var listlength = musicList.length;
            var music = {};
            music.id = addedlists[i].id;
            music.source =  addedlists[i].source;
            musicList[listlength]= JSON.parse(JSON.stringify(music));

            //加载歌单信息，并添加到html
            ajaxPlayList(addedlists[i].id,listlength,(id)=>{
                addSheet(id,musicList[id].name,musicList[id].cover);
            });
        }
    }
    
    // 登陆了，但歌单又没有，说明是在刷新歌单
    if(playerReaddata('uid') && !tmp_ulist) {
        ajaxUserList('qqmusic',rem.uid);
        return true;
    }
    
    // 首页显示默认列表
    if(mkPlayer.defaultlist >= musicList.length) mkPlayer.defaultlist = 1;  // 超出范围，显示正在播放列表
    
    if(musicList[mkPlayer.defaultlist].isloading !== true)  loadList(mkPlayer.defaultlist);
    
    // 显示最后一项登陆条
    sheetBar();
}

// 清空用户的同步列表
function clearUserlist() {
    if(!rem.uid) return false;
    
    // 查找用户歌单起点
    for(var i=1; i<musicList.length; i++) {
        if(musicList[i].creatorID !== undefined && musicList[i].creatorID == rem.uid) break;    // 找到了就退出
    }
    
    // 删除记忆数组
    musicList.splice(i, musicList.length - i); // 先删除相同的
    musicList.length = i;
    
    // 刷新列表显示
    clearSheet();
    initList();
}

// 清空当前显示的列表
function clearDislist() {
    musicList[rem.dislist].item.length = 0;  // 清空内容
    if(rem.dislist == 1) {  // 正在播放列表
        playerSavedata('playing', '');  // 清空本地记录
        $(".sheet-item[data-no='1'] .sheet-cover").attr('src', 'data:image/png;base64,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');    // 恢复正在播放的封面
    } else if(rem.dislist == 2) {   // 播放记录
        playerSavedata('his', '');  // 清空本地记录
    }
    layer.msg('列表已被清空');
    dataBox("sheet");    // 在主界面显示出音乐专辑
}

// 刷新播放列表，为正在播放的项添加正在播放中的标识
function refreshSheet() {
    // 调试信息输出
    if(mkPlayer.debug) {
        console.log("开始播放列表 " + musicList[rem.playlist].name + " 中的歌曲");
    }
    
    $(".sheet-playing").removeClass("sheet-playing");        // 移除其它的正在播放
    
    $(".sheet-item[data-no='" + rem.playlist + "']").addClass("sheet-playing"); // 添加样式
}

// 播放器本地存储信息
// 参数：键值、数据
function playerSavedata(key, data) {
    key = 'mkPlayer2_' + key;    // 添加前缀，防止串用
    data = JSON.stringify(data);
    // 存储，IE6~7 不支持HTML5本地存储
    if (window.localStorage) {
        localStorage.setItem(key, data);	
    }
}

// 播放器读取本地存储信息
// 参数：键值
// 返回：数据
function playerReaddata(key) {
    if(!window.localStorage) return '';
    key = 'mkPlayer2_' + key;
    return JSON.parse(localStorage.getItem(key));
}
