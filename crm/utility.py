# -*- coding: utf-8 -*-

import urllib2
import simplejson

def GeoIP(s):
	"""
	GeoIP info: http://freegeoip.net/static/index.html
	Restrictions: < 1,0000 queries an hour
	"""
	url = "http://freegeoip.net/json/"
	try:
		req = urllib2.urlopen(url + s)
		result = req.read()
		rpt = simplejson.loads(result)
		for key,value in rpt.iteritems():
			if key == "country_name":
				return value
		else:
			raise Http404("GeoIP 오류")
	except Exception, msg:
		print msg
		raise Http404(msg)