from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from indexinfo.models import indexdata,graphdata,queryfilenametable
from django.template import RequestContext
from execute.forms import ExecuteForm
from run.views import *
import json
from os import remove
import ConfigParser
import os
import sys
import glob
def land(request):
	indexdataobject = indexdata.objects.all()
	querynamedataobject = queryfilenametable.objects.all()
	queryInfo = {}
	if request.method == 'GET':
		form = ExecuteForm()
		context = {'form': form,'TITLE' : 'Execute Sparql'}
		return render_to_response('execute.html', context,context_instance=RequestContext(request))

	elif request.method == 'POST':

		print request.POST
		try:
			IndexName 	= request.POST.__getitem__('indexname')
			QueryId	= request.POST.__getitem__('queries')
			query = request.POST.__getitem__('qtext')
			queryInfo['index']=IndexName
			queryInfo['name']=QueryId

			#*************** WRITE NEW DATASET NAME ***************
			RIQ_CONF =  ('config-files/riq.conf')

			config = ConfigParser.RawConfigParser()
			config.optionxform=str
			config.read(RIQ_CONF)

			# Write prefix for the dataset and set its conf name
			DATASET_PREFIX_DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/data/')
			FILE = ''

			if   IndexName == 'BTC':
				FILE = 'btc-2012-split-clean'
			elif IndexName == 'LOGD':
				FILE = 'dbpedia'
			elif IndexName == 'D10':
				FILE = 'd10-small-sample'

			config.set('Dataset', 'NAME',FILE)

			#Write new configuration


			f = open('riqtemp.conf','w')
			config.write(f)
			f.close()

			# read the riqtemp.conf
			# create riq.conf
			q = open('riqtemp.conf')
			r = open('config-files/riq.conf', 'w')
			for line in q:
				if line.find(' = ') != -1:
					r.write(line.replace(' = ', '='))
				else:
					r.write(line)
			q.close()
			r.close()

			# remove riqtemp.conf
			remove('riqtemp.conf')
			#******************************************************
		except:
			return HttpResponse("Form Not Valid!", status=500,content_type='plain/text')


		#DETERMINE CACHE/OPT PARAMETERS
		try:
			TypeCache 	= request.POST.__getitem__('typecache')
		except:
			TypeCache = 'warm'
		try:
			optimizeType = request.POST.__getitem__('optimizationtype')
		except:
			optimizeType = 'opt'

		if(TypeCache=='warm'):
			TypeCache = '-c warm'
			queryInfo['cache']='Warm'
		else:
			TypeCache = '-c cold'
			queryInfo['cache']='Cold'

		if(optimizeType=='opt'):
			optimizeType = '-O'
			queryInfo['opt']='Enabled'
		else:
			optimizeType = ''
			queryInfo['opt']='Disabled'

		args = " "+TypeCache+" "+optimizeType+" "

		qi = open('queries/temp.info', 'w')
		qi.write(json.dumps(queryInfo).encode('utf-8'));
		qi.close()

		# Run the query
		results = runQuery(query.encode(sys.stdout.encoding), args,"temp.q")
		if (results.startswith("error")):
			return HttpResponse(results , status=600,content_type='plain/text')
		return HttpResponse("Received Query", status=200,content_type='plain/text')

def getTimings(request):

	 times = {}
	 times['type'] = 'cold'
	 times['riqf'] = '6.42'
	 times['riq'] = '16.29'
	 times['virt'] = '39.18'
	 times['jena'] = '3564.4'

	 return HttpResponse(json.dumps(times), content_type="application/json")


def getResults(request):
	data = getQueryResults('temp.q')
	return HttpResponse(content=data,content_type='xml; charset=utf-8')

def getQueryGraph(request):
	filename = 'temp.q'	
	DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/log/')
        bgpfile = ''
        file_dir_extension = os.path.join(DIR, '*'+filename+'*filter.1.log')
	print 'Getting TPs in the query from:'
        for name in glob.glob(file_dir_extension):
		print name
                bgpfile = name

	rlog = open(bgpfile)
	bStartRead = 0
	d3records = {}
	d3record = {}
	#graphdataobject.subject =  set the value of subject
	i=0
	for line in rlog:

		if line.startswith('structure format:') == True & bStartRead == 0:
				bStartRead = 1

		if (line.startswith('subject') == True) & bStartRead == 1:
				d3record['subject'] = line[line.find(': ')+1:].rstrip('\n')


		if (line.startswith('predicate') == True) & bStartRead == 1:
				d3record['predicate'] = line[line.find(': ')+1:].rstrip('\n')


		if (line.startswith('object') == True) & bStartRead == 1:
				d3record['object'] = line[line.find(': ')+1:].rstrip('\n')
				d3records[i] = d3record
				d3record = {}
				i=i+1

		if line.find('parse_tree size:') != -1:
				break


	rlog.close()
	#move this code to visualize
	#DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/log/')
        #candidatefile = ''
        #file_dir_extension = os.path.join(DIR, '*'+filename+'*filter.candidates')
        #for name in glob.glob(file_dir_extension):
        #        print name
        #        candidatefile = name

	#candidatelog = open(candidatefile)

	#demodir =  os.path.join(os.path.abspath(os.pardir),'RiQ/')

	#candidatelogindecimal = open(demodir+"output/candidatedataindecimal.txt", 'w')
	#for line in candidatelog:
	#	binarytodecimal = str(int(line, 2))
		#print binarytodecimal
		#print ('Candidate' + binarytodecimal)
	#	candidatelogindecimal.write('Candidate' + binarytodecimal + '\n')

	#candidatelog.close()
	#candidatelogindecimal.close()

	#print(d3records)
	#html = "<html><body> "+"Hello"+"</body></html>"

	return HttpResponse(json.dumps(d3records), content_type="application/json")


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
	elif(queryname == 'btc10'):
		query ="""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT *
WHERE {
	GRAPH ?g {
		?var6 a <http://dbpedia.org/ontology/PopulatedPlace> .
		?var6 <http://dbpedia.org/ontology/abstract> ?var1 .
		?var6 rdfs:label ?var2 .
		?var6 geo:lat ?var3 .
		?var6 geo:long ?var4 .
		{
			?var6 rdfs:label "Brunei"@en .
		}
		UNION
		{
			?var5 <http://dbpedia.org/property/redirect> ?var6 .
			?var5 rdfs:label "Brunei"@en .
			OPTIONAL { ?var6 foaf:homepage ?var10 }
			OPTIONAL { ?var6 <http://dbpedia.org/ontology/populationTotal> ?var12 }
			OPTIONAL { ?var6 <http://dbpedia.org/ontology/thumbnail> ?var14 }
		}
	}
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
