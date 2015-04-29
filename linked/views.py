from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import requests
from run.views import createQueryFile
import subprocess

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
from thread import start_new_thread

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
			settings = request.POST.getlist('settings')
		except:
			print "Linked Form Error:", sys.exc_info()[0]

			return HttpResponse("Form Not Valid!", status=500,content_type='plain/text')
	
		tools=''
		if u'riq' in settings:
			tools = '1'
		else:
			tools = '0'
		
		if u'jena' in settings: 
			tools = tools + '1'
		else:
			tools = tools + '0'
		if u'virt' in settings:
			tools = tools + '1'
		else:
			tools = tools + '0'
               
		query = query.replace(' <http://134.193.129.222:8080/endpoints/>',' <http://134.193.129.222:8080/endpoints/?tools='+tools+'>')		
		start_new_thread(executeQuery,(query,format))
		print 'Spawning querying thread..'
                return HttpResponse('Query Received!', status=200,content_type='plain/text')


def executeQuery(query,outputformat):
	print 'Thread started'
	f = open('status/linked','w')
	f.write('started\n')
	f.close()
	filename = 'tempLinked.q'
	createQueryFile(query,filename)
	#reqData = {'query':query,'output':outputformat}
	#headers = {'content-type': 'application/x-www-form-urlencoded'}
	#resp = requests.post('http://134.193.128.130:3030/btc/query',params=reqData,headers=headers )
	#/tdbquery --loc=/mnt/data2/datasets/btc-2012-split-clean/btc-2012-split-clean.nq.tdb --query=/home/anask/RiQ/queries/tempLinked.q -v --optimize=off


	cmd = ['/home/vsfgd/Jena/apache-jena-2.11.1/bin/tdbquery','--loc','/mnt/data2/datasets/btc-2012-split-clean/btc-2012-split-clean.nq.tdb','--file', 'queries/'+filename,'--results',outputformat,'--optimize','off']
        print 'Issuing Linked Query:'
        print cmd
        p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_stdout = p.stdout.read()
        p_stderr = p.stderr.read()
        if len(p_stderr)>0:
             print 'Linked Query Error:'
             print(p_stderr)
       
        print 'Linked Query Finished'

	f = open('output/tempLinked.txt','w')
	f.write(p_stdout)
	f.close()

        f = open('status/linked','a')
        f.write('Done')
        f.close()

def getStatus(request):

                a=open('status/linked','rb')
                lines = a.readlines()
                a.close()
		print 'Linked Status: '+str(lines)

                if lines:
                        first_line = lines[:1]
                        last_line = lines[-1]

                if last_line == 'Done':
                        return HttpResponse("true")
                elif last_line == 'Error':
                        return HttpResponse("error")

                return HttpResponse("false")
def getTimings(request):

	 times = {}
	 times['type'] = 'cold'
	 times['riqf'] = '6.42'
	 times['riq'] = '16.29'
	 times['virt'] = '39.18'
	 times['jena'] = '3564.4'

	 return HttpResponse(json.dumps(times), content_type="application/json")


def getResults(request):

	f =  os.path.join(os.path.abspath(os.pardir),'RiQ/output/tempLinked.txt')
	outf = open(f,'r')
	data=outf.read()
	outf.close()

	#response = HttpResponse(content=resp.text,content_type=outputformat+'; charset=utf-8')
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
