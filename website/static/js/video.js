define(['jquery', 'vendor/audio5'], function ($, Audio5js) {
    var podcast;

    $('.play').on('click',function(e){
        var $self = $(this);

        if(!podcast){
          podcast = new Audio5js({
            ready: function () {
              this.load($self.attr('data-url'));
              this.play();
            }
          });

          $self.removeClass('icon-play').addClass('icon-stop').text('Pausar');
          activo = false;

        } else {

          if(podcast.playing){
            podcast.pause();
            $self.removeClass('icon-stop').addClass('icon-play').text('Reanudar');

          } else{
            podcast.play();
            $self.removeClass('icon-play').addClass('icon-stop').text('Pausar');
          }
        }
    });
});