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
# import fyzz
# import glob
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
# 	riq = './run_riq_query.py -C /home/anask/riq.conf.py -q /home/anask/temp.q  -c none  -r 1 -f xml'

	DIR  = os.path.join(os.path.abspath(os.pardir))
	cmd = [ "python", DIR+"/RIS/indexing/RIS/scripts/run_riq_query.py", "-C", "RiQ/config-files/riq.conf","-q", "RiQ/tempLinked.q",  "-c" ,"none" , "-r", "1", "-f" ,"xml"]

	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	p_stdout = p.stdout.read()
	p_stderr = p.stderr.read()
	print(p_stdout)
 	print(p_stderr)

#
#
#
#
# 	usr=os.getlogin()
# 	os.chdir('/home/'+usr+'/RIS/indexing/RIS/scripts/')
#
#         child = ' '
# 	try:
#                 child = pexpect.spawn("su")
#         except:
#                 print "Unable to login as root."
#                 sys.exit()
#
#         i = child.expect([pexpect.TIMEOUT, "Password:"])
#
#         if i == 0:
#                 print "Timed out when logging into root."
#                 sys.exit()
#         if i == 1:
#                 child.sendline("yeb4<slav")
#
# 		try:
# 			riq = './run_riq_query.py -C /home/anask/riq.conf.py -q /home/anask/temp.q  -c none  -r 1 -f xml'
# 			child.sendline(riq)
# 			child.expect('Done.')
# 			# print results #
# 			files= glob.glob('/home/anask/log/*.results')
# 			with open (files[0], "r") as myfile:
# 				data=myfile.read()
# 				print '!'+data+'!'
# 				myfile.close()
# 		except Exception as E:
# 			print E
# 			# Error, return empty xml #
# 			selected_vars = getVars(qStr)
# 			print getXML(selected_vars)

def createQueryFile(queryStr):
        f = open('queries/tempLinked.q','w')
        f.write(queryStr)
        f.close()
 		#WRITE QUERY TO FILE
# 		try:
# 			qf = open('queries/tempLinked.q', 'w')
# 			qf.write(query.encode(sys.stdout.encoding))
# 			qf.close()
# 		except:
# 			print "Unexpected File Error:", sys.exc_info()[0]
# 			return HttpResponse("File Error!", status=500,content_type='plain/text')

#		return HttpResponse("Received Form", status=200,content_type='plain/text')

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
