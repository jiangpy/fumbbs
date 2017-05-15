/**
 * Created by Administrator on 2017/3/17.
 */


$(function () {
    $('.btn-lg').click(function (event) {
        event.preventDefault();
        var email = $('#inputEmail').val();
        var password = $('#inputPassword').val();
        var remember = $('input[name=remember]').is(':checked')
        if (!remember){
            remember = 0
        }else{
            remember = 1
        }
        myajax.post({
            'url':'/login/',
            'data':{
                'email':email,
                'password':password,
                'remember':remember,
            },
            'success':function (data) {
                if(data['code']==200){
                    window.location='/'
                }else{
                    var message = data['message']
                    $('#error-info').text(message)
                }
            },
            'fail':function (error) {
                console.log(error)
            }
        })

    })
})