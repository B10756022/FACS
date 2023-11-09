const swiper = new Swiper(".swiper", {
        // Optional parameters
        direction: "horizontal",
        // 讓速度變成1.5秒
        speed: 1000,
        loop: true,
        //   自動撥放
        autoplay: {
          delay: 1500,
        },
        //  切換模式:漸層
        effect: "fade",
        followFinger: "true",
        mousewheel: true,
        //  allowTouchMove:false,

        // If we need pagination
        pagination: {
          el: ".swiper-pagination",
        },

        //   // Navigation arrows 箭頭 先不使用
        //   navigation: {
        //     nextEl: '.swiper-button-next',
        //     prevEl: '.swiper-button-prev',
        //   },

        //   // And if we need scrollbar 滑動滾輪條 先不用
        //   scrollbar: {
        //     el: '.swiper-scrollbar',
        //   },
      });