$(function(){//ready
    //code

    $('.input_item').blur(function (e) { 
       
        var  this_obj = $(this);

        var input_value = this_obj.val();
        var id = this_obj.attr("id");

        this_obj.next().text("");

        switch (id) {
            case 'username':
                if (!isUername(input_value)) {

                     this_obj.next().text("请按要求输入邮箱地址");
                     this_obj.next().css('color','red')   
                } 
                 
                break;
            case 'tel':
                if (!isTel(input_value)) {

                     this_obj.next().text("请输入中国大陆手机号码");
                     this_obj.next().css('color','red')   
                } 
                
                break;
        
            default:
                break;
        }
    });

    $('#yes_btn').click(function (e) {

        var username = $('#username').val()
        var tel = $('#tel').val()

        if(isUername(username) && isTel(tel)){
            $('#userForm').submit();
        }


    });






    $('.edit_data').click(function(){

        $("#wrap").css("display",'block')

        var user_id= $(this).attr('id');
        //请求session数据
        $.get('/get_user_session',{id:user_id},function (data){
            console.log(data)
            $('#user_id').val(data.id)
            $('#username').val(data.username)
            $('#tel').val(data.telephone)
            var url_str='/change_data?id='+data.id;
            $('#userForm').attr('action',url_str)

        })

    })

    $('.close').click(function(){
        $("#wrap").css("display",'none')
    })
    $('#cancle_btn').click(function(){
        $("#wrap").css("display",'none')
    })

})

