jQuery(function ($) {
    (function youtubeCounter() {
        // youtube video views
        var count = $.cookie('youtube_views');
        var $youtube = $('.btn_youtube');
        if (count) {
            $youtube.find('.count').text(count);
        }
        else {
            $.getJSON('https://gdata.youtube.com/feeds/api/users/' + $youtube.data('id') + '?alt=json&callback=?', function (data) {
                var count = formatNumber(data.entry['yt$statistics'].subscriberCount);
                $.cookie('youtube_views', count);
                $youtube.find('.count').text(count);
            });
        }
    })();
});