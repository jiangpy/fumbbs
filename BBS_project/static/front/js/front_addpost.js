/**
 * Created by Administrator on 2017/3/25.
 */





// 发布帖子
$(function () {
    $('#pub_post_btn').click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name=title]');
        var captchaInput = $('input[name=graph_captcha]');

        var title = titleInput.val();
        var board = $('.board-select').val();
        var content = window.editor.$txt.html();
        var graph_captcha = captchaInput.val();
        myajax.post({
           'url':'/addpost/',
            'data':{
               'title':title,
                'board_id':board,
                'content':content,
                'graph_captcha':graph_captcha
            },
            'success':function (data) {
                if(data['code']==200){
                    console.log(content);
                    myalert.alertConfirm({
                        'title':'发布成功！',
                        'confirmText':'再发一篇',
                        'cancelText':'返回首页',
                        'confirmCallback':function () {
                            titleInput.val('');
                            window.editor.clear();
                            captchaInput.val('');
                        },
                        'cancelCallback':function () {
                            window.location = '/';
                        }
                    });
                }else {
                    myalert.alertError(data['message']);
                }
            }

        });
    })
})