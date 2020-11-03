$(function () {
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src, 'xx', Math.random());
        self.attr('src', newsrc);
    });
});
//页面初始化
layui.use(['element', 'carousel', 'flow', 'form'], function () {
    var carousel = layui.carousel;
    //建造实例

    form = layui.form;


    $(function () {
        $("#add_account").click(function () {
            var self = $(this);
            layer.open({
                type: 1,
                anim: 1,
                area: ['61%', '60%'],
                skin: 'demo-class',
                // btn: ['立即提交', '取消'],
                maxmin: true,
                shadeClose: false,
                title: '贡献微信公众号',
                content: $('#add'),
                success: function (index) {
                    var but = $(".layui-layer-btn0");
                    but.attr('lay-filter', 'demo1');
                    but.attr('lay-submit', "");
                },
                end: function () {  //层销毁时
                    $("input").val("");
                    $("select").val("");
                    $('#captcha-img').trigger('click');
                }
            });
        })
    });
    form.on('submit(add)', function (data1, index) {
        var self = $(this);
        var dic = new Object();
        var account_name = data1.field.account_name;
        var tag_name = data1.field.tag_name;
        var account_link = data1.field.account_link;
        var founder = data1.field.founder;
        var graph_captcha = data1.field.graph_captcha;
        dic.account_name = account_name;
        dic.tag_name = tag_name;
        dic.account_link = account_link;
        dic.founder = founder;
        dic.graph_captcha = graph_captcha;

        zlajax.post({
            'url': '/admin/community_account_add/',
            'data': dic,
            'success': function (data) {
                if (data['code'] == 200) {
                    layer.msg(data['message']);
                    $("input").val("");
                    $("select").val("");
                } else {
                    layer.msg(data['message']);
                }
                $('#captcha-img').trigger('click');
            }, 'fail': function () {
                layer.msg('网络错误！')
            }
        });

        return false
    });
});
$(document).scroll(function () {
    right = $("#right");
    var scroH = $(document).scrollTop();
    if (scroH > 40) {
        right.css('top', 0)
    } else {
        right.removeAttr('style')
    }
});

$(function () {
    $('.to-top').toTop();
});