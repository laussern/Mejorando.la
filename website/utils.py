import GeoIP

# devuelve el horario del programa
# localizado por pais gracias a la
# libreria GeoIP
def get_pais(meta):
    geo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

    # por si el usuario esta detras de un proxy
    if 'HTTP_X_FORWARDED_FOR' in meta and meta['HTTP_X_FORWARDED_FOR']:
        ip = meta['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = meta['REMOTE_ADDR']

    country = geo.country_name_by_addr(ip)
    if country is None:
        country = ''

    return country


def get_code(meta):
    geo = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)

    # por si el usuario esta detras de un proxy
    if 'HTTP_X_FORWARDED_FOR' in meta and meta['HTTP_X_FORWARDED_FOR']:
        ip = meta['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = meta['REMOTE_ADDR']

    code = geo.country_code_by_addr(ip)
    if code is None:
        code = ''

    return code