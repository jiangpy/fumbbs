/**
 * Created by Administrator on 2017/4/16.
 */


$(function () {
    var imgTag = $('.post-content>p>img');
    if(imgTag.attr('style')){
        console.log(imgTag.attr('style'));
        imgTag.removeAttr('style');
    }
});


//点赞事件
$(function () {
    $("#praise-btn").click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        var praisenumber = parseInt($(this).attr('data-praisenumber'));
        var is_login = parseInt($(this).attr('data-login'));
        var c_url = window.location.pathname;
        if(is_login==0){
            window.location = '/account/login/?next='+c_url;
            return
        }
        console.log(post_id);
        console.log(praisenumber);
        myajax.post({
            "url":'/post_praise/',
            'data':{
                'post_id':post_id,
                'praisenumber':praisenumber,
            },
            'success':function (data) {
                var msg = '';
                if (praisenumber==0){
                    msg='点赞成功！'
                }else {
                    msg= '取消赞成功！'
                }
                if(data['code']==200){
                    myalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload()
                    },700);

                }else{
                    myalert.alertErrorToast(data['message'])
                }
            }
        })
    })
});