/**
 * Created by Administrator on 2017/4/7.
 */

// 添加板块执行事件
$(function () {
    $('#add-boards-btn').click(function (event) {
        event.preventDefault();
        myalert.alertOneInput({
            'title':'添加板块',
            'placeholder':'请输入版块名称',
            'confirmCallback':function (inputValue) {
                myajax.post({
                    'url':'/add_board/',
                    'data':{
                        'name':inputValue,
                    },
                    'success':function (data) {
                        if (data['code']==200){
                            myalert.close();
                            setTimeout(function () {
                                myalert.alertSuccessToast('添加成功！');
                            },1000);
                            setTimeout(function () {
                                window.location.reload();
                            },2000);
                        }else{
                            myalert.alertErrorToast(data['message']);
                        }
                    }
                })
            }
        })
    })
});


//编辑板块执行事件

$(function () {
   $('.edit-board-btn').click(function (event) {
       event.preventDefault();
        var board_id = $(this).attr('data-board-id');
        var board_name = $(this).attr('data-board-name');
        if(!board_id){
            myalert.alertErrorToast('板块不存在，无法编辑！');
        }
        myalert.alertOneInput({
            'title':'编辑板块',
            'placeholder':board_name,
            'confirmCallback':function (inputValue) {
                 myajax.post({
                    'url':'/edit_board/',
                    'data':{
                        'board_id':board_id,
                        'name':inputValue,
                    },
                    'success':function (data) {
                        if (data['code']==200){
                            myalert.close();
                            setTimeout(function () {
                                myalert.alertSuccessToast('编辑成功！');
                            },1000);
                            setTimeout(function () {
                                window.location.reload();
                            },2000);
                        }else{
                            myalert.alertErrorToast(data['message']);
                        }
                    }
                })
            }
        })
   })
});

// 删除板块
$(function () {
   $('.delete-board-btn').click(function (event) {
       event.preventDefault();
        var board_id = $(this).attr('data-board-id');
        if(!board_id){
            myalert.alertErrorToast('板块不存在，无法删除！');
        }
        myalert.alertConfirm({
            'msg':'确认删除该板块？',
            'confirmCallback':function () {
                 myajax.post({
                    'url':'/delete_board/',
                    'data':{
                        'board_id':board_id,
                    },
                    'success':function (data) {
                        if (data['code']==200){
                            myalert.close();
                            setTimeout(function () {
                                myalert.alertSuccessToast('删除成功！');
                            },1000);
                            setTimeout(function () {
                                window.location.reload();
                            },2000);
                        }else{
                            myalert.alertErrorToast(data['message']);
                        }
                    }
                })
            }
        })
   })
});
