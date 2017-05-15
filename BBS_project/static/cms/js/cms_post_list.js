/**
 * Created by Administrator on 2017/4/14.
 */

//加精与取消加精
$(function () {
    $(".is_elite").click(function (event) {
        event.preventDefault();
        var elite = parseInt($(this).attr('data-post-elite'));
        var post_id = $(this).attr('data-post-id');
        myajax.post({
            'url':'/elite/',
            'data':{
                'elite':elite,
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code']==200){
                    var msg='';
                    if(elite==1){
                        msg = '取消加精成功！'
                    }else{
                        msg = '加精成功！'
                    }
                    myalert.alertSuccessToast(msg);
                    setTimeout(function () {
                        window.location.reload()
                    },500)
                }else{
                    myalert.alertErrorToast(data['message'])
                }
            }
        })
    })
});


//删除帖子
$(function () {
    $('.is_remove').click(function (event) {
        event.preventDefault();
        var post_id = $(this).attr('data-post-id');
        myajax.post({
            'url':'/delete_post/',
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code']==200){
                    myalert.alertSuccessToast('删除成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500)
                }else{
                    myalert.alertErrorToast(data['message'])
                }
            }
        })

    });
});


//排序事件
$(function () {
   $('#sort_select').change(function (event) {
       var sort = $(this).val();
       var newurl = myparam.setParam(window.location.href,'sort',sort);
       var newurl = myparam.setParam(newurl,'page',1);
       window.location = newurl;
   })
});


//板块过滤
$(function () {
    $('#board-filter_select').change(function (event) {
        var bord_id = $(this).val();
        var newurl = myparam.setParam(window.location.href,'board',bord_id);
        var newurl = myparam.setParam(newurl,'page',1);
        window.location=newurl;
    })
})