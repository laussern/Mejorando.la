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

	/* formularios */
	function validate_basic($form) {
		$form.find('input.required, textarea.required').each(function () {
			var $self = $(this);

			$self.removeClass('error');

			if($self.val().match(/^\s*$/)) $self.addClass('error');
		});
	}

	function send_form($form) {
		if($form.find('input.required.error, .drop.error, textarea.required.error').size() > 0) {
			console.log($form);
			error_overlay('Errores en los campos.');

			return false;
		}

		send_overlay();
		$.post($form.attr('action'), $form.serialize(),
			function (r) {
				unsend_overlay();

				if(r == 'OK') {
					close_overlay();
				} else {
					error_overlay('Error, porfavor vuelve a intentarlo más tarde.');
				}
		});

		return true;
	}

	$('#add_form').live('submit', function () {
		var $self = $(this);

		notif_overlay('');
		validate_basic($self)

		// validate imagen drop 
		if($self.find('input[name="imagen"]').val().match(/^\s*$/)) $self.find('.drop-curso').addClass('error')
		else $self.find('.drop-curso').removeClass('error')

		send_form($self);

		return false;
	});

	$('#edit_form').live('submit', function () {
		var $self = $(this);
		
		notif_overlay('');
		validate_basic($self)

		send_form($self);

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
		$panel 	 = $overlay.find('.panel');

	$('a.back').live('click', close_overlay);
	function close_overlay() {
		$overlay.fadeOut(function () {
			$('body').removeClass('overlayed');
			$panel.removeClass('loaded').html('');
		});

		return false;
	}

	function notif_overlay(str) {
		$panel.find('.notif').html(str);
	}

	function error_overlay(str) {
		notif_overlay('<span class="error">*</span>'+str);
	}

	function send_overlay() { 
		notif_overlay('Enviando...'); 
		$panel.addClass('sending'); 
	}

	function unsend_overlay() { 
		notif_overlay('');
		$panel.removeClass('sending'); 
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