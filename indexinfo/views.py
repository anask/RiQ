from django.shortcuts import render_to_response, redirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from datetime import datetime
from os import remove
import ConfigParser
from pexpect import pxssh
import subprocess
import locale
import csv
import sys
import requests
import json
import os
import getpass
import time
from indexinfo.models import indexdata,graphdata,queryfilenametable
from indexinfo.forms import IndexConstructionForm

def land(request):
	if request.method == 'POST':
		form = IndexConstructionForm(request.POST)

		if form.is_valid():
# 			print form.cleaned_data['dataset']
# 			print form.cleaned_data['lhskparameter']
# 			print form.cleaned_data['lhslparameter']
# 			print form.cleaned_data['maximumgraphs']
# 			print form.cleaned_data['bloomerror']
# 			print form.cleaned_data['graphindex']
			currentDate = datetime.now()

			indexName = form.cleaned_data['dataset'] + 'K' + form.cleaned_data['lhskparameter'] + 'L' + form.cleaned_data['lhslparameter'] + currentDate.strftime("%Y-%m-%d %H%M%S")

			indexdataobject = indexdata.objects.create(Dataset=form.cleaned_data['dataset'], LHSKParameter=form.cleaned_data['lhskparameter'], LHSLParameter=form.cleaned_data['lhslparameter'],MaximumGraphs=form.cleaned_data['maximumgraphs'], BloomError=form.cleaned_data['bloomerror'], BloomCapacity= form.cleaned_data['bloomcapacity'],  GraphIndex= form.cleaned_data['graphindex'], IndexName = indexName, CreateDate = currentDate )

			if indexdataobject.Dataset == 'BTC':
				indexdataobject.TotalGraphs = 10
			else:
				indexdataobject.TotalGraphs = 20

			RIQ_CONF =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/riq.conf')
			print ('Opening: '+RIQ_CONF)
			print('Setting..')
			#indexdataobject.save()
			config = ConfigParser.RawConfigParser()
			config.optionxform=str
			config.read(RIQ_CONF)
			config.set('DEFAULT', 'USER', 'anask') # getpass.getuser()
			config.set('LSH','LSHK',form.cleaned_data['lhskparameter'])
			config.set('LSH','LSHL',form.cleaned_data['lhslparameter'])
			config.set('Limits', 'MAXCCSIZE',form.cleaned_data['maximumgraphs'])
			#config.set('Section=GRAPHS', 'GRAPHS2INDEX',form.cleaned_data['graphindex'])
			config.set('Dablooms', 'CAPACITY',form.cleaned_data['bloomcapacity'])
			config.set('Dablooms', 'ERROR_RATE',form.cleaned_data['bloomerror'])
			print('Setting..Done.')

			# Write prefix for the dataset and set its conf name
			DATASET_PREFIX_DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/data/')
			FILE = ''

			if form.cleaned_data['dataset']=='BTC':
				FILE = 'btc-2012-split-clean'
			elif form.cleaned_data['dataset']=='LOGD':
				FILE = 'dbpedia'
			elif form.cleaned_data['dataset']=='D10':
				FILE = 'd10-small-sample'

			config.set('Dataset', 'NAME',FILE)

			#Write new configuration

			f = open('riqtemp.conf','w')
			config.write(f)
			f.close()

			#print 'locale encoding: ' + locale.getpreferredencoding()
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
			pvstatus = constructPVs(DATASET_PREFIX_DIR,FILE)
			return render_to_response('index.html', {'form': form, 'TITLE' : 'Index Construction','IndexName' : indexName, 'PVStatus':pvstatus}, context_instance=RequestContext(request))
		else:
			print 'form is invalid'
			print form.errors
			return render_to_response('index.html', {'form': form,'TITLE' : 'Index Construction'}, context_instance=RequestContext(request))
	else:
		form = IndexConstructionForm()
		context = {'form': form,'TITLE' : 'Index Construction'}
		return render_to_response('index.html', context, context_instance=RequestContext(request))

# Assuming RIQ's code is in the same main directory as the demo
def constructPVs(prefix, infile):
	#Construct PVs
	if (True):
		return """{"Avg graph size":" 14 triples","Written graphs":" 4","Max graph size":" 46 triples","group":{"lsh2gids_size":40,"pv_lsh_t":0.782208,"groups":3,"build_graph_t":0.810623,"union_t":0.80684,"total_t":0.291724},"split":{"split_t":0.5},"pv_t":"0.44420185089","cbf":{"cbf_t":0.31682},"Total URIs/literals":" 0","Total size":" 58 triples"}"""
	RIQ_DIR  = os.path.join(os.path.abspath(os.pardir),'RIS')
	cmd = [ RIQ_DIR+"/indexing/code/rdf2spovec/rdf2spovec", '-f','nquads', '-i', prefix+infile+".nq", '-o', prefix+infile+".sigv2"]
	start = time.time()
	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p_stdout = p.stdout.read()
	p_stderr = p.stderr.read()
	end = time.time()
	pvdur = {u'pv_t' : str(end - start)}
	json_data = {u'content':'none'}

	#Run indexing
	cmdi = [ RIQ_DIR+"/indexing/RIS/scripts/run_riq_index.py", "-v" ,"-C", "../RiQ/config-files/riq.conf"]
	pi = subprocess.Popen(cmdi, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	pi_stdout = pi.stdout.read()
	pi_stderr = pi.stderr.read()
	print(pi_stdout)

	#Get results
	if (len(p_stderr)==0):
		with open(RIQ_DIR+"/indexing/RIS.RUN/log/index."+infile+".all.json") as json_file:
			json_data = json.load(json_file)
			json_data.update(pvdur)
		p_stdout = p_stdout.splitlines()
		for s in p_stdout:
			if s.startswith(('Written graphs','Avg graph', 'Max graph', 'Total size','Total URIs')):
				s=s.split(":")
				j =  {s[0]:s[1]}
				json_data.update(j)

	else:
		return "ERRORs: FOUND % DURATION: "+str(dur)

	return json.dumps(json_data)
