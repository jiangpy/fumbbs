/**
 * Created by Administrator on 2017/3/18.
 */


$(function () {
    $('#resetpwd_btn').click(function (event) {
        event.preventDefault()
        var oldpwdInput = $('input[name=oldpwd]');
        var newpwdInput = $('input[name=newpwd]');
        var newpwdRepeatInput = $('input[name=newpwdrepeat]');

        var oldpwd = oldpwdInput.val();
        var newpwd = newpwdInput.val();
        var newpwdRepeat = newpwdRepeatInput.val();
        myajax.post({
            'url':'/resetpwd/',
            'data':{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'newpwdrepeat':newpwdRepeat
            },
            'success':function (data) {
                if(data['code']==200){
                    oldpwdInput.val('');
                    newpwdInput.val('');
                    newpwdRepeatInput.val('');
                    myalert.alertSuccessToast('恭喜！密码修改成功！')
                }else{
                    myalert.alertErrorToast(data['message'])
                }
            },
            'error':function (errors) {
                myalert.alertNetworkError()
            }
        })
    })
})