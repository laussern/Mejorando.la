# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.http import Http404
from django.template import TemplateDoesNotExist, RequestContext
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

from models import Curso, CursoRegistro, CursoPago
from website.utils import get_pais
from utils import calculate

import stripe
import logging
import urllib

stripe.api_key = settings.STRIPE_SECRET_KEY


def home(req):
    import website.models

    # el archivo de cursos
    # organizados por mes-año
    return render_to_response('cursos/home.html', {
        'meses': [{
            'fecha': fecha,
            'cursos': website.models.Curso.objects.filter(fecha__year=fecha.year, fecha__month=fecha.month, activado=True).order_by('-fecha')
        } for fecha in website.models.Curso.objects.filter(activado=True).dates('fecha', 'month', order='DESC')]
    })


# vista publica del curso
def curso(req, curso_slug):
    if req.method == 'POST':
        curso = get_object_or_404(Curso, slug=curso_slug)
        vs = {'curso': curso}  # variables para el rendereo de la plantilla
        action = req.POST.get('action')

        if action and curso.activado:
            if action == 'buy':
                nombre = req.POST.get('nombre')
                email = req.POST.get('email')
                tel = req.POST.get('telefono')
                quantity = req.POST.get('quantity')
                token = req.POST.get('stripeToken')

                if nombre and email and tel and quantity and token:
                    # realizar el cargo con la api de stripe
                    p = CursoPago(nombre=nombre, email=email, telefono=tel, pais=get_pais(req.META), quantity=quantity, curso=curso, method='card')
                    p.save()

                    concept = calculate(int(quantity), curso.precio)

                    try:
                        charge = stripe.Charge.create(
                            amount=concept['amount'] * 100,
                            currency='usd',
                            card=token,
                            description=email
                        )
                    except Exception, e:
                        p.error = str(e)
                        p.save()

                        send_mail(u'¿Podemos ayudarte de alguna forma?', u'Vimos que tuviste problemas pagando el %s de Mejorando.la\n¿Podemos ayudarte de alguna forma?\nNo olvides que puedes contactarnos vía skype en mejorandola' % curso.nombre, 'Ventas Mejorando.la <ventas@mejorando.la>', [p.email], fail_silently=True)

                        return HttpResponse('ERR')

                    # si no se realiza el cargo regresar error
                    if not charge.paid:
                        return HttpResponse('ERR')

                    p.charged = True
                    p.save()

                    req.session['p32'] = p.id

                    return HttpResponse('OK')

                else:
                    return HttpResponse('ERR')

            elif action == 'deposit' or action == 'paypal':
                nombre = req.POST.get('nombre')
                email = req.POST.get('email')
                tel = req.POST.get('telefono')
                quantity = req.POST.get('quantity')

                if nombre and email and tel and quantity:
                    p = CursoPago(nombre=nombre, email=email, telefono=tel, pais=get_pais(req.META), quantity=quantity, curso=curso, method=action)
                    p.save()

                    return HttpResponse('OK')

                else:
                    return HttpResponse('ERR')

            elif action == 'register':
                email = req.POST.getlist('email')
                pago = req.session.get('p32')

                if email and pago:
                    p = get_object_or_404(CursoPago, id=pago)

                    # no permitir registro sin haber pagado
                    if not p.charged:
                        return HttpResponse('ERR')

                    for e in email:
                        r = CursoRegistro(email=e, pago=p)
                        r.save()

                    return HttpResponse('OK')

                else:
                    return HttpResponse('ERR')

            else:
                return HttpResponse('ERR')
        else:
            return HttpResponse('ERR')

    try:
        curso = Curso.objects.get(slug=curso_slug)
    except Curso.DoesNotExist:
        curso = None

    vs = RequestContext(req, {'curso': curso, 'publishable_key': settings.STRIPE_PUBLISHABLE_KEY})
    try:
        return render_to_response('%s.html' % curso_slug, vs)
    except TemplateDoesNotExist:
        if not curso:
            raise Http404

        return render_to_response('cursos/curso.html', vs)


@require_POST
def paypal_ipn(req):

    logging.error('PAYPAL IPN STARTED: payment_status %s, item_number %s, payer_email %s' % (req.POST.get('payment_status'), req.POST.get('item_number'), req.POST.get('payer_email')))

    # si estamos hablando de un pago
    if req.POST.get('payment_status') == 'Completed':

        # validar los datos que se reciben con paypal
        r = urllib.urlopen('https://www.paypal.com/cgi-bin/webscr', req.body + '&cmd=_notify-validate').read()

        logging.error('PAYPAL IPN VALIDATION: %s' % r)

        # respuesta de paypal
        if r == 'VERIFIED':
            curso = get_object_or_404(Curso, id=req.POST.get('item_number'))

            p = CursoPago.objects.filter(email=req.POST.get('payer_email'), curso=curso)

            if p.exists():
                p = p[0]

                p.charged = True
                p.save()
            else:
                p = CursoPago(nombre='%s %s' % (req.POST.get('first_name'), req.POST.get('last_name')), email=req.POST.get('payer_email'), telefono=req.POST.get('contact_phone'), pais=req.POST.get('address_country'), quantity=1, curso=curso, method='paypal', charged=True)
                p.save()

                logging.error('PAYPAL IPN: El pago no esta registrado en la bd')

            r = CursoRegistro(email=p.email, pago=p)
            r.save()

    return HttpResponse('OK')
