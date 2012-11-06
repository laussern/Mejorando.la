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

	$('.add-curso').click(function () {
		mainpopup.load($(this).attr('href')+' #content');

		return false;
	})

	$('.edit-curso').click(function () {
		mainpopup.load($(this).attr('href')+' #content', function () {
			var popup2 = new Popup('.popup2');

			$('.add-docente').click(function () {
				popup2.load($(this).attr('href') + ' #add_docente_form');

				return false;
			});

			$('.edit-docente').click(function () {
				popup2.load($(this).attr('href') + ' #edit_docente_form');

				return false;
			});

			$('.add-dia').click(function () {
				popup2.load($(this).attr('href') + ' #add_dia_form');

				return false;
			});

			$('.edit-dia').click(function () {
				popup2.load($(this).attr('href') + ' #edit_dia_form');

				return false;
			});

			function done2(r) {
				if(r.vars && r.vars.id) {
					var model = r.vars;

					switch(model.tipo) {
						case 'docente':
							var $docente = $('.docente[data-id="'+model.id+'"]');

							$docente.find('.docente-twitter').text('@'+model.twitter);
							$docente.find('.docente-imagen').attr('src', model.imagen)
							break;
					}
				}

				popup2.hide();
			}

			/* AGREGAR Y EDITAR DOCENTES */
			$('#add_docente_form').live('submit', function () {
				var $self = $(this);

				notif.hide();
				validate_basic($self);

				// validate imagen drop 
				if($self.find('input[name="imagen"]').val().match(/^\s*$/)) $self.find('.drop-docente').addClass('error')
				else $self.find('.drop-docente').removeClass('error')

				send_form($self, done2);

				return false;
			});

			$('#edit_docente_form').live('submit', function () {
				var $self = $(this);

				notif.hide();
				validate_basic($self);

				send_form($self, done2);

				return false;
			});

			/* AGREGAR Y EDITAR DIAS */
			function admin_docente() {
				var $self = $(this);

				notif.hide();
				validate_basic($self);

				send_form($self, done2);

				return false;
			}

			$('#add_dia_form').live('submit', admin_docente);
			$('#edit_dia_form').live('submit', admin_docente);

		});

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

	function send_form($form, done) {
		if($form.find('input.required.error, .drop.error, textarea.required.error').size() > 0) {
			notif.err('Errores en los campos.');

			return false;
		}

		notif.show('Enviando...')
		$.post($form.attr('action'), $form.serialize(),
			function (r) {
				try {
					var d = JSON.parse(r);
				} catch(err) { }

				notif.hide();

				if(r == 'OK' || (typeof d != 'undefined' && d.status == 'ok')) {
					if(done) done(d);
					else mainpopup.hide();
				} else {
					notif.err('Error, porfavor vuelve a intentarlo más tarde.');
				}
		});

		return true;
	}

	$('#add_curso_form').live('submit', function () {
		var $self = $(this);

		notif.hide();
		validate_basic($self)

		// validate imagen drop 
		if($self.find('input[name="imagen"]').val().match(/^\s*$/)) $self.find('.drop-curso').addClass('error')
		else $self.find('.drop-curso').removeClass('error')

		send_form($self);

		return false;
	});

	$('#edit_curso_form').live('submit', function () {
		var $self = $(this);
		
		notif.hide();
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
	var Popup = function (selector) {
		var $self 	 = $(selector),
			$overlay = $self.find('.overlay');

		this.hide = function () {
			var $panel 	 = $self.find('.panel'),
				$overlay = $self.find('.overlay');

			$overlay.addClass('fadeOut');
			$panel.addClass('fadeOut');

			setTimeout(function () {
				$self.removeClass('show');
				$overlay.removeClass('fadeOut').removeClass('fadeIn');
				$panel.removeClass('fadeOut').removeClass('fadeIn');
				$panel.html('');
			}, 1010);

			return false;
		};

		this.show1 = function (two) {
			var $panel 	 = $self.find('.panel');

			$self.addClass('show');
			$overlay.addClass('fadeIn');

			if(two) this.show2();
		};

		this.show2 = function () {
			var $panel 	 = $self.find('.panel');

			$panel.addClass('fadeIn');
		};

		this.load = function (url, loaded) {
			var $panel 	 = $self.find('.panel');

			this.show1();

			var self = this;
			setTimeout(function () { 
				$panel.load(url, function () {
					self.show2();
					$panel.find('a.back').click(self.hide);

					if(loaded) loaded();
				});
			}, 10);
		};

		// botones para cerrar
		$overlay.click(this.hide);
	};

	var mainpopup = new Popup('#mainpopup');


	var notif = {
		show: function (str) {
			$('.notif').html(str);
		}, 
		err: function (str) {
			$('.notif').html('<span class="error">*</span>'+str);
		},
		hide: function () {
			$('.notif').html('')
		}
	};
});