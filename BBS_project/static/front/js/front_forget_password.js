/**
 * Created by Administrator on 2017/5/6.
 */


// 发送手机验证码事件
$(function () {
    var btn = $('#captcha_btn');
    btn.click(function (event) {
        event.preventDefault();
        var telephone = $('input[name=telephone]').val();
        console.log(telephone);
        myajax.post({
            'url':'/account/get_telephone_captcha/',
            'data':{
                'telephone':telephone
            },
            'success':function (data) {
                if (data['code']==200){
                    myalert.alertSuccessToast('验证码发送成功！')
                    var timeCount = 60;
                   btn.attr('disabled','disabled');
                   btn.css('cursor','default');
                   var timer = setInterval(function () {
                       btn.text(timeCount+ ' ' + '短信已发送');
                       timeCount--;
                       if (timeCount<=0){
                           btn.text('发送验证码');
                           btn.removeAttr('disabled');
                           clearInterval(timer);
                           btn.css('cursor','pointer');
                       }
                   },1000);
                }else {
                    myalert.alertErrorToast(data['message'])
                }
            },
        })
    })
});


//密码修改执行事件：
$(function () {
   $('#btn-submit').click(function (e) {
       e.preventDefault();
       var telephoneInput = $('input[name=telephone]');
       var tel_captchaInput = $('input[name=tel_captcha]');
       var new_passwordInput = $('input[name=new_password]');
       var repe_new_passwordInput = $('input[name=repe_new_password]');

       var telephone =  telephoneInput.val();
       var tel_captcha = tel_captchaInput.val();
       var new_password = new_passwordInput.val();
       var repe_new_password = repe_new_passwordInput.val();
       console.log('new:'+new_password);
       console.log('repe:'+repe_new_password);

       myajax.post({
           'url':'/account/forget_password/',
           'data':{
               'telephone':telephone,
               'tel_captcha':tel_captcha,
               'new_password':new_password,
               'repe_new_password':repe_new_password
           },
           'success':function (data) {
               if(data['code']==200){
                   myalert.alertSuccessToast('密码修改成功！')
               }else{
                   myalert.alertErrorToast(data['message'])
               }
           }
       })
   })
});