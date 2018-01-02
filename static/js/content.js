/*************************************************
作者：
小组：
说明：短信验证所用到的JS方法，此实例仅作为Demo，一些验证暂时省略。
创建日期：
版本号：V
**********************************************/

window.onload = function () {




    //提交注册按钮

    $("#submit").click(function () {
        var content = $("#content").val();
        if(content == ''){
            $("#contentTip").html("<font color='red' size='3'>内容不能为空</font>");
            return;
        }else{
            $("#contentTip").html("");
        }

        $("#submit").attr("disabled", "true"); //关闭按钮
        // 向后台发送处理数据
        $.ajax({
            url: "/update/",
            data: {content: content},
            type: "POST",
            dataType: "json",
            success: function (data) {
                data = eval("("+data+")");
                if (data.result == 400){
                     alert("登录超时，请刷新页面，登录后再提交")
                     //window.location.reload();
                     return;
                }else if (data.result == 401) {
                    $("#contentTip").html("data.item路径不对,必须以<font color='red' size='3'>data.path</font>其中的一项开头".replace(/data.item/, data.item).replace(/data.path/,data.path));
                    $("#submit").removeAttr("disabled");// 启用按钮
                    return;
                } else if (data.result == 402) {
                    $("#contentTip").html("<font color='red' size='3'>data.item文件不存在，请确认了再发布</font>".replace(/data.item/, data.item));
                    $("#submit").removeAttr("disabled");// 启用按钮
                    return;
                }else if (data.result == 403) {
                    $("#contentTip").html("<font color='red' size='3'>服务器错误，请联系管理员</font>");
                    return;
                }else if (data.result ==404){
                   $("#contentTip").html("<font color='red' size='3'>data.item路径错误，危险！！！</font>".replace(/data.item/, data.item));
                   $("#submit").removeAttr("disabled");// 启用按钮
                } else{
                    alert("更新成功");
                    return;
                }
            }
        });
    });



}