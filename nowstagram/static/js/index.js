$(function () {
    var oExports = {
        initialize: fInitialize,
        // 渲染更多数据
        renderMore: fRenderMore,
        // 请求数据
        requestData: fRequestData,
        // 简单的模板替换
        tpl: fTpl
    };
    // 初始化页面脚本
    oExports.initialize();
function detail_index() {
    //展开后条目评论功能的实现
    var oExports = {
        initialize: fInitialize,
        encode: fEncode
    };
    oExports.initialize();

    function fInitialize() {
        var that = this;

        var num = $('ul.discuss-list');
        for (i = 1; i <= num.length; i++){

            // 点击添加评论
            var bSubmit = false;
            $('#jsSubmit-' + i).unbind();
            $('#jsSubmit-' + i).on('click', function () {
                var control_id = $(this).attr('id')//jsSubmit-n  首页的第n条
                var id = control_id.substring(9)
                console.log(id)
                var sImageId = $('#js-image-id-' + id).val();//联系index.html image在数据库中的编号
                console.log('simage1.'+sImageId)
                var oCmtIpt = $('#jsCmt-' + id);
                console.log(oCmtIpt.val())
                var oListDv = $('.js-discuss-list-' + id);

                sCmt = oCmtIpt.val()
                console.log(sCmt)
                // 评论为空不能提交
                if (!sCmt) {
                    console.log('pinglun: ' + id + oCmtIpt.attr('id'))
                    return alert('评论不能为空');
                    //continue;
                }
                // 上一个提交没结束之前，不再提交新的评论
                if (bSubmit) {
                    return;
                }
                bSubmit = true;
                $.ajax({
                    url: '/addcomment/',
                    type: 'post',
                    dataType: 'json',
                    data: {image_id: sImageId, content: sCmt}
                }).done(function (oResult) {
                    if (oResult.code !== 0) {
                        console.log('2,'+oResult.code+' '+oResult.msg)
                        return alert(oResult.msg|| '提交失败，请重试' );
                    }
                    // 清空输入框
                    oCmtIpt.val('');
                    // 渲染新的评论
                    var sHtml = [
                        '<li>',
                            '<a class="_4zhc5 _iqaka" title="', that.encode(oResult.username), '" href="/profile/', oResult.user_id, '">', that.encode(oResult.username), '</a> ',
                            '<span><span>', that.encode(sCmt), '</span></span>',
                        '</li>'].join('');
                    oListDv.prepend(sHtml);

                    // 修改评论数
                    var counts = $(".length-" + id).text()
                    $(".length-" + id).text(parseInt(counts, 10) + 1);

                }).fail(function (oResult) {
                    console.log('1,'+oResult.code+' '+oResult.msg)
                    alert(oResult.msg || '提交失败，请重试' );

                }).always(function () {
                    bSubmit = false;
                });
            });
        }
    }

    function fEncode(sStr, bDecode) {
        var aReplace =["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
             sStr = sStr.replace(new RegExp(aReplace[i],'g'), aReplace[i+1]);
        }
        return sStr;
    };

}


    function fInitialize() {
    //首页更多条目ajax请求
        var that = this;
        // 常用元素
        that.listEl = $('div.js-image-list');
        // 初始化数据
        //that.uid = window.uid;
        that.page = 1;
        that.pageSize = 5;
        that.listHasNext = true;
        // 绑定事件
        $('.js-load-more').on('click', function (oEvent) {
            var oEl = $(oEvent.currentTarget);
            var sAttName = 'data-load';
            // 正在请求数据中，忽略点击事件
            if (oEl.attr(sAttName) === '1') {
                return;
            }
            // 增加标记，避免请求过程中的频繁点击
            oEl.attr(sAttName, '1');
            that.renderMore(function () {
                // 取消点击标记位，可以进行下一次加载
                oEl.removeAttr(sAttName);
                // 没有数据隐藏加载更多按钮
                !that.listHasNext && oEl.hide();
            });
        });
    }

    function fRenderMore(fCb) {
        var that = this;
        // 没有更多数据，不处理
        if (!that.listHasNext) {
            return;
        }
        that.requestData({
            uid: that.uid,
            page: that.page + 1,
            pageSize: that.pageSize,
            call: function (oResult) {
                // 是否有更多数据
                that.listHasNext = !!oResult.has_next && (oResult.images || []).length > 0;
                // 更新当前页面
                that.page++;
                // 渲染数据
                var sHtml = '';
                $.each(oResult.images, function (nIndex, oImage) {
            var cur_page_id = (that.page - 1) * that.pageSize + nIndex + 1;
            sHtml_part1 = that.tpl([
                         '<article class="mod">',
            '<header class="mod-hd">',
                '<time class="time">#{created_date}</time>',
                '<a href="/profile/#{user_id}" class="avatar">',
                 '   <img src="#{head_url}">',
                '</a>',
                '<div class="profile-info">',
                    '<a title="#{user_name}" href="/profile/#{user_id}">#{user_name}</a>',
                '</div>',
            '</header>',
            '<div class="mod-bd">',
                '<div class="img-box">',
                    '<a href = "/image/#{id}">',
                    '<img src="#{url}">',
               ' </div>',
           ' </div>',
           ' <div class="mod-ft">',
              '  <ul class="discuss-list">',
                   ' <li class="more-discuss js-discuss-list">',
                       ' <a>',
                           '<a href = "/image/{{image.id}}">',
                           ' <span>全部</span><span class="">#{comment_count}</span>',
                            '<span>条评论</span></a>',
                    '</li>',
                    '<div class="js-discuss-list-',
                cur_page_id.toString(),
                '"> </div>'].join(''), oImage);
                    sHtml_part2 = ' ';

                    for (var ni = 0; ni < Math.min(2,oImage.comment_count); ni++){
                        dict = {'comment_user_username':oImage.comments[ni].comment_username, 'comment_user_id':oImage.comments[ni].user_id,
                            'comment_content':oImage.comments[ni].content };

                        sHtml_part2 += that.tpl([
                        '    <li>',
                            '    <a class="_4zhc5 _iqaka" title="#{comment_user_username}" href="/profile/#{comment_user_id}" data-reactid=".0.1.0.0.0.2.1.2:$comment-17856951190001917.1">#{comment_user_username}</a>',
                            '    <span>',
                            '        <span>#{comment_content}</span>',
                           '     </span>',
                         '   </li>',
                             ].join(''), dict);
                    }

                    sHtml_part3 =    that.tpl([
                        '</div>',
              '  </ul>',
               '<section class="discuss-edit">',
                  '<a class="icon-heart-empty"></a>',
                   '<form>',
                   ' <input placeholder="添加评论..." id="jsCmt-',
                        cur_page_id.toString(),
                        '" type="text">',
                   '<input id = "js-image-id-',
                        cur_page_id.toString(),
                        '" type = "text" style="display: none" value="#{id}">',
                   '</form>',
                   ' <button class="more-info" id="jsSubmit-',
                        cur_page_id.toString(),
                        '">更多选项</button>',
                '</section>',
           ' </div>',

       ' </article>  '
                    ].join(''), oImage);

                    sHtml += sHtml_part1 + sHtml_part2 + sHtml_part3;
                });
                sHtml && that.listEl.append(sHtml);
            },
            error: function () {
                alert('出现错误，请稍后重试');
            },
            always: fCb
        });
        setTimeout(detail_index, 1000);
    }

    function fRequestData(oConf) {
        var that = this;
        var sUrl = '/index/images/' + oConf.page + '/' + oConf.pageSize + '/';
        $.ajax({url: sUrl, dataType: 'json'}).done(oConf.call).fail(oConf.error).always(oConf.always);
    }

    function fTpl(sTpl, oData) {
        var that = this;
        sTpl = $.trim(sTpl);
        return sTpl.replace(/#{(.*?)}/g, function (sStr, sName) {
            return oData[sName] === undefined || oData[sName] === null ? '' : oData[sName];
        });
    }
});