jQuery(function ($) {
    // Stripe
    Stripe.setPublishableKey(config.publishable_key);

    // pestañas
    +function () {
        if($(window).width() < 1000) return;

        var $tabs = $('#tabs').addClass('js'),
            $tab  = $tabs.find('.tab').hide(),
            $sel  = $tabs.find('.selector');

        $(window).resize(function () {
            if($(window).width() < 1000) $tabs.removeClass('js');
            else $tabs.addClass('js');
        });

        // mostrar los primeros
        $sel.first().addClass('active');
        $tab.first().fadeIn();

        $sel.mouseenter(function () {
            var $self = $(this);

            // ocultar los viejos
            $sel.filter('.active').removeClass('active');
            $tab.stop(true, true).fadeOut();

            // mostrar los correctos
            $self.next('.tab').stop(true, true).fadeIn();
            $self.addClass('active');
        });
    }();

    // funcionalidad de pago
    +function () {
        // constantes
        var METHOD_CARD = 0, METHOD_DEPOSIT = 1, METHOD_PAYPAL = 2;

        // variables globales
        var quantity=1, method = 0;

        // ui (pantallas y barra de estado)
        var $screens = $('.screens'), $screen = $screens.find('.screen'), $status = $('#pago-status');

        // formularios y campos para estos
        var $forms    = $('#pago-forms'),
            $buyform  = $('#buy-form'),
            $regform  = $('#reg-form'),
            $depform  = $('#dep-form'),
            $payform  = $('#pay-form'),
            $quantity = $('input[name="quantity"]');

        // agregar o restar numero de asistentes
        $('.pago-count a').click(function () {
            var $self = $(this);

            var q = quantity;
            if($self.is('.pago-mas')) {
                q++;
            } else {
                if(quantity == 1) return;
                q--;
            }

            update_quantity(q);

            afterQuantity(); // actualizar barra de estado
        });

        function afterQuantity() {
            var r = calculate( get_price() ), c = get_currency();

            var extra = '';
            if(r.discount > 0) extra = ' <span>con un descuento de <strong>$'+r.discount+' '+c+'</strong></span>';

            set_status('$'+r.total+' '+c+extra);

            // agregar campos de registro al formulario
            if(method == METHOD_CARD) update_regform();
        }

        function update_quantity(num) {
            quantity  = num;

            // actualizar elementos html
            $quantity.val(num);
            $('.pago-num').html(num);
        }

        function update_method(num) {
            method = num;

            // actualizar barra de estado
            var n = get_method_name();
            set_status('$'+get_price()+' '+get_currency()).addClass(n);
            afterQuantity();
            $forms.removeClass('paypal deposit card');
            $forms.addClass(n);
        }

        function get_currency() {
            if(method == METHOD_DEPOSIT)      return config.currencyd;
            else if(method == METHOD_PAYPAL) return config.currencyp;

            return 'USD';
        }

        function get_price() {
            if(method == METHOD_DEPOSIT)
                return parseInt(config.preciod, 10);
            else if(method == METHOD_PAYPAL)
                return parseInt(config.preciop, 10);

            return parseInt(config.precio, 10);
        }

        function get_method_name() {
            if(method == METHOD_DEPOSIT)      return 'deposit';
            else if(method == METHOD_PAYPAL) return 'paypal';

            return 'card';
        }

        function set_status(str) { return $status.html(str); }


        $depform.submit(function () {
            if(!validates($depform))
                return err($depform, 'Debe completar todos los campos.');

            send_form($depform);
            $.post($depform.attr('action'), $depform.serialize(), deposito);

            return false;
        });

        $payform.submit(function () {
            if(!validates($payform))
                return err($payform, 'Debe completar todos los campos.');

            send_form($payform);
            $.post($payform.attr('action'), $payform.serialize(), paypal);

            return false;
        });

        var error_translations = {
            'incorrect_number': 'El número de tarjeta es incorrecto',
            'invalid_number': 'El número de tarjeta no es un número real o está mal escrito',
            'invalid_expiry_month': 'La fecha de expiración de la tarjeta es invalida',
            'invalid_expiry_year': 'El año de expiración de la tarjeta es invalido',
            'invalid_cvc': 'El código de seguridad de la tarjeta no es el correcto',
            'expired_card': 'Tu tarjeta expiró',
            'incorrect_cvc': 'El código de seguridad de la tarjeta no es el correcto',
            'card_declined': 'Tu tarjeta fue rechazada (intenta con otra)',
            'processing_error': 'Un error ocurrió mientras procesabamos tu tarjeta, intenta de nuevo'
        };
        $buyform.submit(function () {

            if(!validates($buyform, true))
                return err($buyform, 'Debe completar todos los campos.');

            send_form($buyform);
            Stripe.createToken({
                number   : $buyform.find('.card-number').val(),
                cvc      : $buyform.find('.card-cvc').val(),
                exp_month: $buyform.find('.card-expiry-month').val(),
                exp_year : $buyform.find('.card-expiry-year').val()
            }, function (status, response) {

                unsend_form($buyform);

                if(response.error) {
                    var msg = response.error.message;

                    if(error_translations[response.error.code]) msg = error_translations[response.error.code];
                    err($buyform, msg);
                } else {
                    $buyform.find('input[name="stripeToken"]').val(response.id);

                    send_form($buyform);
                    $.post($buyform.attr('action'), $buyform.serialize(), registro);
                }
            });

            return false;
        });

        $regform.submit(function () {
            if(!validates($regform))
                return err($regform, 'Debe completar todos los campos.');

            send_form($regform);

            $.post($regform.attr('action'), $regform.serialize(), ultimo);

            return false;
        });

        // ir al siguiente paso
        $('.pago-btns .next').live('click', pago_next);
        // volver a la pantalla anterior
        $('.pago-btns .cancel').click(pago_back);

        // cambiar de metodo de pago a tarjeta de credito
        $('.method-c').click(function () {
            update_method(METHOD_CARD);

            pago_next();
        });

        // cambiar de metodo de pago a deposito
        $('.method-d').click(function () {
            if(typeof config.preciod != 'undefined' && typeof config.currencyd != 'undefined') {
                update_method(METHOD_DEPOSIT);

                pago_next();
            }
        });

        // cambiar de metodo de pago a paypal
        $('.method-p').click(function () {
            if(typeof config.preciop != 'undefined' && typeof config.currencyp != 'undefined') {
                update_method(METHOD_PAYPAL);

                pago_next();
            }
        });

        // volver a la pantalla principal
        $('.pago-btns .clearstatus').click(function () {
            update_quantity(1);

            $status.text('$0 USD').removeClass('deposit paypal card');
            $forms.removeClass('deposit paypal card');
            update_method(METHOD_CARD); // metodo default
        });

        update_method(METHOD_CARD); // metodo default

        $('#paybypal').click(function () {
            update_method(METHOD_PAYPAL); // metodo default
            return false;
        });

        function pago_next() {
            var $cur = $('.screen.active');

            $cur.removeClass('active');
            $cur.next('.screen').addClass('active');
        }

        function pago_back() {
            var $cur = $('.screen.active');

            $cur.prev('.screen').addClass('active');
            $cur.removeClass('active');
        }

        function deposito(r) {
            unsend_form($depform);

            if(r == 'OK') {
                $status.addClass('success').html(':) Gracias');
                $screens.html('<div class="final"><p>En breve recibirás la información para realizar tu pago al siguiente curso:</p><h1>'+config.nombre+'</h1><p>Para cualquier duda puedes comunicarte a:</p></div>');
            } else {
                err($depform, 'Ocurrió un error en el proceso. Por favor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.');
            }

        }

        function paypal(r) {
            unsend_form($payform);

            if(r == 'OK') {
                var p = get_price();
                r = calculate( p );

                var f = '<form id="paypal" action="https://www.paypal.com/cgi-bin/webscr" method="post">'+
                    '<input type="hidden" name="charset" value="utf-8" />'+
                    '<input type="hidden" name="cmd" value="_xclick" />'+
                    '<input type="hidden" name="rm" value="1" /> <!-- send data back via POST -->'+
                    '<input type="hidden" name="cancel_return" value="'+window.location.href+'" />'+
                    '<input type="hidden" name="notify_url" value="https://mejorando.la/cursos/paypal_ipn" />'+
                    '<input type="hidden" name="return" value="'+window.location.href+'?felicidades" />'+
                    '<input type="hidden" name="business" value="cursos@mejorando.la" />'+
                    '<input type="hidden" name="lc" value="ES" />'+
                    '<input type="hidden" name="no_shipping" value="1" />'+
                    '<input type="hidden" name="no_note" value="1" />'+
                    '<input type="hidden" name="cpp_logo_image" value="https://mejorando.la/images/logo_for_paypal.png" />'+

                    '<input type="hidden" name="currency_code" value="'+get_currency()+'" /> <!-- USD EUR MXN -->'+
                    '<input type="hidden" name="quantity" value="'+quantity+'" />'+
                    '<input type="hidden" name="discount_amount" value="'+r.discount+'" />'+
                    '<input type="hidden" name="amount" value="'+p+'" />'+
                
                    '<input type="hidden" name="item_name" value="'+config.nombre+'" />'+
                    '<input type="hidden" name="item_number" value="'+config.id+'" />'+
                '</form>';

                $(f).submit();
            } else {
                if(r == 'ERR TOO MANY TRIES') {
                    err($payform, 'Agradecemos tu interés y perseverancia para inscribirte al curso pero tenemos problemas con tu banco y nuestro sistema.  Escríbenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a> para que busquemos alternativas. No queremos dejarte fuera del próximo curso.');
                } else {
                    err($payform, 'Ocurrió un error en el proceso. Por favor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.');
                }
            }
        }

        function registro(r) {
            unsend_form($buyform);

            if(r == 'OK') {
                // si se elige la opcion de crear con el mismo registro
                if($('#samedata').is(':checked')) $regform.find('input.email').first().val($buyform.find('input.email').val());
                // ir al siguiente paso
                pago_next();
            } else {
                if(r == 'ERR TOO MANY TRIES') {
                    err($buyform, 'Agradecemos tu interés y perseverancia para inscribirte al curso pero tenemos problemas con tu banco y nuestro sistema.  Escríbenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a> para que busquemos alternativas. No queremos dejarte fuera del próximo curso.');
                } else {
                    err($buyform, 'Ocurrió un error en el proceso. Por favor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.');
                }
            }
        }

        function ultimo (r) {
            unsend_form($regform);

            if(r == 'OK') {
                $status.addClass('success').html(':) Felicidades');
                $screens.html('<div class="final"><p>Ya estás listo para asistir a este curso:</p><h1>'+config.nombre+'</h1><p>Para cualquier duda puedes comunicarte a:</p></div>');
            } else {
                err($regform, 'Ocurrió un error en el proceso. Por favor intentalo más tarde o escribenos a <a href="mailto:ventas@mejorando.la">ventas@mejorando.la</a>.');
            }

        }

        function send_form($form) {
            $form.addClass('sending');
            notice($form, 'Enviando...');
        }

        function unsend_form($form) {
            $form.removeClass('sending');
            notice($form, '');
        }
        
        function notice($form, str) {
            $form.find('.notice').html(str);

            return false;
        }

        function err($form, str) {
            $form.find('.notice').html('<span class="err">*</span> '+str);

            return false;
        }

        function validates($form, card) {

            $form.find('input[type="text"]').each(function () {
                var $self = $(this);

                if(!card && $self.attr('name') === undefined)
                    return;

                $self.removeClass('error');
                if($self.val().match(/^\s*$/)) {
                    $self.addClass('error');
                }
            });

            if($form.find('.error').size() > 0) return false;
            else return true;
        }

        function calculate(price) {
            // get base numbers
            var rate = Math.floor(quantity / 5),
                total = price * quantity;

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

            return {
                'total': total,
                'discount': discount
            };
        }

        function update_regform() {
            var $als = $regform.find('.alumnos');

            var html = '';
            for(var i = 1; i <= quantity; i++)
                html += '<label class="alumno">Alumno '+i+': <input type="text" placeholder="Email" class="email"   name="email" /></label>';

            $als.html(html);
        }

    }();

    // ver video bottom
    $('#video-link').click(function () {
        var $self = $(this);
        $self.html('<iframe width="666" height="376" src="'+$self.attr('href')+'?autoplay=1&modestbranding=1&showinfo=0&autohide=1&controls=0" frameborder="0" allowfullscreen></iframe>');
        return false;
    });

    var popup = new function () {
        var $self      = $('#pago'),
            $overlay = $self.find('.overlay'),
            $panel   = $self.find('.panel');
        
        this.hide = function () {
            $overlay.addClass('fadeOut');
            $panel.addClass('bounceOutUp');

            setTimeout(function () {
                $self.removeClass('show');
                $overlay.removeClass('fadeOut').removeClass('fadeIn');
                $panel.removeClass('bounceOutUp').removeClass('bounceInDown');
            }, 1010);

            return false;
        };

        this.show = function () {
            $self.addClass('show');
            $overlay.addClass('fadeIn');
            $panel.addClass('bounceInDown');
        };

        // botones para cerrar
        $overlay.click(this.hide);
    }();

    $('.close').click(popup.hide);
    $('#registrate').click(popup.show);

    if (document.location.href.indexOf('?felicidades') !== -1) {
        $('#pago-status').addClass('success').html(':) Felicidades');
        $('.screens').html('<div class="final"><p>Ya estás listo para asistir a este curso:</p><h1>'+config.nombre+'</h1><p>Para cualquier duda puedes comunicarte a:</p></div>');

        $('#registrate').trigger('click');

    }

});