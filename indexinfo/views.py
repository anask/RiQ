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
			print form.cleaned_data['dataset']
			print form.cleaned_data['lhskparameter']
			print form.cleaned_data['lhslparameter']
			print form.cleaned_data['maximumgraphs']
			print form.cleaned_data['bloomerror']
			print form.cleaned_data['graphindex']
			currentDate = datetime.now()

			indexName = form.cleaned_data['dataset'] + 'K' + form.cleaned_data['lhskparameter'] + 'L' + form.cleaned_data['lhslparameter'] + currentDate.strftime("%Y-%m-%d %H%M%S")

			indexdataobject = indexdata.objects.create(Dataset=form.cleaned_data['dataset'], LHSKParameter=form.cleaned_data['lhskparameter'], LHSLParameter=form.cleaned_data['lhslparameter'],MaximumGraphs=form.cleaned_data['maximumgraphs'], BloomError=form.cleaned_data['bloomerror'], BloomCapacity= form.cleaned_data['bloomcapacity'],  GraphIndex= form.cleaned_data['graphindex'], IndexName = indexName, CreateDate = currentDate )

			if indexdataobject.Dataset == 'BTC':
				indexdataobject.TotalGraphs = 10
			else:
				indexdataobject.TotalGraphs = 20

			RIQ_CONF =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/riq.conf')

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


			# Write prefix for the dataset and set its conf name
			DATASET_PREFIX_DIR =  os.path.join(os.path.abspath(os.pardir),'RIS/indexing/RIS.RUN/data/')
			FILE = ''

			if form.cleaned_data['dataset']=='BTC':
				FILE = 'btc-2012-split-clean'
			elif form.cleaned_data['dataset']=='LOGD':
				FILE = 'logd-dataset'
			elif form.cleaned_data['dataset']=='D10':
				FILE = 'd10-small-sample'

			config.set('Dataset', 'NAME',FILE)

			#Write new configuration

			f = open('riqtemp.conf.py','w')
			config.write(f)
			f.close()

			#print 'locale encoding: ' + locale.getpreferredencoding()
			# read the riqtemp.conf
			# create riq.conf
			q = open('riqtemp.conf.py')
			r = open('config-files/riq.conf', 'w')
			for line in q:
				if line.find(' = ') != -1:
					r.write(line.replace(' = ', '='))
				else:
					r.write(line)
			q.close()
			r.close()

			# remove riqtemp.conf
			remove('riqtemp.conf.py')
			pvstatus = constructPVs(DATASET_PREFIX_DIR+FILE)
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
def constructPVs(infile):
	#if (True):
	#	return "Written graphs: 1 % Avg graph size: 58 triples % Max graph size: 58 triples % Total size: 58 triples % Total URIs/literals: 0 % Duration: 0.0115s ".upper()
	RIQ_DIR  = os.path.join(os.path.abspath(os.pardir),'RIS')
	cmd = [ RIQ_DIR+"/indexing/code/rdf2spovec/rdf2spovec", '-f','nquads', '-i', infile+".nq", '-o', infile+".sigv2"]
	start = time.time()
	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p_stdout = p.stdout.read()
	p_stderr = p.stderr.read()
        end = time.time()
        dur = end - start
	outstr=''
	p_stdout = p_stdout.splitlines()
	for s in p_stdout:
		if s.startswith(('Written graphs','Avg graph', 'Max graph', 'Total size','Total URIs')):
			outstr = outstr + s +'%'
	end = time.time()
	dur = end - start
	outstr = outstr + 'Duration: '+str(round(dur,4))+'s'
	return outstr.upper()
