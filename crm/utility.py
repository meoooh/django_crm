# -*- coding: utf-8 -*-

import urllib2
import simplejson
import iptools   # http://python-iptools.readthedocs.org/en/latest/
from django.http import Http404


def printException(exc):
	for i in exc:
		print i


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
			raise Http404
	except Exception, msg:
		print msg
		raise Http404


def ipValidation(t):
	if '/' in t:
		if iptools.ipv4.validate_cidr(t):
			return iptools.IpRange(t)
	elif '-' in t:
		s, e = t.split('-')
		
		if iptools.ipv4.validate_ip(s) and iptools.ipv4.validate_ip(e):
			return iptools.IpRange(s, e)
	elif '~' in t:
		s, e = t.split('~')
		
		if iptools.ipv4.validate_ip(s) and iptools.ipv4.validate_ip(e):
			return iptools.IpRange(s, e)
	else:
		if iptools.ipv4.validate_ip(t):
			return iptools.IpRange(t)
			
	return False


def supportREST(request):

	method = request.method

	if method == 'PUT' or method == 'DELETE':

		if hasattr(request, '_post'):
			del request._post
			del request._files

		try:
			request.method = 'POST'
			request._load_post_and_files()
			request.method = method

		except AttributeError:
			request.META['REQUEST_METHOD'] = 'POST'
			request._load_post_and_files()
			request.META['REQUEST_METHOD'] = method

		request.PUT = request.POST
		request.DELETE = request.POST

	return request