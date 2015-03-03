from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse

def land(request):
	return render_to_response('execute.html', { 'TITLE': 'Execute SPARQL'})
