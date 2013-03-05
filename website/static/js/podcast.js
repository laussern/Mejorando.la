require([
	'jquery',
	'vendor/audio5'],
	function ($, Audio5js){
    var podcasts = {
      click: function(e){
        var $button = $(this);        
        // if not playing, pause all players and play this
        if (!$button.data('playing')) {
          $('.icon-stop').trigger('pause.audio');
          $(this).trigger('play.audio');
        // if playing, only pause this
        } else {
          $(this).trigger('pause.audio');
        }
      },
      play: function(e) {
        var $button = $(this);
        var playing = $button.data('playing');
        var podcast = $button.data('podcast');
        
        if (playing)
          return;

        if(!podcast){
          podcast = new Audio5js({
            ready: function () {
              this.load($button.attr('data-url'));
              this.play();
            }
          });
          
          $button.data('podcast', podcast);
        }
        
        podcast.play();
        $button.removeClass('icon-play').addClass('icon-stop').text('Pausar');
        $button.data('playing', true);
      },
      pause: function(e) {
        var $button = $(this);
        var playing = $button.data('playing');
        var podcast = $button.data('podcast');
        
        if (!playing || !podcast)
          return;
        
        podcast.pause();
        $button.removeClass('icon-stop').addClass('icon-play').text('Reanudar');
        $button.data('playing', false);
      },
      init: function(){
        $('.play')
          .on('click', podcasts.click)
          .on('play.audio', podcasts.play)
          .on('pause.audio', podcasts.pause);
      }
    };

    podcasts.init();

	
	}
);


