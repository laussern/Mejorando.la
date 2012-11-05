from utils import get_pais

def geo(req):
	return { 'geo_pais': get_pais(req.META).lower() }