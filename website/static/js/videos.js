require([
    'jquery',
    'vendor/jquery.lazyload'],
    function ($, youtube, countdown) {
        $("img").lazyload({
            effect: 'fadeIn',
            threshold: 200
        });
});