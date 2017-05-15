/**
 * Created by Administrator on 2017/4/5.
 */

//异步刷新验证码
$(function () {
    var captcha_img = $('.graph_captcha');
    captcha_img.click(function (event) {
        event.preventDefault();
        var oldsrc = captcha_img.attr('src');
        var newsrc = myparam.setParam(oldsrc,'xx',Math.random());
        captcha_img.attr('src',newsrc);
    });
});