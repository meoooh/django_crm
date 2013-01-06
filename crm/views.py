from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required #from django.contrib.auth.decorators import login_required
def mainPage(request):
	variables = RequestContext(request, { # from django.template import RequestContext
			'username': request.user.username,
			})
	
	return render_to_response('mainPage.html', variables) # from django.shortcuts import render_to_response

def userRegister(request):
	pass
