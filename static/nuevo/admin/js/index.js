jQuery(function () {
	var $container = $('.cursos');

	$container.isotope({
		itemSelector: '.curso'
	});

	$('.curso a[data-filter]').toggle(function () {
		var $self = $(this),
			selector = $self.attr('data-filter');

		$self.addClass('active');

		$container.isotope({ filter: selector });
		
		return false;

	}, function () {
		var $self = $(this);

		$self.removeClass('active');

		$container.isotope({filter : ''});
		return false;
	});

	$('.add').click(function () {
		cargar_overlay($(this).attr('href')+' #add_form');

		return false;
	})

	$('.edit').click(function () {
		cargar_overlay($(this).attr('href')+' #edit_form');

		return false;
	})

	$('#add_form').live('submit', function () {
		close_overlay();

		return false;
	});

	$('#edit_form').live('submit', function () {
		close_overlay();

		return false;
	});

	/* drag de imagenes */

	function ignore(e) {
		var event = typeof e.originalEvent != 'undefined' ? e.originalEvent : e;
		if (event.stopPropagation) event.stopPropagation();
		if (event.preventDefault) event.preventDefault();
	}

	$('.drop')
		.live('dragenter', ignore).live('drop', function (e) {
			e = (e && e.originalEvent ? e.originalEvent: window.event) || e;
			ignore(e);

			var files = (e.files || e.dataTransfer.files), 
				$self = $(this),
				$img  = $self.find('img'),
				$form = $self.closest('form');

			var str = "";
			for (var i = 0; i < files.length; i++) {
				(function(i){
					var reader = new FileReader();
					reader.onload = function (event) {
						$form.find('input[name="imagen"]').val(event.target.result);
						$form.find('input[name="imagen_filename"]').val(files[i].name);
						$img.attr('src', event.target.result);
					};
					reader.readAsDataURL(files[i]);
				})(i);
			}
	});

	/* popup de edicion */
	var $overlay = $('.overlay'), 
		$panel = $overlay.find('.panel');

	$('a.back').live('click', close_overlay);
	function close_overlay() {
		$overlay.fadeOut(function () {
			$('body').removeClass('overlayed');
			$panel.removeClass('loaded').html('');
		});

		return false;
	}

	function open_overlay() {
		$overlay.fadeIn(function () {
			$('body').addClass('overlayed');
		});
	}

	function cargar_overlay(url) {
		open_overlay();	

		setTimeout(function () {
			$panel.load(url, function () { $(this).addClass('loaded'); });
		}, 10);
	}
});