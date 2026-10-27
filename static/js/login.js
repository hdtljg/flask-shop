$(function (){
    $('#submit').click(function (){

        var username=$('#username').val()
        var pwd=$('#pwd').val()

        $.ajax({
            url:'api/login',
            type:'post',
            data:{username:username,password:pwd},
            // dataType:'text',
            dataType:'json',  // 修改为json格式
            success:function (data){
                console.log("请求成功",data)
                if (data.status!='success'){
                    $('#msg span').text("用户名或密码错误")
                }else{
                      // 根据用户角色跳转到不同页面
                    if (data.role === 'admin') {
                        window.location.href="/admin_dashboard";
                    } else {
                        window.location.href="/index";
                    }
                    // window.location.href="/index";
                }
            },
            error:function (e){
                console.log("请求失败")
            }
        })
    })
})