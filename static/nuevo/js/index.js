jQuery(function ($) {
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

		$sel.click(function () {
			var $self = $(this);

			if($self.hasClass('active')) return;
			else {
				var $hidden = $tab.filter(':hidden');

				// ocultar los viejos
				$sel.filter('.active').removeClass('active');
				$tab.filter(':visible').fadeOut();

				// mostrar los correctos
				$hidden.fadeIn();
				$self.addClass('active');
			}

		});
	}();

	// funcionalidad de pago
	+function () {
		var $pago 	 = $('#pago'),
			$btn 	 = $('#pago-btn'), 
			$content = $('#pago-content'), 
			time     = 200,
			step     = 0,
			price    = config.precio,
			quantity = 1,
			discount = 0,
			total    = price,
			tmpl_btn = ['$0 '+config.moneda+'', 
						'<strong>$<span class="rtotal">'+total+'</span> '+config.moneda+'</strong>descuento <em>$<span class="rdiscount">'+discount+'</span> '+config.moneda+'</em>', 
						'<strong>$<span class="rtotal">%total</span> '+config.moneda+'</strong><em><span class="rquantity">%quantity</span></em> reserva(s)', 
						':) Felicidades'],
			tmpl_cont = ['<h1><strong>Paso 1 / <span>3</span></strong>Modo de Pago</h1><div class="pago-methods"><a class="pago-method tarjeta active">Tarjeta de Credito</a><a class="pago-method deposito">Deposito Bancario</a></div><div class="pago-btns"><button class="cancel">cancelar</button><button class="next">siguiente</button></div>', 
						 '<h1><strong>Paso 2 / <span>3</span></strong>Numero de Reservas</h1><div class="pago-count"><span class="pago-num">'+quantity+'</span><a class="pago-menos">-</a><a class="pago-mas">+</a></div><div class="pago-btns"><button class="cancel">cancelar</button><button class="next">siguiente</button></div>', 
						 '<h1><strong>Paso 3 / <span>3</span></strong>Datos Personales</h1><form class="buy-form" method="post"><input name="nombre" type="text" placeholder="Nombre" class="nombre" /><input name="email" type="text" placeholder="Email" class="email" /><input name="telefono" type="text" placeholder="Teléfono" class="tel" /></form><div class="pago-btns"><button class="cancel">cancelar</button><button class="next">Comprar</button></div>', 
						 '<p>Ya estás listo para asistir a este curso:</p><h1>'+config.nombre+'</h1><div class="pago-links"><p>Te invitamos a saber más de nuestros</p><a href="http://mejorando.la/cursos" target="_blank"><button>Cursos</button></a><a href="http://mejorando.la/videos" target="_blank"><button>Videos</button></a></div>'], default_btn = default_cont = '';


		function format(str) {
			str = str.replace('%total', total);
			str = str.replace('%price', price);
			str = str.replace('%discount', discount);
			str = str.replace('%quantity', quantity);

			return str;
		}

		// calcular el price total y aplicar descuentos 
		function calculate() {
			total = price*quantity, rate = Math.floor(quantity/5), discount = 0;

			// descuento de plazas gratis
			discount += rate * price;

			// aplicar el descuento solo cuando no sea cada 5 (que es cuando hay una plaza gratis mas)
			if(quantity % 5 != 0)
				discount += (price*0.1)*(quantity < 5 ? quantity-1 : quantity-(5*rate) );

			total = total-discount;

			$('.rtotal').text(total);
			$('.rdiscount').text(discount);
		}


		function validates() {
			var $form = $('.buy-form');

			$form.find('input[type="text"]').each(function () {
				var $self = $(this);

				$self.removeClass('error');
				if($self.val().match(/^\s*$/)) {
					$self.addClass('error');
				}
			});

			if($form.find('.error').size() > 0) return false;
			else return true;
		}

		// avanzar una pagina
		function next_step() {
			if(step >= 4) return;

			if(step == 3) {
				if(!validates()) return;

				var $form = $('.buy-form');

				$.post($form.attr('action'), $form.serialize(), 
					function (r) {
						step++;

						// same here
						$btn.fadeOut(time, function () {
							$btn.html(format(tmpl_btn[step-1]));
							$pago.removeClass('step'+(step-1));
							$pago.addClass('step'+step);

							$btn.fadeIn();
						});

						$content.fadeOut(time, function () {
							$content.html(format(tmpl_cont[step-1]));
							$content.fadeIn();
						});
				});

				return;
			}

			// same here
			step++;

			$btn.fadeOut(time, function () {
				$btn.html(format(tmpl_btn[step-1]));
				$pago.removeClass('step'+(step-1));
				$pago.addClass('step'+step);

				$btn.fadeIn();
			});

			$content.fadeOut(time, function () {
				$content.html(format(tmpl_cont[step-1]));
				$content.fadeIn();
			});
		}

		// boton grande de pagar y registrarse
		$btn.click(function () {
			if($btn.hasClass('disabled')) return;

			default_cont = $content.html();
			default_btn  = $btn.html();

			next_step();

			$btn.addClass('disabled');
		});

		// ir al siguiente paso
		$('.pago-btns .next').live('click', function () { next_step(); });
		// reiniciar los pasos
		$('.pago-btns .cancel').live('click', function () { 
			step = 0;

			$btn.removeClass('disabled');
			$pago.removeClass('step1').removeClass('step2').removeClass('step3');

			$content.html(default_cont);
			$btn.html(default_btn);
		});

		// cambiar de metodo de pago
		$('.pago-method').live('click', function () {
			var $self = $(this);

			if($self.hasClass('active')) return;
			else {
				var $si = $('.pago-method.active');

				$self.addClass('active');
				$si.removeClass('active');
			}
		});

		// agregar o restar numero de asistentes
		$('.pago-count a').live('click', function () {
			var $self = $(this);

			if($self.is('.pago-mas')) {
				quantity++;
			} else {

				if(quantity == 1) return;
				quantity--;
			}

			calculate();
			$('.pago-num').html(quantity);
		});
	}();

	$('#video-link').click(function () {
		$(this).html('<iframe width="660" height="370" src="http://www.youtube.com/embed/x4ZwpiKR7ew?autoplay=1&modestbranding=1&showinfo=0&autohide=1&controls=0" frameborder="0" allowfullscreen></iframe>')
		return false;
	});

});