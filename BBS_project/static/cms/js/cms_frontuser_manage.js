/**
 * Created by Administrator on 2017/4/6.
 */



//操作前台用户执行事件
$(function () {
    $('.is_active_btn').click(function (event) {
        event.preventDefault();
        var is_active = parseInt($(this).attr('data-is_active'));
        var uid  = $(this).attr('data-frontuser-id');
        var msg = '';
        if(is_active==1){
            msg = '是否禁用'
        }else{
            msg = '是否取消禁用'
        }
        myalert.alertConfirm({
            'msg':msg,
            'confirmCallback':function () {
                myajax.post({
                    'url':'/frontuser_manage/',
                    'data':{
                        'is_active':is_active,
                        'uid':uid,
                    },
                    'success':function (data) {
                        if(data['code']==200){
                            setTimeout(function () {
                                myalert.alertSuccessToast('操作成功！')
                            },500);
                            setTimeout(function () {
                                window.location.reload();
                            },1500)


                        }else{
                            myalert.alertErrorToast(data['message'])
                        }
                    }
                })
            },
            'cancelCallback':function () {
                myalert.close();
            }
        })
    })
});



// 排序执行事件

$(function () {
    $('.sort-select').change(function (event) {
        event.preventDefault();
        var option = $(this).val();
        newhref = myparam.setParam(window.location.href,'sort',option);
        window.location = newhref;
    })
})