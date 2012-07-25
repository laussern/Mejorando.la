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
			//$("#formulario #inscripcion").text("Seguro ya estabas inscrito").fadeOut().fadeIn();
			$("#f-viaje  #confirmacion").text("Verifica que todos los datos estén bien escritos").slideDown();
		} else {
			$("#f-viaje #inscri").text("¡Ya estás inscrito!").fadeOut().fadeIn();
		}
	}

	var opciones = {
		beforeSubmit: enviando,
		success: recepcion,
		clearForm: true
	};
	
	$('#f-viaje').ajaxForm(opciones); 
});