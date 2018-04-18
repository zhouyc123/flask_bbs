$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();


        // event.preventDefault() 是阻止按钮默认的提交表单事件
        var oldpwdE = $("input[name=oldpwd]");
        var newpwdE = $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd = oldpwdE.val();
        var newpwd = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        zlajax.post({
                'url' : '/cms/resetpwd/',
                'data': {
                    'oldowd':oldpwd,
                    'newpwd':newpwd,
                    'newpwd2':newpwd2

                },
                'success':function (data) {
                    // console.log(data)
                    if(data['code'] == 200){
                        zlalert.alertSuccessToast("恭喜密码修改成功！");
                    }else {
                        var message = data['message'];
                        zlalert.alertInfoToast(message);
                    }
                },
                'fail':function (error) {
                    // console.log(error)
                    zlalert.alertNetworkError();
                }
            })
    });
});