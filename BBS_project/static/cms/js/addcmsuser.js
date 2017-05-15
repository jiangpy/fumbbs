/**
 * Created by Administrator on 2017/3/26.
 */


$(function () {
    $('#submit').click(function (event) {
        event.preventDefault();
        var usernameInput = $('input[name=username]');
        var emailInput = $('input[name=email]');
        var passwordInput = $('input[name=password]');
        var roleCheckbox = $(':checkbox:checked');
        var username = usernameInput.val();
        var email = emailInput.val();
        var password = passwordInput.val();
        roles = [];
        roleCheckbox.each(function (index,element) {
            var role_id = $(this).val();
            roles.push(role_id);
        });
        myajax.post({
            'url':'/cmsusermanage/adduser/',
            'data':{
                'username':username,
                'email':email,
                'password':password,
                'roles':roles,
            },
            'success':function (data) {
                if(data['code']==200){
                    usernameInput.val('');
                    emailInput.val('');
                    passwordInput.val('');
                    roleCheckbox.each(function () {
                        $(this).prop('checked',false);
                    });
                    myalert.alertSuccessToast('添加成功！');
                    setTimeout(function () {
                        window.location='/cmsusermanage/';
                    },1000)
                }else{
                    myalert.alertInfoToast(data['message']);
                }

            }
        })
    })
})