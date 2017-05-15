/**
 * Created by Administrator on 2017/4/27.
 */

//头像上传
$(function () {
    var upload_btn = $('#avater-img');
    var domain = 'http://oo78d7e19.bkt.clouddn.com/';
    var uploader = Qiniu.uploader({
        runtimes: 'html5,flash,html4',      // 上传模式，依次退化
        browse_button: 'upload-avater-btn',         // 上传选择的点选按钮，必需
        uptoken_url: '/get_qiniu_token/',         // Ajax请求uptoken的Url，强烈建议设置（服务端提供）
        get_new_uptoken: false,             // 设置上传文件的时候是否每次都重新获取新的uptoken
        domain: domain,     // bucket域名，下载资源时用到，必需
        max_file_size: '100mb',             // 最大文件体积限制
        flash_swf_url: 'path/of/plupload/Moxie.swf',  //引入flash，相对路径
        max_retries: 3,                     // 上传失败最大重试次数
        dragdrop: false,                     // 开启可拖曳上传
        chunk_size: '4mb',                  // 分块上传时，每块的体积
        auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
        log_level: 5, //log级别
        filters:{
            mime_types:[
                {title : "Image files", extensions : "jpg,gif,png"},
        ]},
        init: {
            'FilesAdded': function(up, files) {
                // 文件添加时，处理相关的事情
            },
            'BeforeUpload': function(up, file) {
                // 每个文件上传前，处理相关的事情
            },
            'UploadProgress': function(up, file) {

                // 每个文件上传时，处理相关的事情

            },
            'FileUploaded': function(up, file, info) {

                var fileurl = domain+file['name'];
                // 每个文件上传成功后，处理相关的事情
                var imgTag = $('#avater-img');
                imgTag.attr('src',fileurl);

            },
            'Error': function(up, err, errTip) {
                   //上传出错时，处理相关的事情

            },
            'UploadComplete': function() {
                   //队列文件处理完毕后，处理相关的事情
            }
        }
    });
});


// 修改邮箱事件
$(function () {
   $('.email-btn').click(function (event) {
       event.preventDefault();
   })
});




// 保存个人信息事件
$(function () {
    $('#submit-btn').click(function (event) {
        event.preventDefault();
        var username = $('input[name=username]').val();
        var realname = $('input[name=realname]').val();
        var avater = $('#avater-img').attr('src');
        var email = $('input[name=email]').val();
        var qq = $('input[name=qq]').val();
        var signature = $('textarea[name=signature]').val();
        var user_id = $(this).attr('data-user-id');
        var gender = parseInt($('input:radio:checked').val());
        console.log(gender);
        myajax.post({
            'url':'/account/personagesetting/'+user_id+'/',
            'data':{
                'username':username,
                'realname':realname,
                'avater':avater,
                'email':email,
                'qq':qq,
                'signature':signature,
                'user_id':user_id,
                'gender':gender,
            },
            'success':function (data) {
                if(data['code']==200){
                    myalert.alertSuccessToast('保存成功！')
                }else{
                    myalert.alertErrorToast(data['message'])
                }
            },
            'error':function (error) {
                console.log(error)
            }
        })
    })
})