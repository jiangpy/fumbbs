/**
 * Created by Administrator on 2017/4/20.
 */

// 初始化富文本编辑器
$(function () {
    var editor = new wangEditor('editor');
    editor.create();
    window.editor = editor;
});
// 图片视频上传
$(function () {
    var up_progress = $('#prcent_progress');
    var progress = $('.progress');
    var upload_btn = $('#upload-btn');
    var domain = 'http://oo78d7e19.bkt.clouddn.com/';
    var uploader = Qiniu.uploader({
        runtimes: 'html5,flash,html4',      // 上传模式，依次退化
        browse_button: 'upload-btn',         // 上传选择的点选按钮，必需
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
                {title:"Video files",extensions : "flv,mpg,mpeg,avi,wmv,mov,asf,rm,rmvb,mkv,m4v,mp4"},
                {title : "Image files", extensions : "jpg,gif,png"},
        ]},
        init: {
            'FilesAdded': function(up, files) {
                var progress = $('.progress');
                progress.show();
                upload_btn.button('loading');
            },
            'BeforeUpload': function(up, file) {
                // 每个文件上传前，处理相关的事情
            },
            'UploadProgress': function(up, file) {

                // 每个文件上传时，处理相关的事情
                //处理进度条
                up_progress.width(file['percent']+'%');
                up_progress.attr('aria-valuenow',file['percent']);
                up_progress.text(file['percent']+'%');
            },
            'FileUploaded': function(up, file, info) {

                // 每个文件上传成功后，处理相关的事情
                var filename = domain+file['name'];
                if(file.type.indexOf('video') >=0 ){
                    //上传视频
                    var videoTag = '<video src="" width="320" height="240" controls><source src='+filename+'></video>';
                    window.editor.$txt.append(videoTag);
                }else{
                    //上传图片
                    var imgTag = '<img src='+filename+'>';
                    window.editor.$txt.append(imgTag);
                }
                progress.css('display','none')
                up_progress.width('0%');
                up_progress.attr('aria-valuenow','0');
                up_progress.text('0'+'%');
                upload_btn.button('reset');
            },
            'Error': function(up, err, errTip) {
                   //上传出错时，处理相关的事情
                if(err['code']=='-600'){
                    var error = '上传的视频不能大于100M';
                    $('#error-info').text(error);
                }

            },
            'UploadComplete': function() {
                   //队列文件处理完毕后，处理相关的事情
            }
        }
    });
});