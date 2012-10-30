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

	/*$('.curso a').click(function(){
		var selector = $(this).attr('data-filter');
		$container.isotope({ filter: selector });
		return false;
	});*/
});