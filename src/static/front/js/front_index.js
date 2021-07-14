$(document).ready(function () {
    $(".layui-colla-content span a").each(function (i) {
        $(this).hover(function () {
            $('.tips').addClass("hover");
            $(this).parent().addClass("lihover");
            var img = $('.tipscont').find('img').attr('src');
            var self = $(this);
            var name = $(this).attr('img-name');
            var src = $(this).attr('img-src');
            var account_id = $(this).attr('img-data');
            if (src == img && src != '') {
                return;
            } else if (src != img && src != '') {
                $('.tipscont').find('img').attr('src', src);
                return;
            }
            zlajax.get({
                'url': '/get_img/',
                'data': {
                    'account_id': account_id,
                },
                'success': function (data) {
                    if (data['code'] == 200) {

                        var img = data['data']['img'];
                        self.attr('img-src', img);
                        $('.tipscont').find('img').attr('src', img);
                    } else {
                        $('.tipscont').find('img').attr('src', '');
                    }
                }
            })
        }, function () {
            $('.tips').removeClass("hover");
            $(this).parent().removeClass("lihover");
        });
    });

});
layui.use(['element', 'carousel', 'flow', 'form'], function () {
    var carousel = layui.carousel;
    //建造实例
    var form = layui.form;
    carousel.render({
        elem: '#test1'
        , width: '100%' //设置容器宽度
        , arrow: 'hover' //始终显示箭头
        , anim: 'default' //切换动画方式
        , interval: 7000

    });
    var flow = layui.flow;

    flow.load({
        elem: '#demo' //指定列表容器
        , isAuto: true
        , mb: 1
        , isLazyimg: true
        , done: function (page, next) { //到达临界点（默认滚动触发），触发下一页
            var lis = [];
            //以jQuery的Ajax请求为例，请求下一页数据（注意：page是从2开始返回）
            var flag = $("#num").attr('data-num');
            console.log(flag);
            if (flag == '1') {
                var url = '/articles/?page=' + page;
                $.get(url, function (res) {
                    //假设你的列表返回在data集合中
                    layui.each(res.data, function (index, item) {
                        lis.push(" <hr>\n" +
                            "            <div class=\"layui-row\">\n" +
                            "                <div class=\"layui-col-md2 layui-col-sm2\" id=\"img\">\n" +
                            "                    <img src=\"http://img04.sogoucdn.com/net/a/04/link?appid=100520033&url=" + item.cover + "\" alt=\"\">\n" +
                            "                </div>\n" +
                            "                <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                            "                    <div class=\"layui-row grid-demo grid-demo-bg1\">\n" +
                            "                        <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                            "                            <span class=\"title\"><a href=" + item.url + " target='_blank'>" + item.title + "</a></span>\n" +
                            "                        </div>\n" +
                            "                        <div class=\"layui-col-md2 layui-col-sm2\">\n" +
                            "                                <span class=\"layui-badge layui-bg-green\">" + item.author + "</span>\n" +
                            "                        </div>\n" +
                            "                        <div class=\"layui-col-md12 layui-col-sm12\">\n" +
                            "                            <div class=\"digest\">\n" + item.digest +

                            "                            </div>\n" +
                            "                        </div>\n" +
                            "\n" +
                            "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                            "                            <span class=\"layui-badge-rim\">" + "<a href=http://wechat.doonsec.com/admin/wechat_echarts/?biz=" + item.biz + " target='_blank'>" + item.account_name + "</a> </span>\n" +
                            "                        </div>\n" + "\n" +
                            "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                            "                            <span class=\"layui-badge-rim\"><a href=\"http://wechat.doonsec.com/article/?id=" + item.id + "\" target='_blank'>微信快照链接</a></span>\n" +
                            "                        </div>\n" +
                            "                        <div class=\"layui-col-md2 layui-col-sm1\" id=\"account\">\n" +
                            "                            <span class=\"layui-badge-rim\"><i class=\"layui-icon layui-icon-praise\" aria-hidden=\"true\"\n" +
                            "                                                             id=\"font\">" + item.like + "</i></span>\n" +
                            "                        </div>\n" +
                            "                        <div class=\"layui-col-md2 layui-col-sm1\" id=\"account\">\n" +
                            "                            <span class=\"layui-badge-rim\"><i class=\"layui-icon  layui-icon-read\" aria-hidden=\"false\"\n" +
                            "                                                             id=\"font\">" + item.read + "</i></span>\n" +
                            "                        </div>\n" +
                            "                        <div class=\"layui-col-md3 layui-col-sm3\" id=\"account\">\n" +
                            "                            <span class=\"layui-badge-rim\">" + item.publish_time + "</span>\n" +
                            "                        </div>\n" +
                            "                    </div>\n" +
                            "                </div>\n" +
                            "            </div>"
                        )
                    });

                    //执行下一页渲染，第二参数为：满足“加载更多”的条件，即后面仍有分页
                    //pages为Ajax返回的总页数，只有当前页小于总页数的情况下，才会继续出现加载更多
                    next(lis.join(''), page < res.count);
                });
            }
        }
    });

    // $(function () {
    //     $("#add_account").click(function () {
    //         // var dialog = $("#banner-dialog");
    //         // var nameInput = dialog.find("input[name='name']");
    //         // var imageInput = dialog.find("input[name='image_url']");
    //         // var linkInput = dialog.find("input[name='link_url']");
    //         // var priorityInput = dialog.find("input[name='priority']");
    //         // nameInput.val("");
    //         // imageInput.val("");
    //         // linkInput.val("");
    //         // priorityInput.val("");
    //         // dialog.modal('show')
    //         layer.open({
    //             type: 1,
    //             anim: 1,
    //             area: ['50%', '60%'],
    //             skin: 'demo-class',
    //             // btn: ['立即提交', '取消'],
    //             maxmin: true,
    //             shadeClose: false,
    //             title: '贡献微信公众号',
    //             content: $('#add'),
    //             success: function (index) {
    //                 var but = $(".layui-layer-btn0");
    //                 but.attr('lay-filter', 'demo1');
    //                 but.attr('lay-submit', "");
    //             }
    //         });
    //     })
    // });
    // form.on('submit(add)', function (data1, index) {
    //     var dic = new Object();
    //     var account_name = data1.field.account_name;
    //     var tag_name = data1.field.tag_name;
    //     var account_link = data1.field.account_link;
    //     var founder = data1.field.founder;
    //     dic.account_name = account_name;
    //     dic.tag_name = tag_name;
    //     dic.account_link = account_link;
    //     dic.founder = founder;
    //
    //     zlajax.post({
    //         'url': '/admin/community_account_add/',
    //         'data': dic,
    //         'success': function (data) {
    //             if (data['code'] == 200) {
    //                 layer.msg(data['message']);
    //                 form.val('example', {
    //                     'account_name': null,
    //                     'tag_name': null,
    //                     'account_link': null
    //                 });
    //                 setTimeout(function () {
    //                     layer.closeAll();
    //                 }, 1000);
    //                 window.location.reload()
    //             } else {
    //                 layer.msg(data['message']);
    //             }
    //         }, 'fail': function () {
    //             layer.msg('网络错误！')
    //         }
    //     });
    //
    //     return false
    // });
});
//公众号下的文章
$(function () {
    $.ajaxSetup({cache: false});
    $(".layui-colla-content a").click(function (event) {
        var a = $(this);
        var id = a.attr('img-data');
        var flag = $("#num");
        flag.attr('data-num', "2");
        $("#demo").empty();
        layui.use('flow', function () {
            var flow = layui.flow;
            flow.load({
                elem: '#demo' //指定列表容器

                , isAuto: true
                , mb: 1
                , done: function (page, next) { //到达临界点（默认滚动触发），触发下一页
                    layer.load();
                    var lis = [];
                    //以jQuery的Ajax请求为例，请求下一页数据（注意：page是从2开始返回）
                    if (flag.attr('data-num') == '2') {
                        var url = '/articles/?page=' + page + '&id=' + id;
                        $.get(url, function (res) {
                            //假设你的列表返回在data集合中
                            layer.closeAll('loading');
                            layui.each(res.data, function (index, item) {

                                lis.push(" <hr>\n" +
                                    "            <div class=\"layui-row\">\n" +
                                    "                <div class=\"layui-col-md2 layui-col-sm2\" id=\"img\">\n" +
                                    "                    <img src=\"http://img04.sogoucdn.com/net/a/04/link?appid=100520033&url=" + item.cover + "\" alt=\"\">\n" +
                                    "                </div>\n" +
                                    "                <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                                    "                    <div class=\"layui-row grid-demo grid-demo-bg1\">\n" +
                                    "                        <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                                    "                            <span class=\"title\"><a href=" + item.url + " target='_blank'>" + item.title + "</a></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm2\">\n" +
                                    "                                <span class=\"layui-badge layui-bg-green\">" + item.author + "</span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md12 layui-col-sm12\">\n" +
                                    "                            <div class=\"digest\">\n" + item.digest +

                                    "                            </div>\n" +
                                    "                        </div>\n" +
                                    "\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\">" + "<a href=http://wechat.doonsec.com/admin/wechat_echarts/?biz=" + item.biz + " target='_blank'>" + item.account_name + "</a> </span>\n" +
                                    "                        </div>\n" + "\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\"><a href=\"http://wechat.doonsec.com/article/?id=" + item.id + "\" target='_blank'>微信快照链接</a></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm1\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\"><i class=\"layui-icon layui-icon-praise\" aria-hidden=\"true\"\n" +
                                    "                                                             id=\"font\">" + item.like + "</i></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm1\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\"><i class=\"layui-icon  layui-icon-read\" aria-hidden=\"false\"\n" +
                                    "                                                             id=\"font\">" + item.read + "</i></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md3 layui-col-sm3\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\">" + item.publish_time + "</span>\n" +
                                    "                        </div>\n" +
                                    "                    </div>\n" +
                                    "                </div>\n" +
                                    "            </div>"
                                )
                            });

                            //执行下一页渲染，第二参数为：满足“加载更多”的条件，即后面仍有分页
                            //pages为Ajax返回的总页数，只有当前页小于总页数的情况下，才会继续出现加载更多
                            next(lis.join(''), page < res.count);
                            url = ''
                        });
                    }
                }
            });

        });
    })
});

//；类别查询d
$(function () {

    $('.search-li').click(function (event) {
        event.preventDefault();
        $.ajaxSetup({cache: false});
        var li = $(this);
        var id = li.attr('id');
        var flag = $("#num");
        flag.attr('data-num', "3");
        $("#demo").empty();
        layui.use('flow', function () {
            var flow = layui.flow;
            flow.load({
                elem: '#demo' //指定列表容器

                , isAuto: true
                , mb: 1
                , done: function (page, next) { //到达临界点（默认滚动触发），触发下一页
                    var lis = [];
                    layer.load();
                    //以jQuery的Ajax请求为例，请求下一页数据（注意：page是从2开始返回）
                    if (flag.attr('data-num') == '3') {
                        var url = '/tags/?page=' + page + '&cat_id=' + id;
                        $.get(url, function (res) {
                            //假设你的列表返回在data集合中
                            layer.closeAll('loading');
                            layui.each(res.data, function (index, item) {

                                lis.push(" <hr>\n" +
                                    "            <div class=\"layui-row\">\n" +
                                    "                <div class=\"layui-col-md2 layui-col-sm2\" id=\"img\">\n" +
                                    "                    <img src=\"http://img04.sogoucdn.com/net/a/04/link?appid=100520033&url=" + item.cover + "\" alt=\"\">\n" +
                                    "                </div>\n" +
                                    "                <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                                    "                    <div class=\"layui-row grid-demo grid-demo-bg1\">\n" +
                                    "                        <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                                    "                            <span class=\"title\"><a href=" + item.url + " target='_blank'>" + item.title + "</a></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm2\">\n" +
                                    "                                <span class=\"layui-badge layui-bg-green\">" + item.author + "</span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md12 layui-col-sm12\">\n" +
                                    "                            <div class=\"digest\">\n" + item.digest +

                                    "                            </div>\n" +
                                    "                        </div>\n" +
                                    "\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\">" + "<a href=http://wechat.doonsec.com/admin/wechat_echarts/?biz=" + item.biz + " target='_blank'>" + item.account_name + "</a> </span>\n" +
                                    "                        </div>\n" + "\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\"><a href=\"http://wechat.doonsec.com/article/?id=" + item.id + "\" target='_blank'>微信快照链接</a></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm1\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\"><i class=\"layui-icon layui-icon-praise\" aria-hidden=\"true\"\n" +
                                    "                                                             id=\"font\">" + item.like + "</i></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md2 layui-col-sm1\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\"><i class=\"layui-icon  layui-icon-read\" aria-hidden=\"false\"\n" +
                                    "                                                             id=\"font\">" + item.read + "</i></span>\n" +
                                    "                        </div>\n" +
                                    "                        <div class=\"layui-col-md3 layui-col-sm3\" id=\"account\">\n" +
                                    "                            <span class=\"layui-badge-rim\">" + item.publish_time + "</span>\n" +
                                    "                        </div>\n" +
                                    "                    </div>\n" +
                                    "                </div>\n" +
                                    "            </div>"
                                )
                            });

                            //执行下一页渲染，第二参数为：满足“加载更多”的条件，即后面仍有分页
                            //pages为Ajax返回的总页数，只有当前页小于总页数的情况下，才会继续出现加载更多
                            next(lis.join(''), page < res.count);
                            url = ''
                        });
                    }
                }
            });

        });
    });

});

