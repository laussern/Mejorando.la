jQuery(function ($) {
	// contador
	var _hora, hora = $("#hora"),
		proximo = $("#proximo"),
		timestamp = parseInt(proximo.attr('data-timestamp'));

	proximo.scountdown({
		callback: function (d, h, m, s) {
			$(".dias", proximo).text(d);
			$(".horas", proximo).text(h);
			$(".minutos", proximo).text(m)
			$(".segundos", proximo).text(s)
		},
		timestamp: timestamp
	});

	_hora = new Date(timestamp);
	hora.text(_hora.toString("h:mmtt"));

	function formatNumber(rep) {
		rep = rep + ''; // coerce to string
		if (rep < 1000) {
			return rep; // return the same number
		}
		else if (rep < 5000) { // place a comma between
			return rep.charAt(0) + ',' + rep.substring(1);
		}
		else { // divide and format
			return (rep / 1000).toFixed(rep % 1000 != 0) + 'k';
		}
	}

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
	var loadiamges = function(efecto){
		$("img").lazyload({
            	effect : efecto,
            	threshold : 200
          });
	}
	if ($(window).width() >= 1000)
		loadiamges('fadeIn')
	else
		loadiamges('show')
});