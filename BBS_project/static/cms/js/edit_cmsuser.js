/**
 * Created by Administrator on 2017/3/26.
 */

//修改用户权限
$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var rolesCheckbox = $(':checkbox:checked');
        var roles = [];
        rolesCheckbox.each(function () {
            var role_id = $(this).val();
            roles.push(role_id);
        });
        var user_id = $(this).attr('data_user_id');
        myajax.post({
            'url':'/cmsusermanage/edit_cmsuser/',
            'data':{
                'user_id':user_id,
                'roles':roles,
            },
            'success':function (data) {
                if(data['code']==200){
                    rolesCheckbox.each(function () {
                        $(this).prop('checked',false);
                    });
                    setTimeout(function () {
                        window.location='/cmsusermanage/';
                    },1000)
                    myalert.alertSuccessToast('修改成功！');
                }else{
                    myalert.alertInfoToast(data['message'])
                };

            },
        });
    })
})


// 拉黑或移出黑名单执行事件
$(function () {
    $('#is_black_btn').click(function (event) {
        event.preventDefault();
        var is_active = $(this).attr('data_is_active');
        var user_id  = $(this).attr('data_user_id');
        console.log(user_id);
        myajax.post({
           'url':'/black_list/',
            'data':{
               'is_active':is_active,
                'user_id':user_id,
            },
            'success':function (data) {
                if(data['code']==200){
                    if(is_active=='1'){
                       var msg = '加入黑名单成功！'
                    }else{
                       var msg = '移出黑名单成功！'
                    }
                    myalert.alertSuccessToast(msg)
                    setTimeout(function () {
                        window.location='/cmsusermanage/';
                    },1000)
                }else {
                    myalert.alertInfoToast(data['message'])
                }
            }
        });
    });
});