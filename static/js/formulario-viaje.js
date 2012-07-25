jQuery(function ($) {
	function enviando()
	{
		$("#f-viaje #inscri").text("Inscribiendote...").fadeOut().fadeIn();
	}

	function recepcion(datos)
	{
		datos = JSON.parse(datos);

		if(datos.error)
		{
			$("#f-viaje  #confirmacion").text("Verifica que todos los datos estén bien escritos").slideDown();
		} else {
			$("#f-viaje #inscri").text("¡Ya estás inscrito!").fadeOut().fadeIn();
			$('#f-viaje')[0].reset()
		}
	}

	var opciones = {
		beforeSubmit: enviando,
		success: recepcion
	};
	
	$('#f-viaje').ajaxForm(opciones); 
});