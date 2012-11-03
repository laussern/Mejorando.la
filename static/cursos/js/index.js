jQuery(function ($) {
	// pestañas
	+function () {
		if($(window).width() < 1000) return;

		var $tabs = $('#tabs').addClass('js'), 
			$tab  = $tabs.find('.tab').hide(), 
			$sel  = $tabs.find('.selector');

		$(window).resize(function () {
			if($(window).width() < 1000) $tabs.removeClass('js');
			else $tabs.addClass('js');
		}); 

		// mostrar los primeros
		$sel.first().addClass('active');
		$tab.first().fadeIn();

		$sel.mouseenter(function () {
			var $self = $(this);

			// ocultar los viejos
			$sel.filter('.active').removeClass('active');
			$tab.stop(true, true).fadeOut(); 

			// mostrar los correctos
			$self.next('.tab').stop(true, true).fadeIn();
			$self.addClass('active');
		});
	}();

	// funcionalidad de pago
	+function () {
		var $screens = $('.screens'), $screen = $screens.find('.screen'), $status = $('#pago-status');

		// calculo de precios
		var quantity=1;

		var $buyform  = $('#buy-form'), 
			$quantity = $buyform.find('input[name="quantity"]');

		// agregar o restar numero de asistentes
		$('.pago-count a').live('click', function () {
			var $self = $(this);

			if($self.is('.pago-mas')) {
				quantity++;
			} else {
				if(quantity == 1) return;
				quantity--;
			}

			$quantity.val(quantity);
			$('.pago-num').html(quantity);

			//calculate();
		});

		// ir al siguiente paso
		$('.pago-btns .next').live('click', pago_next);

		$buyform.submit(function () {

			if(!validates(true)) {
				return notice('Errores en los campos.')			
			}

			Stripe.createToken({
				number   : $buyform.find('.card-number').val(),
				cvc      : $buyform.find('.card-cvc').val(),
				exp_month: $buyform.find('.card-expiry-month').val(),
				exp_year : $buyform.find('.card-expiry-year').val()
			}, function (status, response) {	
				if(response.error) {
					notice(response.error.message);
				} else {
					$buyform.find('input[name="stripeToken"]').val(response.id);

					$.post($buyform.attr('action'), $buyform.serialize(), registro);
				}
			});

			return false;
		})

		$('.pago-btns .cancel').live('click', function () { 
			$('.screen.active').removeClass('active');
			$screen.first().addClass('active');
		});

		function pago_next() {
			var $cur = $('.screen.active');

			$cur.removeClass('active')
			$cur.next('.screen').addClass('active');
		}

		function registro(r) {
			if(r == 'OK') {
				$status.addClass('success').html(':) Felicidades');
				$screens.html('<div class="final"><p>Ya estás listo para asistir a este curso:</p><h1>'+config.nombre+'</h1><div class="pago-links"><p>Te invitamos a saber más de nuestros</p><a href="http://mejorando.la/cursos" target="_blank"><button>Cursos</button></a><a href="http://mejorando.la/videos" target="_blank"><button>Videos</button></a></div></div>');
			} else {
				notice_error();
			}
		}

		function notice_error(str) {
			$buyform.find('.notice').html('Ocurrió un error en el proceso. Porfavor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.')
		}

		function notice(str) {
			$buyform.find('.notice').html(str)

			return false;
		}

		function validates(card) {

			$buyform.find('input[type="text"]').each(function () {
				var $self = $(this);

				if(!card && $self.attr('name') == undefined) return;

				$self.removeClass('error');
				if($self.val().match(/^\s*$/)) {
					$self.addClass('error');
				}
			});

			if($buyform.find('.error').size() > 0) return false;
			else return true;
		}
	}();

	// ver video bottom
	$('#video-link').click(function () {
		$(this).html('<iframe width="660" height="370" src="http://www.youtube.com/embed/x4ZwpiKR7ew?autoplay=1&modestbranding=1&showinfo=0&autohide=1&controls=0" frameborder="0" allowfullscreen></iframe>')
		return false;
	});

	// Stripe
	Stripe.setPublishableKey('pk_test_4JlnsSvabjP6ynQdQM3WPZEy');

	var popup = new function () {
		var $self 	 = $('#pago'),
			$overlay = $self.find('.overlay')
			$panel   = $self.find('.panel');
		
		this.hide = function () {
			$overlay.addClass('fadeOut');
			$panel.addClass('bounceOutUp');

			setTimeout(function () {
				$self.removeClass('show');
				$overlay.removeClass('fadeOut').removeClass('fadeIn');
				$panel.removeClass('bounceOutUp').removeClass('bounceInDown');
			}, 1010);

			return false;
		};

		this.show = function () {
			$self.addClass('show');
			$overlay.addClass('fadeIn');
			$panel.addClass('bounceInDown');
		};

		// botones para cerrar
		$overlay.click(this.hide);
	}();

	$('.close').click(popup.hide);
	$('#registrate').click(popup.show);
});