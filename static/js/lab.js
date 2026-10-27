// // 执行完成才加载这个代码
// // window.onload=function(){
// //     //code
// //     //jq code
// // }

// // readiy预加载，同步解析
// $(function(){
//     //code
//     // document.getElementById('username')

//     var obj= document.getElementById('username');
//     var in_obj=$('.input_item')
//     // var in_obj=$('#username')

//     boj.style.borderColor='red'

//     in_obj.css('border-color','green')

//     // in_obj.css{
//     //     'border-color','green',
//     //     'color','red'
//     // }
//     var objs=document.getElementsByClassName('input_item')


// })
$(function(){
    $('.input_item').focus(function(e){
        //先确定是谁的焦点事件源

        var this_obj=$( this )
        var id=this_obj.attr("id");

        switch (id) {
            case 'username':
                this_obj.next().css('color','#9e9e9e')
                this_obj.next().text("用户名为6－18位数字、字母、下划线字符，需要以字母开头")
                break;

            case 'password':
                this_obj.next().css('color','#9e9e9e')
                this_obj.next().text("密码为4－18位数字、字母、下划线字符")
                break;

            case 'tel':
                this_obj.next().css('color','#9e9e9e')
                this_obj.next().text("可通过手机号找回密码")
                break;



            default:
                break;
        }
    })

     $('.input_item').blur(function(e){
        //先确定是谁的焦点事件源

        var this_obj=$( this )

        var input_value=this_obj.val();

        var id=this_obj.attr("id");
      this_obj.next().text("")
        switch (id) {
            case 'username':
                // this_obj.next().text("用户名为6－18位数字、字母、下划线字符，需要以字母开头")
                if(!isUername(input_value)){
                    this_obj.next().text("请按要求输入用户名");
                    this_obj.next().css('color','red');
                }
                // var reg=/^[a-zA-Z]\w{5,17}$/;
                // if (!reg.test(input_value)) {
                //       this_obj.next().text("请要求输入邮箱地址")
                //       this_obj.next().css('color','red')
                // }
                break;

            case 'password':
               if(!isPassword(input_value)){
                    this_obj.next().text("请按要求输入密码");
                    this_obj.next().css('color','red');
                }
                break;

            case 'tel':
                 if(!isTel(input_value)){
                    this_obj.next().text("请按要求输入中国大陆手机号码");
                    this_obj.next().css('color','red');
                }


                break;



            default:
                break;
        }
    })
   $('#reg_btn').click(function (e) {
        var username = $('#username').val();
        var tel = $('#tel').val();
        var password = $('#password').val();
        var isAgree = $('#service').is(':checked'); // 检查是否同意条款

        if(isUername(username) && isTel(tel) && isPassword(password)) {
            if (!isAgree) {
                alert('请同意服务条款！');
                return;
            }

            // 手动提交表单
            $('#userForm').submit();
        }
   });



    $('#psd_icon').click(function (e) {
        // e.preventDefault();
        var type=$('#password').attr('type');
        if (type=='password') {

            $(this).css('background-image','url(../img/eye.png)')
            $('#password').attr('type','text');
        } else {
            $(this).css('background-image','url(../img/noeye.png)')
            $('#password').attr('type','password');
        }

    });
})