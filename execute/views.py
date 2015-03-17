from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from indexinfo.models import indexdata,graphdata,queryfilenametable
from django.template import RequestContext
from execute.forms import ExecuteForm
import json

def land(request):
	indexdataobject = indexdata.objects.all()
	querynamedataobject = queryfilenametable.objects.all()

	if request.method == 'GET':
		form = ExecuteForm()
		context = {'form': form,'TITLE' : 'Index Construction'}
		return render_to_response('execute.html', context,context_instance=RequestContext(request))

	elif request.method == 'POST':
		form = ExecuteForm()
		IndexName 	= request.POST.__getitem__('indexname')
		Dataset 		= request.POST.__getitem__('dataset')
		QueriesForm	= request.POST.__getitem__('queries')
		TypeCache 	= request.POST.__getitem__('typecache')
		optimizeType = request.POST.__getitem__('optimizationtype')

		print (IndexName ,Dataset ,QueriesForm,TypeCache,optimizeType)

		context = {'form': form,'TITLE' : 'Index Construction'}
		return render_to_response('execute.html', context,context_instance=RequestContext(request))


def getQueryList(request):
	queryname = request.GET['name'].lower()
	query = """SELECT *
WHERE {
	GRAPH ?g{
		?s ?p	?o .
	}
} LIMIT 10
"""
	if(queryname == 'btc1'):
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
	elif(queryname == 'btc2'):
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
	elif(queryname == 'dbpd1'):
		query = """PREFIX resource: <http://dbpedia.org/resource/>
PREFIX ontology: <http://dbpedia.org/ontology/>

#SELECT *
#SELECT ?g
SELECT ?city ?area ?code ?zone ?abstract ?postal ?water ?popu ?offset ?g
WHERE {
  GRAPH ?g {
    { ?city ontology:areaLand ?area .
      ?city ontology:areaCode ?code . }
    UNION
    { ?city ontology:timeZone ?zone .
      ?city ontology:abstract ?abstract . }
    ?city ontology:country resource:United_States .
    ?city ontology:postalCode ?postal .
    OPTIONAL { ?city ontology:areaWater ?water . }
    OPTIONAL { ?city ontology:populationTotal ?popu . }
    FILTER EXISTS { ?city ontology:utcOffset ?offset . }
  }
}
"""
	elif(queryname == 'dbpd2'):
		query = """PREFIX res: <http://dbpedia.org/resource/>
PREFIX onto: <http://dbpedia.org/ontology/>

#SELECT *
SELECT ?city ?area ?code ?zone ?abstract ?postal ?offset ?popu ?g
WHERE {
GRAPH ?g {
    { ?city onto:areaLand ?area .
    ?city onto:areaCode ?code . }
    UNION
    { ?city onto:timeZone ?zone .
    ?city onto:abstract ?abstract . }
    ?city onto:country res:United_States .
    ?city onto:postalCode ?postal .
    FILTER EXISTS { ?city onto:utcOffset ?offset . }
    OPTIONAL { ?city onto:populationTotal ?popu . }
    }
}
"""
	return HttpResponse(query,  content_type="text/plain")