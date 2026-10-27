// 图片轮播功能实现
window.onload = function() {
    // 获取轮播相关元素
    const banner = document.querySelector('.banner');
    const images = banner.querySelectorAll('img');
    const dots = banner.querySelectorAll('.dot');

    // 设置轮播参数
    let currentIndex = 0;
    const totalImages = images.length;
    const intervalTime = 3000; // 3秒切换一次
    let slideInterval;

    // 初始化轮播图样式
    function initCarousel() {
        // 设置所有图片初始样式
        images.forEach((img, index) => {
            img.style.position = 'absolute';
            img.style.top = '0';
            img.style.left = '0';
            img.style.opacity = index === 0 ? '1' : '0';
            img.style.transition = 'opacity 0.5s ease-in-out';
        });

        // 初始化第一个点为激活状态
        updateDots();

        // 开始自动轮播
        startAutoSlide();

        // 添加点击事件
        addEvents();
    }

    // 更新指示器
    function updateDots() {
        dots.forEach((dot, index) => {
            dot.style.width = '10px';
            dot.style.height = '10px';
            dot.style.borderRadius = '50%';
            dot.style.backgroundColor = index === currentIndex ? '#ff5000' : '#ccc';
            dot.style.display = 'inline-block';
            dot.style.margin = '0 5px';
            dot.style.cursor = 'pointer';
            dot.style.transition = 'background-color 0.3s ease';
        });
    }

    // 切换到指定图片
    function showImage(index) {
        images.forEach((img, i) => {
            img.style.opacity = i === index ? '1' : '0';
        });
        currentIndex = index;
        updateDots();
    }

    // 下一张图片
    function nextImage() {
        let nextIndex = (currentIndex + 1) % totalImages;
        showImage(nextIndex);
    }

    // 上一张图片
    function prevImage() {
        let prevIndex = (currentIndex - 1 + totalImages) % totalImages;
        showImage(prevIndex);
    }

    // 开始自动轮播
    function startAutoSlide() {
        slideInterval = setInterval(nextImage, intervalTime);
    }

    // 停止自动轮播
    function stopAutoSlide() {
        clearInterval(slideInterval);
    }

    // 添加事件监听
    function addEvents() {
        // 鼠标悬停时停止轮播
        banner.addEventListener('mouseenter', stopAutoSlide);
        // 鼠标离开时继续轮播
        banner.addEventListener('mouseleave', startAutoSlide);

        // 点击指示器切换图片
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showImage(index);
            });
        });

        // 为轮播图添加左右点击切换功能
        banner.addEventListener('click', function(e) {
            // 判断点击位置，左侧点击上一张，右侧点击下一张
            const bannerWidth = banner.offsetWidth;
            const clickX = e.clientX - banner.getBoundingClientRect().left;

            if (clickX < bannerWidth / 2) {
                prevImage();
            } else {
                nextImage();
            }
        });
    }

    // 初始化轮播图
    initCarousel();
};
