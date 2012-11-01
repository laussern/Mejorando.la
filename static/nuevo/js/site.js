// Avoid `console` errors in browsers that lack a console.
(function() {
	var noop = function noop() {};
	var methods = [
		'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
		'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
		'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
		'timeStamp', 'trace', 'warn','speakers'
	];
	var length = methods.length;
	var console = window.console || {};

	while (length--) {
		// Only stub undefined methods.
		console[methods[length]] = console[methods[length]] || noop;
	}
}());

// Place any jQuery/helper plugins in here.

var Site = {
	register: function() {
		// set initial paypal values
		$('#paypal input[name="item_name"]').val(payment_config.name);
		$('#paypal input[name="curso"]').val(payment_config.name);
		$('#paypal input[name="item_number"]').val(payment_config.code);
		$('#paypal input[name="code"]').val(payment_config.code);
		$('#paypal input[name="return"]').val(payment_config.redirect_url);
		$('#paypal input[name="cancel_return"]').val(payment_config.cancel_url);

		var $register = $('#register');

		$('#payment-data').validator();
		
		$('#register-link').on('click', function(e){
			e.preventDefault();

			$(window)[0].scrollTo(0, 0);
			$('body').addClass('overlay');

			$('.change-method').trigger('click');

			// Remove "success" message when opening a finished form
			$('#register').removeClass('done').find('.cart strong').html( Site.format_price(0, 'bank') );

			Site.placeholders();
			Site.validation();

			Site.step_1();
			Site.step_2();
		});

		$register.on('click', 'a.back', function(e){
			e.preventDefault();
			
			var $step = $register.find('.step-active');
			$step.removeClass('step-active').hide();

			var selector = $(this).attr('href');
			$(selector).addClass('step-active').fadeIn();
		});

		$register.on('click', 'a.next', function(e){
			e.preventDefault();
			
			var $step = $register.find('.step-active');
			$step.removeClass('step-active').hide();

			var selector = $(this).attr('href');
			$(selector).addClass('step-active').fadeIn();
		});

		$('#close').on('click', function(e){
			e.preventDefault();
			$('body').removeClass('overlay').trigger('click');

			var validator = $('#payment-data').data('validator');
			if (validator) {
				validator.reset();
			}
		});
	},

	placeholders: function(){
		if (Modernizr.input.placeholder)
			return;

		Modernizr.load({
			load: ['js/jquery.placeholder-1.0.1.js'],
			complete: function(){
				$('input[placeholder], textarea[placeholder]').placeholder({
					blankSubmit: true
				});
			}
		});
	},

	validation: function(){
		$('#payment-data')
			.validator()
			.on('submit', function(e){
				e.preventDefault();

				var $form = $(this);
				var callback = function(){
					// validate the form with jquery tools plugin
					if (!$form.data('validator').checkValidity())
						return;
					
					Site.step_3();
				};
				
				// run callback
				if (Modernizr.input.placeholder) {
					callback();
				} else {
					// workaround: let jquery.placeholder() do its work first
					setTimeout(callback, 100);
				}
			});
	},

	format_price: function(price, payment_method) {
		var x = payment_config[payment_method];
		
		// eg. $150 USD
		return x.sign + price + '&nbsp;' + x.currency;
	},

	update_cart: function() {
		// get current payment method, price and currency
		var payment_method = $('#step-1 input:checked').val();
		var price    = payment_config.online.price;
		var currency = payment_config.online.currency;

		if (payment_method == 'bank') {
			price    = payment_config.bank.price;
			currency = payment_config.bank.currency;
		}

		// get dom elements
		var $cart     = $('#register .cart');
		var $step     = $('#step-2');
		var $quantity = $step.find('.quantity');



		// get base numbers
		var quantity  = parseInt($quantity.text(), 10);
		var rate = Math.floor(quantity / 5);
		var total = price * quantity;

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



		// update fields
		$('#paypal input[name="currency"]').val(currency);
		$('#paypal input[name="currency_code"]').val(currency);

		$('#paypal input[name="discount_amount"]').val(discount);
		$('#paypal input[name="descuento"]').val(discount);
		
		$('#paypal input[name="total"]').val(total);

		$cart.find('strong').html( Site.format_price(total, payment_method) );

		if (discount) {
			$cart.addClass('has-discount');
			$cart.find('.discount em').html(Site.format_price(discount, payment_method));
		} else {
			$cart.removeClass('has-discount');
		}
	},

	step_1: function() {
		if ($('body').data('step-1'))
			return;

		$('body').data('step-1', true);

		var $step     = $('#step-1');
		var $register = $('#register');

		$register.find('.cart strong').html(Site.format_price(0, 'bank'));
		$('#option-card .price').html(Site.format_price(payment_config.online.price, 'online'));
		$('#option-bank .price').html(Site.format_price(payment_config.bank.price, 'bank'));

		$step.on('click', 'input', function(e){
			var $input = $(this);
			var value = $input.val();
			var $li = $input.parent('li');

			$register.removeClass().addClass(value);

			$li.addClass('active');
			$li.siblings('.active').removeClass('active');
			
			$step.removeClass('step-active').hide();
			$step.next().addClass('step-active').fadeIn();

			Site.update_cart();
		});

		// if the url has ?felicidades, we go to the last step right away
		if (document.location.href.indexOf('?felicidades') !== -1) {
			$('#input-online').attr('checked', 'checked');
			$('#input-online').trigger('click');
			Site.step_4();
		}
	},

	step_2: function() {
		if ($('body').data('step-2'))
			return;

		$('body').data('step-2', true);

		var $step     = $('#step-2');
		var $quantity = $step.find('.quantity');
		var quantity  = 1;

		// paypal form data
		var $form_quantity = $('#paypal input[name="quantity"], #paypal input[name="personas"]');

		$step.on('click', '.dec', function(e){
			e.preventDefault();
			
			if (quantity <= 1)
				return;

			quantity -= 1;
			$quantity.text(quantity);
			$form_quantity.val(quantity);

			Site.update_cart();

			var class_name = (quantity <= 5) ? quantity : 5;
			$quantity.removeClass();
			$quantity.addClass('quantity quantity-' + class_name);
		});

		$step.on('click', '.inc', function(e){
			e.preventDefault();
			quantity += 1;
			$quantity.text(quantity);
			$form_quantity.val(quantity);

			Site.update_cart();

			var class_name = (quantity <= 5) ? quantity : 5;
			$quantity.removeClass();
			$quantity.addClass('quantity quantity-' + class_name);
		});
	},

	step_3: function() {
		var payment_method = $('#step-1 input[type="radio"]:checked').val();
		var $form = $('#paypal');

		$('#paypal input[name="tipo"]').val( payment_method == 'online' ? 'paypal' : 'deposito' );
		$('#paypal input[name="nombre"]').val( $('#payment-data input[name="nombre"]').val() );
		$('#paypal input[name="email"]').val( $('#payment-data input[name="email"]').val() );
		$('#paypal input[name="telefono"]').val( $('#payment-data input[name="telefono"]').val() );
		
		$.ajax({
			type: 'POST',
			url: 'http://mejorando.la/cursos/registro',
			data: $form.serialize(),
			complete: function(){
				if (payment_method == 'online') {
					$form.trigger('submit');
				} else if (payment_method == 'bank') {
					Site.step_4();
				}
			}
		});
	},

	step_4: function() {
		var $register = $('#register');
		var $step = $register.find('.step-active');

		$register.addClass('done');
		$step.removeClass('step-active').hide();
		$register.find('.cart strong').text(':) Felicidades');

		$('#step-4').addClass('step-active').fadeIn();
	},

	tabs: function() {
		var $syllabus = $('#syllabus');
		var $bg = $syllabus.find('span.bg');
		var top = null;
		$('#syllabus-location').css('height',$('#syllabus .content').outerHeight())
		$syllabus.on('mouseenter', '.tab', function(e){
			e.preventDefault();
			var $tab = $(this);
			var $day = $tab.parent();
			
			if ($day.hasClass('active'))
				return;

			$day.siblings('.active').removeClass();
			$day.addClass('active');

			var offset = $day.data('offset');
			if (!offset) {
				top = ($tab.outerHeight() / 2) - ($bg.outerHeight() / 2);
				offset = (top + $tab.position().top) + 'px';
				$day.data('offset', offset);
			}

			$bg.css('top', offset);
		});
	},

	speakers: function(){
		if($(window).width() > 1000){
			var $speakers = $('#speakers section');
			var numero_profesores = $speakers.length;
			if (numero_profesores < 4 ){
				$speakers.css('width', $('#speakers .wrap').width() / numero_profesores -10 ) 	
			}else{
				$speakers.addClass('fix')
			}
		}
		
		
	},

	video: function() {
		var $link = $('#video a, .video_header a');
		var href = $link.attr('href');
		var youtube = href.split('youtu.be/')[1];
		var html = '<iframe class="video_promo" width="661" height="372" src="http://www.youtube.com/embed/' + youtube + '?autoplay=1&autohide=1" frameborder="0" allowfullscreen></iframe><img class="video_fix" src="../static/nuevo/images/video.png">';

		$link.on('click', function(e){
			e.preventDefault();
			$(this).after(html);
			$(this).fadeOut('fast', function(){
				$(this).remove();
			});
		});
	},

	init: function(){
		Site.register();
		Site.tabs();
		Site.video();
		Site.speakers();

		$('#register-link strong').html( Site.format_price(payment_config.online.price, 'online') );

		if (document.location.href.indexOf('?felicidades') !== -1) {
			$('#register-link').trigger('click');
		}
	}
};

Site.init();