from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def mainPage(request):
	variables = RequestContext(request, {
			'username': request.user.username,
			})
	
	return render_to_response('mainPage.html', variables)

def userRegister(request):
	pass
