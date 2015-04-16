from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import requests


# def land(request):
# 	return render_to_response('linked.html', { 'TITLE': 'Linked Data'})

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from indexinfo.models import indexdata,graphdata,queryfilenametable
from django.template import RequestContext
from linked.forms import LinkedForm
import json
from os import remove
import ConfigParser
import os
import sys

def land(request):
	indexdataobject = indexdata.objects.all()
	querynamedataobject = queryfilenametable.objects.all()
	if request.method == 'GET':
		form = LinkedForm()
		context = {'form': form,'TITLE' : 'Execute Sparql'}
		return render_to_response('linked.html', context,context_instance=RequestContext(request))

	elif request.method == 'POST':

		print request.POST
		try:
			format 	= request.POST.__getitem__('format')
			QueryId	= request.POST.__getitem__('queries')
			query = request.POST.__getitem__('qtext')
			settings = request.POST.__getitem__('settings')
		except:
			print "Linked Form Error:", sys.exc_info()[0]
			return HttpResponse("Form Not Valid!", status=500,content_type='plain/text')

		return executeQuery(query,format)

 		#WRITE QUERY TO FILE
# 		try:
# 			qf = open('queries/tempLinked.q', 'w')
# 			qf.write(query.encode(sys.stdout.encoding))
# 			qf.close()
# 		except:
# 			print "Unexpected File Error:", sys.exc_info()[0]
# 			return HttpResponse("File Error!", status=500,content_type='plain/text')

#		return HttpResponse("Received Form", status=200,content_type='plain/text')

def executeQuery(query,outputformat):
	reqData = {'query':query,'output':outputformat}
	headers = {'content-type': 'application/x-www-form-urlencoded'}
	resp = requests.post('http://134.193.128.130:3030/btc/query',params=reqData,headers=headers )
	response = HttpResponse(content=resp.text,content_type=outputformat+'; charset=utf-8')
	return response


def getTimings(request):

	 times = {}
	 times['type'] = 'cold'
	 times['riqf'] = '6.42'
	 times['riq'] = '16.29'
	 times['virt'] = '39.18'
	 times['jena'] = '3564.4'

	 return HttpResponse(json.dumps(times), content_type="application/json")


def getResults(request):

	f =  os.path.join(os.path.abspath(os.pardir),'RiQ/output/results.txt')
	outf = open(f,'r')
	data=outf.read()
	outf.close()

	return HttpResponse(data, content_type="plain/text")


def getQueryList(request):
	queryname = request.GET['name'].lower()
	query = """SELECT *
WHERE {
		SERVICE   <http://134.193.129.222:8080/endpoints/>{
			graph ?g {
				?s ?p "Brunei"@en .
			}
		}
}
"""
	if(queryname == 'f1'):
		query = """PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX movie: <http://data.linkedmdb.org/resource/movie/>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?film ?label ?subject WHERE {
	SERVICE <http://data.linkedmdb.org/sparql> {
		?film a movie:film .
		?film rdfs:label ?label .
		?film owl:sameAs ?dbpediaLink .
		FILTER(regex(str(?dbpediaLink), "dbpedia", "i"))
	}
	SERVICE <http://dbpedia.org/sparql> {
		?dbpediaLink dcterms:subject ?subject .
	}
}
LIMIT 50
"""
	elif(queryname == 'f2'):
		query ="""SELECT DISTINCT ?person
WHERE {
	SERVICE <http://dbpedia.org/sparql> {
		?person a <http://xmlns.com/foaf/0.1/Person> .
	}
} LIMIT 10
"""

	return HttpResponse(query,  content_type="text/plain")

class D3GraphData:
  def __init__(self):
    self.subject = None
    self.predicate = None
    self.object = None

class Candidate:
  def __init__(self):
    self.name = None