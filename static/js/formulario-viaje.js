$(function(){
	var opciones = {
	beforeSubmit: enviando,
	success: recepcion
	};

	$('#f-viaje').ajaxForm(opciones); 
})
function enviando()
{
	$("#f-viaje #inscri").text("Inscribiendote...").fadeOut().fadeIn();
}

function recepcion(datos)
{
	datos = $.trim(datos);
	if(datos=="OK")
	{
		$("#f-viaje #inscri").text("¡Ya estás inscrito!").fadeOut().fadeIn();
		$('#f-viaje')[0].reset()
	}
	else
	{
		$("#f-viaje  #confirmacion").text("Verifica que todos los datos estén bien escritos").slideDown();
	}
	
	
	
}