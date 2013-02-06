define(['jquery', 'vendor/jquery.form'], function ($) {

    var nombre = $('input[type="text"]'),
        email = $('input[type="email"]');

    function fin(){
        nombre.animate({'opacity':1});
        email.animate({'opacity':1});
    }

    email.on('focus',function(){
        if(email.is(':focus')){
            email.animate({'max-width':360,'opacity': 0.5}, 500, fin);
            nombre.animate({'max-width':360,'opacity': 0.5}, 500, fin);
        }
    });

    $('#formulario').ajaxForm({
        clearForm: true,
        beforeSubmit: function ()
        {
            $("#formulario  #confirmacion").hide();
            $("#formulario #inscripcion").text("Inscribiendote...").fadeOut().fadeIn();
        },
        success: function (datos)
        {
            datos = JSON.parse(datos);

            if(datos.error)
            {
                $("#formulario  #inscripcion").text("Ya estabas registrado").fadeOut().fadeIn();
                $("#formulario  #email").focus();
            } else {
                $("#formulario #inscripcion").text("¡Ya estás inscrito!").fadeOut().fadeIn();
            }
        }
    }); 
});