jQuery(function ($) {
	function enviando()
	{
		$("#formulario #inscripcion").text("Inscribiendote...").fadeOut().fadeIn();
	}

	function recepcion(datos)
	{
		datos = JSON.parse(datos);

		if(datos.error)
		{
			//$("#formulario #inscripcion").text("Seguro ya estabas inscrito").fadeOut().fadeIn();
			$("#formulario  #confirmacion").text("Verifica que todos los datos estén bien escritos").slideDown();
			$("#formulario  #email").focus();
		} else {
			$("#formulario #inscripcion").text("¡Ya estás inscrito!").fadeOut().fadeIn();
		}
	}

	var opciones = {
		beforeSubmit: enviando,
		success: recepcion,
		clearForm: true
	};
	
	$('#formulario').ajaxForm(opciones); 
});