/**
 * Created by Administrator on 2017/3/19.
 */


//获取邮箱验证码
$(function () {
    $('#captcha_btn').click(function (event) {
        event.preventDefault()
        var oldemail = $('input[name=oldemail]').val();
        myajax.post({
            'url':'/mail_captcha/',
            'data':{
                'oldemail':oldemail,
            },
            'success':function (data) {
                if(data['code']==200){
                    myalert.alertSuccessToast('邮件发送成功！')
                }else{
                    myalert.alertInfoToast(data['message'])
                }
            },
            'error':function (error) {
                myalert.alertNetworkError()
                console.log(error)
            }
        })
    })
})

//确认修改邮箱
$(function () {
    $('#resetemail').click(function (event) {
        event.preventDefault();
        var oldemailInput = $('input[name=oldemail]');
        var captchaInput = $('input[name=captcha]');
        var newemailInput = $('input[name=newemail]');

        var oldemail = oldemailInput.val();
        var captcha = captchaInput.val();
        var newemail = newemailInput.val();

        myajax.post({
            'url':'/resetemail/',
            'data':{
                'oldemail':oldemail,
                'captcha':captcha,
                'newemail':newemail
            },
            'success':function (data) {
                if(data['code']==200){
                    oldemailInput.val('');
                    captchaInput.val('');
                    newemailInput.val('');
                    myalert.alertSuccessToast('恭喜！邮箱修改成功！')
                }else{
                    myalert.alertInfoToast(data['message'])
                }
            },
            'error':function (error) {
                myalert.alertNetworkError()
            }
        })
    })
})

