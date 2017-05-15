/**
 * Created by Administrator on 2017/3/20.
 */

$(function () {
    var btn = $('#send-captcha-btn');
   btn.click(function (event) {
       event.preventDefault();
       // 获取手机号码
       var telephone = $('input[name=telephone]').val();

       if(!telephone){
           myalert.alertInfoToast('请输入手机号码！');
           return;
       };

       myajax.post({
           'url': '/account/sms_captcha/',
           'data':{
               'telephone':telephone,
           },
           'success':function (data) {
               if(data['code']==200){
                   myalert.alertSuccessToast('短信发送成功，请查收！');
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
                   myalert.alertInfoToast(data['message'])
               }
           },
           'error':function (error) {
               console.log(error)
           }
       })
   })
});


