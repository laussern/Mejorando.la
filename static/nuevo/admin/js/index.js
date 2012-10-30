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

	$('a.back').live('click', close_overlay);

	var $overlay = $('.overlay'), $panel = $overlay.find('.panel');
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