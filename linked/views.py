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
	GRAPH ?g{
		?s ?p	?o .
	}
} LIMIT 10
"""
	if(queryname == 'f1'):
		query = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX geo: <http://aims.fao.org/aos/geopolitical.owl#>
PREFIX collect: <http://purl.org/collections/nl/am/>
PREFIX ore: <http://www.openarchives.org/ore/terms/>
PREFIX fbase: <http://rdf.freebase.com/ns/>

SELECT ?s1 ?o1 ?s2 WHERE {
	GRAPH ?g {
		?s1 collect:acquisitionDate "1980-05-16" .
		?s1 collect:acquisitionMethod collect:t-14382 .
		?s1 collect:associationSubject ?o1 .
		?s1 collect:contentMotifGeneral collect:t-8782 .
		?s1 collect:creditLine collect:t-14773 .
		?s1 collect:material collect:t-3249 .
		?s1 collect:objectCategory collect:t-15606 .
		?s1 collect:objectName collect:t-10444 .
		?s1 collect:objectNumber "KA 17150" .
		?s1 collect:priref "23182" .
		?s1 collect:productionDateEnd "1924" .
		?s1 collect:productionDateStart "1924" .
		?s1 collect:productionPlace collect:t-624 .
		?s1 collect:title "Plate commemorating the first Amsterdam-Batavia flight"@en .
		?s1 ore:proxyFor collect:physical-23182 .
		?s1 ore:proxyIn collect:aggregation-23182 .
		?s1 collect:relatedObjectReference ?s2 .
		?s2 collect:relatedObjectReference ?s1 .
	}
}
"""
	elif(queryname == 'f2'):
		query ="""SELECT ?sub ?pred1 ?pred2 ?pred3 ?pred4
WHERE
{
	?sub ?pred1 <http://lexvo.org/id/term/afr/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/aze/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/bez/Hupanama> .
	?sub ?pred1 <http://lexvo.org/id/term/ces/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/cgg/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/cym/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/dan/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/dav/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/deu/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/dje/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/lav/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/lin/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/nmg/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/nno/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/nob/Panama> .
	?sub ?pred1 <http://lexvo.org/id/term/zul/i-Panama> .
	?sub ?pred2 <http://lexvo.org/id/un_m49/013> .
	?sub ?pred3 <lvont:GeographicRegion> .
	?sub ?pred4 <http://psi.oasis-open.org/iso/3166/#591> .
	?sub ?pred4 <http://sws.geonames.org/3703430/> .
}
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