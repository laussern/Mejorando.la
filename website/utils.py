# -*- coding: utf-8 -*-

import GeoIP


def get_ip(meta):
    # por si el usuario esta detras de un proxy
    if meta.get('HTTP_X_REAL_IP'):
        return meta.get('HTTP_X_REAL_IP')

    return meta['REMOTE_ADDR']


# devuelve el horario del programa
# localizado por pais gracias a la
# libreria GeoIP
def get_pais(meta):
    geo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

    country = geo.country_name_by_addr(get_ip(meta))
    if country is None:
        country = ''

    if country == 'Spain':
        country = u'España'

    return country


def get_pais_by_ip(ip):
    geo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

    country = geo.country_name_by_addr(ip)
    if country is None:
        country = ''

    if country == 'Spain':
        country = u'España'

    return country


def get_code(meta):
    geo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

    code = geo.country_code_by_addr(get_ip(meta))
    if code is None:
        code = ''

    return code
