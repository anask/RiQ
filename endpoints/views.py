from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import time
import subprocess
import sys, os
import json
# import sh
# import pexpect
import fyzz
import glob
from subprocess import call

def land(request):

	tool = "RIQ"
	if request.method == 'GET':
			# forward query to RIQ
			query =  request.GET['query']
			print 'RIQ RECEIVED:'
			print query
			results = runQuery(query)
			return HttpResponse(content=results,content_type='xml; charset=utf-8')

	else:
			print ("RIQ GOT POST: ")
			print (request.POST)
			return HttpResponse(content="",content_type='xml; charset=utf-8')

def runQuery(query):
	createQueryFile(query)
	DIR  = os.path.join(os.path.abspath(os.pardir))
	cmd = [ DIR+"/RIS/indexing/RIS/scripts/run_riq_query.py", "-C", "config-files/riq.conf","-q", "queries/tempLinked.q", "-f" ,"xml"]
	print cmd
	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p_stdout = p.stdout.read()
	p_stderr = p.stderr.read()
	print(p_stdout)
 	print(p_stderr)

	try:
 		rfile = DIR+"/RIS/indexing/RIS.RUN/log/"+'query.'+'btc-2012-split-clean'+'.tempLinked.q.nopt.none.tdb2.xml.1.results'
 		with open (rfile, "r") as myfile:
 				data=myfile.read()
 				myfile.close()
		return HttpResponse(content=data,content_type='xml; charset=utf-8')
	except Exception as E:
 			print E
 			# Error, return empty xml #
 			selected_vars = getVars(qStr)
 			data =  getXML(selected_vars)
			return HttpResponse(content=data,content_type='xml; charset=utf-8')

def createQueryFile(queryStr):
        f = open('queries/tempLinked.q','w')
        f.write(queryStr)
        f.close()

def getVars (query):
	vrs=[]
	ast = fyzz.parse(query)
	if ast.selected == ['*']:
		varNDXs = [i for i in range(len(query)) if query.startswith('?', i)]
		for v in varNDXs:
			var = query[v+1:v+2]
			if var not in vrs:
				vrs.append(var)
	else:
		for v in ast.selected:
			vrs.append(v.name)
	return vrs

def getXML(variables):
	xmlDoc="""!<?xml version="1.0"?><sparql xmlns="http://www.w3.org/2005/sparql-results#"><head>"""
	for v in variables:
		xmlDoc=xmlDoc+'<variable name="'+v+'"/>'
	xmlDoc = xmlDoc + '</head></sparql>!'
	return xmlDoc
