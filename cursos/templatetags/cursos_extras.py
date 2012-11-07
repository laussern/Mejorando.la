from django import template
from website.utils import get_code
from datetime import datetime

import pytz

register = template.Library()

@register.simple_tag
def mylocaltime(req, hours):
	result = ''

	code = get_code(req.META)

	if code:
		try:
			dt = datetime(2012, 12, 01, hours, 0, 0, tzinfo=pytz.utc)
			result = dt.astimezone(pytz.timezone(pytz.country_timezones[code][0])).strftime('%I%p')
		except: pass

	result = result.lower().lstrip('0')
	
	return result

@register.simple_tag
def mytimezone(req):
	result = ''

	code = get_code(req.META)

	if code:
		try:
			dt = datetime(2012, 12, 01, 0, 0, 0, tzinfo=pytz.utc)
			result = dt.astimezone(pytz.timezone(pytz.country_timezones[code][0])).strftime('%Z')
		except: pass


	return result