jQuery(function ($) {
	// Stripe
	Stripe.setPublishableKey(config.publishable_key);

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
		var quantity=1, price = parseInt(config.precio);

		var $buyform  = $('#buy-form'), 
			$regform  = $('#reg-form'),
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


			calculate();
			update_regform();
		});

		// ir al siguiente paso
		$('.pago-btns .next').live('click', pago_next);

		$buyform.submit(function () {

			if(!validates($buyform, true)) return err($buyform, 'Debe completar todos los campos.')			

			send_form($buyform);
			Stripe.createToken({
				number   : $buyform.find('.card-number').val(),
				cvc      : $buyform.find('.card-cvc').val(),
				exp_month: $buyform.find('.card-expiry-month').val(),
				exp_year : $buyform.find('.card-expiry-year').val()
			}, function (status, response) {	
				unsend_form($buyform);

				if(response.error) {
					err($buyform, response.error.message);
				} else {
					$buyform.find('input[name="stripeToken"]').val(response.id);

					send_form($buyform);
					$.post($buyform.attr('action'), $buyform.serialize(), registro);
				}
			});

			return false;
		})

		$regform.submit(function () {
			if(!validates($regform)) return err($regform, 'Debe completar todos los campos.')

			send_form($regform);

			$.post($regform.attr('action'), $regform.serialize(), ultimo);

			return false;
		});

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
			unsend_form($buyform);

			if(r == 'OK') {
				// si se elige la opcion de crear con el mismo registro
				if($('#samedata').is(':checked')) $regform.find('input.email').first().val($buyform.find('input.email').val());
				// ir al siguiente paso
				pago_next();
			} else {
				err($buyform, 'Ocurrió un error en el proceso. Porfavor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.');
			}
		}

		function ultimo (r) {
			unsend_form($regform);

			if(r == 'OK') {
				$status.addClass('success').html(':) Felicidades');
				$screens.html('<div class="final"><p>Ya estás listo para asistir a este curso:</p><h1>'+config.nombre+'</h1><div class="pago-links"><p>Te invitamos a saber más de nuestros</p><a href="http://mejorando.la/cursos" target="_blank"><button>Cursos</button></a><a href="http://mejorando.la/videos" target="_blank"><button>Videos</button></a></div></div>');
			} else {
				err($regform, 'Ocurrió un error en el proceso. Porfavor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.');
			}

		}

		function send_form($form) {
			$form.addClass('sending');
			notice($form, 'Enviando...');
		}

		function unsend_form($form) {
			$form.removeClass('sending');
			notice($form, '');
		}
		
		function notice($form, str) {
			$form.find('.notice').html(str)

			return false;
		}

		function err($form, str) {
			$form.find('.notice').html('<span class="err">*</span> '+str)

			return false;
		}

		function validates($form, card) {

			$form.find('input[type="text"]').each(function () {
				var $self = $(this);

				if(!card && $self.attr('name') == undefined) return;

				$self.removeClass('error');
				if($self.val().match(/^\s*$/)) {
					$self.addClass('error');
				}
			});

			if($form.find('.error').size() > 0) return false;
			else return true;
		}

		function calculate() {
			// get base numbers
			var rate = Math.floor(quantity / 5),
				total = price * quantity;

			// descuento de plazas gratis
			var discount = rate * price;

			// aplicar el descuento solo cuando no sea cada 5 (que es cuando hay una plaza gratis mas)
			if ((quantity % 5) !== 0)
				discount += (price * 0.1) * (quantity < 5 ? quantity-1 : quantity - (5 * rate) );

			// final total price
			total -= discount;

			// redondeando numeros
			discount = Math.ceil(discount);
			total = Math.ceil(total);

			var extra = '';

			if(discount > 0) extra = ' <span>con un descuento de <strong>$'+discount+' USD</strong></span>';

			$status.html('$'+total+' USD'+extra)
		}

		function update_regform() {
			var $als = $regform.find('.alumnos');

			var html = '';
			for(var i = 1; i <= quantity; i++) 
				html += '<label class="alumno">Alumno '+i+': <input type="text" placeholder="Email" class="email"   name="email" /></label>';

			$als.html(html);
		}
	}();

	// ver video bottom
	$('#video-link').click(function () {
		$(this).html('<iframe width="660" height="370" src="http://www.youtube.com/embed/x4ZwpiKR7ew?autoplay=1&modestbranding=1&showinfo=0&autohide=1&controls=0" frameborder="0" allowfullscreen></iframe>')
		return false;
	});

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