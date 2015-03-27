from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json

def land(request):
	return render_to_response('visualize.html', { 'TITLE': 'Visualize Query'})


def getQueryInfo(request):
	with open('queries/temp.info') as json_file:
		json_data = json.load(json_file)

	return HttpResponse(json.dumps(json_data), content_type="application/json")


def getQueryCandidates(request):
	q = open('output/candidatedataindecimal.txt')
	candidates = {}
	i=0
	for line in q:
		candidates[i]=line.rstrip()
		i=i+1
	q.close
	jobj = {}
	jobj['candidates']=candidates

	return HttpResponse(json.dumps(jobj), content_type="application/json")