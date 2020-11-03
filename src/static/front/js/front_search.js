layui.use(['layer', ''], function () {
    var layer = layui.layer;
});


function setHeightKeyWord(keyword) {
    /* 获取需要处理的关键字 */
    var tempHTML = $("#demo").html();
    /* 关键字替换文本 该文本设置有高亮颜色 */
    var replaceText = "<font style='color:red;'>$1</font>";
    /* 关键字正则匹配规则 */
    var r = new RegExp("(" + keyword + ")", "ig");
    /* 将匹配到的关键字替换成我们预设的文本 */
    tempHTML = tempHTML.replace(r, replaceText);
    /* 将文本显示到浏览器上 */
    return tempHTML
    // $("#demo").html(tempHTML);
}

$(function () {
    $(".search_btn").click(function (event) {
        event.preventDefault();
        var flag = $("#num");
        flag.attr('data-num', '4');
        var search_obj = $(".search_text");
        var keyword = search_obj.val();
        if (keyword.match(/^[ ]*$/)) {
            layer.msg("搜索关键词不能为空！");
            return;
        }
        $(".search-sub-menu").fadeOut(500);
        $(document).unbind('scroll');
        layui.use('flow', function () {
            var flow = layui.flow;
            $("#demo").empty();
            var nospace_keyword = keyword.replace(/ /g, "");
            var new_keyword = nospace_keyword.replace(/&/g, "|");
            console.log(new_keyword);
            var replaceText = "<font style='color:red;'>$1</font>";
            var r = new RegExp("(" + new_keyword + ")", "ig");
            flow.load({
                elem: '#demo' //指定列表容器

                , isAuto: true
                , mb: 1
                , done: function (page, next) { //到达临界点（默认滚动触发），触发下一页
                    var lis = [];
                    layer.load();
                    //以jQuery的Ajax请求为例，请求下一页数据（注意：page是从2开始返回）
                    if (flag.attr('data-num') == '4') {
                        zlajax.post({
                            'url': '/search/',
                            "traditional": true,
                            'data': {
                                'page': page,
                                'keyword': keyword,
                            },
                            'success': function (data) {
                                layer.closeAll('loading');
                                if (data['code'] == 0) {

                                    layer.msg(data['message']);

                                    layui.each(data.data, function (index, item) {
                                        lis.push(" <hr>\n" +
                                            "            <div class=\"layui-row\">\n" +
                                            "                <div class=\"layui-col-md2 layui-col-sm2\" id=\"img\">\n" +
                                            "                    <img src=\"http://img04.sogoucdn.com/net/a/04/link?appid=100520033&url=" + item.cover + "\" alt=\"\">\n" +
                                            "                </div>\n" +
                                            "                <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                                            "                    <div class=\"layui-row grid-demo grid-demo-bg1\">\n" +
                                            "                        <div class=\"layui-col-md10 layui-col-sm10\">\n" +
                                            "                            <span class=\"title\"><a href=" + item.url + "  target='_blank'>" + item.title.replace(r, replaceText) + "</a></span>\n" +
                                            "                        </div>\n" +
                                            "                        <div class=\"layui-col-md2 layui-col-sm2\">\n" +
                                            "                                <span class=\"layui-badge layui-bg-green\">" + item.author.replace(r, replaceText) + "</span>\n" +
                                            "                        </div>\n" +
                                            "                        <div class=\"layui-col-md12 layui-col-sm12\">\n" +
                                            "                            <div class=\"digest\">\n" + item.digest.replace(r, replaceText) +
                                            "                            </div>\n" +
                                            "                        </div>\n" +
                                            "\n" +
                                            "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                                            "                            <span class=\"layui-badge-rim\">" + "<a href=/admin/wechat_echarts/?biz=" + item.biz + " target='_blank'>" + item.account_name.replace(r, replaceText) + "</a> </span>\n" +
                                            "                        </div>\n" + "\n" +
                                            "                        <div class=\"layui-col-md2 layui-col-sm2\" id=\"account\">\n" +
                                            "                            <span class=\"layui-badge-rim\"><a href=\"article/?id=" + item.id + "\" target='_blank'>微信快照链接</a></span>\n" +
                                            "                        </div>\n" +
                                            "                        <div class=\"layui-col-md1 layui-col-sm1\" id=\"account\">\n" +
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
                                        );
                                    });
                                } else {
                                    layer.msg(data['message']);
                                }
                                //执行下一页渲染，第二参数为：满足“加载更多”的条件，即后面仍有分页
                                //pages为Ajax返回的总页数，只有当前页小于总页数的情况下，才会继续出现加载更多
                                next(lis.join(''), page < data.count);

                                // setHeightKeyWord(keyword);
                            },
                            'fail': function (error) {
                                layer.closeAll('loading');
                                layer.msg('网络错误！');
                            }
                        });
                    }
                }
            });
        });
    })
});