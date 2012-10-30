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
		$('body').addClass('overlayed');

		$('.panel').load($(this).attr('href')+' #add_form')

		return false;
	})

	$('.edit').click(function () {
		$('body').addClass('overlayed');

		$('.panel').load($(this).attr('href')+' #edit_form')

		return false;
	})

	$('#add_form').live('submit', function () {
		$('body').removeClass('overlayed')

		return false;
	});

	$('a.back').live('click', function () {
		$('body').removeClass('overlayed')		
	});
});