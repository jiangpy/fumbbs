/**
 * Created by Administrator on 2017/4/20.
 */


$(function () {
    $('#submit-comment').click(function (event) {
        event.preventDefault();
        var content = window.editor.$txt.html();
        var post_id = $(this).attr('data-post-id');
        var comment_id = $('.comment-content').attr('data-comment-id');
        console.log(content);
        console.log(post_id);
        myajax.post({
            'url':'/addcomment/'+post_id+'/',
            'data':{
                'content':content,
                'post_id':post_id,
                'comment_id':comment_id
            },
            'success':function (data) {
                if(data['code']==200){
                    myalert.alertSuccessToast('评论发表成功！')
                    setTimeout(function () {
                        window.location = '/postdetail/'+post_id+'/';
                    },500)
                }else {
                    myalert.alertErrorToast(data['message'])
                }
            }
        })
    })
});