layui.use(['form', 'layedit', 'jquery'], function () {
    var form = layui.form;
    var layedit = layui.layedit;

    var index = layedit.build('demo', {
        tool: [
            'strong' //加粗
            , 'italic' //斜体
            , 'underline' //下划线
            , 'del' //删除线
            , '|' //分割线
            , 'left' //左对齐
            , 'center' //居中对齐
            , 'right' //右对齐
            , 'link' //超链接
            , 'unlink' //清除链接
            , 'face' //表情
        ]
    }); //建立编辑器
    form.verify({
        content: function (value) {
            if (value.length > 20) {
                return '内容长度不能大于200个字符';
            }
        }
    });
    //监听提交
    form.on('submit(formDemo)', function (data) {
        var content = data.field.content;
        var graph_captcha = data.field.graph_captcha;
        var content = layedit.getContent(index);
        if (content.length <= 0) {
            layer.msg('内容不能为空！');
            return false;
        }
        if (content.indexOf('alert') > -1) {
            alert('xss');/* 添加一个彩蛋*/
            alert('听说你想alert? 那就给你alert');
             $('#captcha-img').trigger('click');
            return false;
        }
        zlajax.post({
            'url': '/admin/msg_board_add/',
            'data': {
                'content': content,
                'graph_captcha':graph_captcha
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    layer.msg(data['message']);
                    $("input").val("");
                     $('#captcha-img').trigger('click');
                } else {
                    layer.msg(data['message']);
                     $('#captcha-img').trigger('click');
                }
            }
        });
        return false;
    });
});