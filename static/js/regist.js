/*************************************************
作者： 牛迁迁
小组：
说明：短信验证所用到的JS方法，此实例仅作为Demo，一些验证暂时省略。
创建日期：2015年8月11日 17:55:40
版本号：V1.0.0
**********************************************/

window.onload = function () {




    //提交注册按钮

    $("#submit").click(function () {
        var username = $("#username").val();
        var password = $("#password").val();

        if(username == ''){
            $("#usernameTip").html("<font color='red'>用户名不能为空</font>");
            return;
        }else{
            $("#usernameTip").html("");
        }
        if(password == ''){
            $("#passwordTip").html("<font color='red'>密码不能为空</font>");
            return;
        }else{
            $("#passwordTip").html("");
        }


       // alert(password+'+++'+username)

        // 向后台发送处理数据
        $.ajax({
            url: "/login/checked",
            data: {password: password, username:username},
            type: "POST",
            dataType: "json",
            success: function (data) {
                data = eval("("+data+")");
                if (data.result == 400 ) {
                    $("#sessions").show()
                    $("#sessions").text("用户名密码错误，请重新输入！");
                    return;
                }else {
                    window.location.href = data.result;
                }
            }
        });
    });
}