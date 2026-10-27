$(function() {
    var timer = null;
    var user_data = getUserData();

    // 开始抽奖
    $("#start").click(function() {
        // 防止重复点击
        if (timer != null) {
            return;
        }

        // 添加抽奖动画
        $('#box').addClass('lottery-animation');
        $('#name').text('抽奖中...');

        // 设置定时器快速切换用户
        timer = setInterval(function() {
            getRandomUser(user_data);
        }, 50);
    });

    // 停止抽奖
    $('#stop').click(function() {
        if (timer != null) {
            clearInterval(timer);
            timer = null;

            // 移除抽奖动画，添加结果动画
            $('#box').removeClass('lottery-animation');
            $('#box').addClass('result-animation');

            // 1秒后移除结果动画，以便下次抽奖
            setTimeout(function() {
                $('#box').removeClass('result-animation');
            }, 1000);
        }
    });
});

// 获取随机用户
function getRandomUser(users) {
    if (!users || users.length === 0) {
        $('#name').text('暂无用户数据');
        return;
    }

    // 获取随机索引
    var len = users.length;
    var i = Math.floor(Math.random() * len);
    var ran_name = users[i].name || '未知用户';
    var ran_img = users[i].img || '2.jpg'; // 默认图片
    var img_src = '/img/' + ran_img;

    // 更新显示
    $('#name').text(ran_name);
    $('#touxiang').attr('src', img_src);
}

// 获取用户数据
function getUserData() {
    var users = null;
    $.ajax({
        url: '/user_info',
        type: 'post',
        dataType: 'json',
        async: false,
        success: function(data) {
            console.log("请求成功: ", data);
            users = data;
        },
        error: function(e) {
            console.log("请求失败: ", e);
            // 如果获取数据失败，提供一些模拟数据
            users = [
                {name: '张三', img: '1.jpg'},
                {name: '李四', img: '2.jpg'},
                {name: '王五', img: '3.png'},
                {name: '赵六', img: '4.jpg'},
                {name: '钱七', img: '5.png'}
            ];
        }
    });
    return users;
}