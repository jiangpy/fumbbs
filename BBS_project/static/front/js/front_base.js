/**
 * Created by Administrator on 2017/4/14.
 */


$(function () {
   var url =  window.location.href;
   if(url.indexOf('addpost')>=0){
        $('.home-page').removeClass('active');
   };
   if(url.indexOf('postdetail')>=0){
        $('.home-page').removeClass('active');
   };
   if(url.indexOf('comment')>=0){
        $('.home-page').removeClass('active');
   };
    if(url.indexOf('profile')>=0){
        $('.home-page').removeClass('active');
    }
});
