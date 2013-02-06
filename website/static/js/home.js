require([
    'jquery',
    'lib/youtube',
    'lib/countdown',
    'vendor/jquery.lazyload'],
    function ($, youtube, countdown) {
        youtube.boot();
        countdown.boot();

        $("img").lazyload({
            effect: 'fadeIn',
            threshold: 200
        });
});