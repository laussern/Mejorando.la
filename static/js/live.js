jQuery(function ($) {
	function enviando()
	{
		$("#formulario .tit").text("Inscribiendote...").fadeOut().fadeIn();
	}

	

	function recepcion(datos)
	{
		datos = JSON.parse(datos);

		if(datos.error)
		{
			//$("#formulario #inscripcion").text("Seguro ya estabas inscrito").fadeOut().fadeIn();
			$("#formulario  .tit").text("Ya estabas registrado").fadeOut().fadeIn();
			$("#formulario  #email").focus();
		} else {
			$("#formulario .tit").text("¡Ya estás inscrito!").fadeOut().fadeIn();

		}
	}

	var opciones = {
		beforeSubmit: enviando,
		success: recepcion,
		clearForm: true
	};
	
	$('#formulario').ajaxForm(opciones); 

	$(window).on('load', function(){
		$('#col2').html('<div class="chat"><iframe src="https://chat.mejorando.la:3000" width="100%" height="75%" frameborder="0"></iframe></div>');
	});


	function getViewportSize()
	{
		var e = window, a = 'inner';
		if ( !( 'innerWidth' in window ) )
		{
			a = 'client';
			e = document.documentElement || document.body;
		}
		return { width : e[ a + 'Width' ] , height : e[ a + 'Height' ] }
	}

	function resize()
	{
		var viewport = getViewportSize();
		var $iframe = $('#col2 iframe');

		// resize chat
		if (viewport.width <= 768)
		{
			var height = viewport.height - $('#video').height();
			$iframe.css('height', height);
			$iframe.data('resized', true);
		}
		else {
			if ($iframe.data('resized'))
				$iframe.css('height', '');
		}
	}

	resize();
	$(window).on('load debouncedresize', resize);
});