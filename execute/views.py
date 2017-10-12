from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from indexinfo.models import indexdata,graphdata,queryfilenametable
from django.template import RequestContext
from execute.forms import ExecuteForm
from run.views import *
from thread import start_new_thread
import json
from os import remove
import ConfigParser
import os
import sys
import glob
import time
import traceback
from shutil import copyfile

def land(request):
	indexdataobject = indexdata.objects.all()
	querynamedataobject = queryfilenametable.objects.all()
	queryInfo = {}
	if request.method == 'GET':
		form = ExecuteForm()
		context = {'form': form,'TITLE' : 'Execute Sparql'}
		return render_to_response('execute.html', context,context_instance=RequestContext(request))

	elif request.method == 'POST':

		#print request.POST
		try:
			IndexName 	= request.POST.__getitem__('indexname')
			QueryId	= request.POST.__getitem__('queries')
			query = request.POST.__getitem__('qtext')
			queryInfo['index']=IndexName
			queryInfo['name']=QueryId
			#updateDatasetName(IndexName)
			selectConfigFile(IndexName)
			queryInfo['namedgraphs'] = getStoredNumberNamedGraphs(QueryId)

		except Exception,e: 
			print str(e)
			return HttpResponse("Form Not Valid!", status=500,content_type='plain/text')


		#DETERMINE CACHE/OPT PARAMETERS
		try:
			TypeCache = request.POST.__getitem__('typecache')
		except:
			TypeCache = 'none'#was warm
		try:
			optimizeType = request.POST.__getitem__('optimizationtype')
		except:
			optimizeType = 'opt'

		if(TypeCache=='warm'):
			TypeCache = '-c none'#was warm
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

		qi = open('queries/temp.info', 'w')
		qi.write(json.dumps(queryInfo).encode('utf-8'));
		qi.close()

		s = open('status/execute', 'w')
		s.write('Started..\n')
		s.close()
		if QueryId[0] in ['B','L']:
			tools=[True,False,False]
		else:
			tools=[True,True,True]
		#	return HttpResponse("Results from previous\n   runs will be shown!", status=200,content_type='plain/text')

		args = " "+TypeCache+" "+optimizeType+" "


		removePreviousRunFiles('execute')
		print('Issuing Query..')			
		tools=[True,False,False]
		r=runMultiToolQuery('temp.q',query.encode(sys.stdout.encoding),args,tools)
	
          	s = open('status/execute', 'a')
                s.write('Done\n')
                s.close()
		#start_new_thread(runQuery,(query.encode(sys.stdout.encoding),args,'temp.q','riq')

		return HttpResponse('Query Received!', status=200,content_type='plain/text')
def getStoredNumberNamedGraphs(qId):
    return {
        'BTC1':'1' ,
        'BTC2':'2' ,
        'BTC3':'0' ,
        'BTC4':'2,020' ,
        'BTC5':'3,691' ,
        'BTC6':'3,691' ,
        'BTC7':'6,413' ,
        'BTC8':'1' ,
        'BTC9':'25,016',
        'BTC10':'25,016',
        'BTC11':'123,171',
        'LUBM1':'0' ,
        'LUBM2': '1',
        'LUBM3':'6' ,
        'LUBM4': '0',
        'LUBM5': '21',
        'LUBM6': '21',
        'LUBM7': '175,559',
        'LUBM8': '179,847',
        'LUBM9': '200,004',
        'LUBM10':'200,004',
        'LUBM11':'200,004',
        'CUSTOM':'N/A',
    }[qId]

def selectConfigFile(indexName):	
	if indexName == 'BTC':
		FILE = 'btc'
	elif indexName == 'LUBM':
		FILE = 'lubm'
	copyfile('config-files/riq.conf.'+FILE, 'config-files/riq.conf')


def updateDatasetName(IndexName):
			DATASET_PREFIX_DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/data/')
			FILE = ''

			if IndexName == 'BTC':
				FILE = 'btc-2012-split-clean'
			elif IndexName == 'LOGD':
				FILE = 'dbpedia'
			elif IndexName == 'D10':
				FILE = 'd10-small-sample'
			elif IndexName == 'LUBM':
				FILE = 'UbaData-1.38B'

			RIQ_CONF =  ('config-files/riq.conf')

			config = ConfigParser.RawConfigParser()
			config.optionxform=str
			config.read(RIQ_CONF)

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

			remove('riqtemp.conf')

def getStoredTimings(c,qId,times):
	if c=='warm':
		if qId == 'BTC1':
			times['virt'] = '0.13'
			times['jena'] = '13.15'
			times['rf'] = '14400'
		elif qId == 'BTC2':
			times['virt'] = '4.43'
			times['jena'] = '20.51'
			times['rf'] = '14400'
		elif qId == 'BTC3':
			times['virt'] = '1.43'
			times['jena'] = '13.30'
			times['rf'] = '276.72'
		elif qId == 'BTC4':
			times['virt'] = '950.07'
			times['jena'] = '148.39'
			times['rf'] = '990.72'
		elif qId == 'BTC5':
			times['virt'] = '10.33'
			times['jena'] = '21.65'
			times['rf'] = '14400'
		elif qId == 'BTC6':
			times['virt'] = '342.79'
			times['jena'] = '56.59'
			times['rf'] = '14400'
		elif qId == 'BTC7':
			times['virt'] = '2.69'
			times['jena'] = '17.09'
			times['rf'] = '387.50'
		elif qId == 'BTC8':
			times['virt'] = '0.16'
			times['jena'] = '369.81'
			times['rf'] = '0'
		elif qId == 'BTC9':
			times['virt'] = '60.42'
			times['jena'] = '33.36'
			times['rf'] = '0'
		elif qId == 'BTC10':
			times['virt'] = '88.36'
			times['jena'] = '38.77'
			times['rf'] = '0'
		elif qId == 'BTC11':
			times['virt'] = '120.28'
			times['jena'] = '2102.06'
			times['rf'] = '0'

		elif qId == 'LUBM1':
			times['virt'] = '77.99'
			times['jena'] = '2.76'
			times['rf'] = '14400'

		elif qId == 'LUBM2':
			times['virt'] = '0.30'
			times['jena'] = '5.05'
			times['rf'] = '14400'

		elif qId == 'LUBM3':
			times['virt'] = '36.58'
			times['jena'] = '244.82'
			times['rf'] = '14400'

		elif qId == 'LUBM4':
			times['virt'] = '0.003'
			times['jena'] = '1.10'
			times['rf'] = '14400'
		elif qId == 'LUBM5':
			times['virt'] = '0.005'
			times['jena'] = '1.43'
			times['rf'] = '486.48'

		elif qId == 'LUBM6':
			times['virt'] = '0.16'
			times['jena'] = '3.67'
			times['rf'] = '600'

		elif qId == 'LUBM7':
			times['virt'] = '43.04'
			times['jena'] = '2346.31'
			times['rf'] = '14400'
		elif qId == 'LUBM8':
			times['virt'] = '37.43'
			times['jena'] = '2353.21'
			times['rf'] = '14400'

		elif qId == 'LUBM9':
			times['virt'] = '137.42'
			times['jena'] = '1445.41'
			times['rf'] = '1219.84'


		elif qId == 'LUBM10':
			times['virt'] = '303.62'
			times['jena'] = '14400'
			times['rf'] = '1315.40'

		elif qId == 'LUBM11':
			times['virt'] = '929.37'
			times['jena'] = '1511'
			times['rf'] = '1485'


	elif c=='cold':
		if qId == 'BTC1':
			times['virt'] = '5.92'
			times['jena'] = '15.79'
			times['rf'] = '14400'
		elif qId == 'BTC2':
			times['virt'] = '6.04'
			times['jena'] = '23.21'
			times['rf'] = '14400'
		elif qId == 'BTC3':
			times['virt'] = '4.50'
			times['jena'] = '16.58'
			times['rf'] = '296.99'
		elif qId == 'BTC4':
			times['virt'] = '965'
			times['jena'] = '295.77'
			times['rf'] = '1010.77'
		elif qId == 'BTC5':
			times['virt'] = '86.71'
			times['jena'] = '668.28'
			times['rf'] = '14400'
		elif qId == 'BTC6':
			times['virt'] = '350.19'
			times['jena'] = '684.97'
			times['rf'] = '14400'
		elif qId == 'BTC7':
			times['virt'] = '81.94'
			times['jena'] = '803.94'
			times['rf'] = '405.29'
		elif qId == 'BTC8':
			times['virt'] = '39.18'
			times['jena'] = '3564.4'
			times['rf'] = '0'
		elif qId == 'BTC9':
			times['virt'] = '142.89'
			times['jena'] = '648.93'
			times['rf'] = '0'
		elif qId == 'BTC10':
			times['virt'] = '165.52'
			times['jena'] = '663.31'
			times['rf'] = '0'
		elif qId == 'BTC11':
			times['virt'] = '237.58'
			times['jena'] = '2050.62'
			times['rf'] = '0'

		elif qId == 'LUBM1':
			times['virt'] = '136.62'
			times['jena'] = '233.59'
			times['rf'] = '14400'

		elif qId == 'LUBM2':
			times['virt'] = '55.87'
			times['jena'] = '520.91'
			times['rf'] = '14400'

		elif qId == 'LUBM3':
			times['virt'] = '119.62'
			times['jena'] = '523.78'
			times['rf'] = '14400'

		elif qId == 'LUBM4':
			times['virt'] = '13.96'
			times['jena'] = '4.83'
			times['rf'] = '14400'

		elif qId == 'LUBM5':
			times['virt'] = '6.16'
			times['jena'] = '511.88'
			times['rf'] = '79.09'

		elif qId == 'LUBM6':
			times['virt'] = '9.19'
			times['jena'] = '600'
			times['rf'] = '79.30'

		elif qId == 'LUBM7':
			times['virt'] = '2349.70'
			times['jena'] = '14400'
			times['rf'] = '0'


		elif qId == 'LUBM8':
			times['virt'] = '2357.7'
			times['jena'] = '14400'
			times['rf'] = '0'


		elif qId == 'LUBM9':
			times['virt'] = '1432.42'
			times['jena'] = '1232.02'
			times['rf'] = '0'

		elif qId == 'LUBM10':
			times['virt'] = '14400'
			times['jena'] = '1327.42'
			times['rf'] = '0'

		elif qId == 'LUBM11':
			times['virt'] = '1511'
			times['jena'] = '1521.32'
			times['rf'] = '0'

def getTimings(request):

	qId = request.GET['queryId']
	c = request.GET['cache']
	o = request.GET['opt']
        index = request.GET['index']

	times = {}
	times['type'] = c
	print 'Getting timings..'
	print 'Query: '+qId
	print 'Cache: '+c
	print 'Optimization: '+o
   
    	a=open('status/execute','rb')
        lines = a.readlines()
        a.close()
	print lines
        if lines:
		
                slast_line = lines[-2]
                last_line = lines[-1].rstrip('\n')

		# was there any error?
		err = False
		err_l = ''
		for l in lines:
    			if 'Error' in l:
				err = True
				err_l = l
	
                if last_line == 'Done':	
	                t = slast_line.rstrip('\n').split(':')[1].split(',')
			if qId != 'CUSTOM':
				if (qId[0].upper() == index[0].upper()):
					#get stored timings for virt, jena, rf
					getStoredTimings(c,qId,times)
				else:
	                        	times['virt'] = '0'
                        		times['jena'] = '0'
                        		times['rf'] = '0'		
			else:
				times['virt'] = t[2]
				times['jena'] = t[1]
				times['rf'] = '0'

        	        tr= t[0].split('/')
               		times['riqf'] = format(float(tr[1]), '.2f')
                	times['riq'] =  format(float(tr[0]), '.2f')

                elif last_line == 'Error':
                        times['riqf'] = '10'
                        times['riq'] =  '10'
                        times['virt'] = '10'
                        times['jena'] = '10'
                        times['rf'] = '10'
        else:
                        times['riq']  = '15'
                        times['riqf'] = '15'
                        times['virt'] = '15'
                        times['jena'] = '15'
                        times['rf'] = '15'
	print 'Returning Times:' 
	print times
	return HttpResponse(json.dumps(times), content_type="application/json")


def getResults(request):
	qId = request.GET['queryId']
	c = request.GET['cache']
	o = request.GET['opt']

	if c=='warm':
		c='none'

	#if qId == 'CUSTOM':
	data = getQueryResults('temp.q','riq',c)
	return HttpResponse(content=data,content_type='xml; charset=utf-8')
	#elif qId == 'BTC10':
	#	data = getQueryResults('q20.','riq',c)
	#	return HttpResponse(content=data,content_type='xml; charset=utf-8')
	#elif qId == 'BTC11':
	#	data = getQueryResults('q3.','riq',c)
	#	return HttpResponse(content=data,content_type='xml; charset=utf-8')

def getStatus(request):

		a=open('status/execute','rb')
		lines = a.readlines()
		a.close()
		if lines:
			first_line = lines[:1]
			last_line = lines[-1].rstrip()

		if last_line == 'Done':
			return HttpResponse("true", status=200,content_type='plain/text')
		elif last_line == 'Error':
			return HttpResponse("error", status=200,content_type='plain/text')
		print last_line
		return HttpResponse("false", status=200,content_type='plain/text')

def getQueryGraph(request):

	qId = request.GET['queryId']
	c = request.GET['cache']
	o = request.GET['opt']

	if (c=='warm'):
		c='none'	
	filename = 'temp.q'


	DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/log/')
        bgpfile = ''
       

	file_dir_extension = os.path.join(DIR, '*'+filename+"."+o+"."+c+'*filter.1.log')

	print ('Openning dir: '+file_dir_extension)
	print 'Getting TPs in the query from:'
        for name in glob.glob(file_dir_extension):
		print 'File: '+name
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

	return HttpResponse(json.dumps(d3records), content_type="application/json")

def getQueryByName(qname): 
	if qname != 'CUSTOM':
		print('Retriving query from file: '+qname+'.q')
		queryfile =  open("queries/"+qname+'.q', "r")
		query = queryfile.read()
		queryfile.close() 
	else:
		query = """SELECT *
WHERE {
	GRAPH ?g {
		?s ?p	"Brunei"@en .
	}
}
"""
	return query

def getQueryList(request):
	queryname = request.GET['name']
	
	if queryname != 'CUSTOM':
		if 'BTC' in queryname:
			dataset = 'BTC'	
		elif 'LUBM' in queryname:
			dataset = 'LUBM'

		queryname = dataset[0].upper() + queryname[len(dataset):] 
	
	query = getQueryByName(queryname)

	return HttpResponse(query,  content_type="text/plain")

class D3GraphData:
  def __init__(self):
    self.subject = None
    self.predicate = None
    self.object = None

class Candidate:
  def __init__(self):
    self.name = None
