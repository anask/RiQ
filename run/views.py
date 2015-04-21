from django.shortcuts import render
import json
import time
import subprocess
import sys, os
import json
import fyzz
import glob
from subprocess import call
from django.shortcuts import render
import json
import time
import subprocess
import sys, os
import json
import fyzz
import glob
from subprocess import call

def runQuery(query,args,filename):
	createQueryFile(query,filename)
	DIR  = os.path.join(os.path.abspath(os.pardir))
	args = args.split()
	cmd = [ DIR+"/RIS/indexing/RIS/scripts/run_riq_query.py", "-C", "config-files/riq.conf","-q", "queries/"+filename, "-f" ,"xml"]
	for a in args:
		cmd.append(a)
	print cmd
 	p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 	p_stdout = p.stdout.read()
 	p_stderr = p.stderr.read()
	print 'Running RIQ..'
 	print(p_stdout)
 	if len(p_stderr)>0:
 		print(p_stderr)
	output = p_stdout.split('\n')
	for s in output:
		if s.startswith("error"):
			return s
		elif s == "Done.":
                        return s


def getQueryResults(filename):
	DIR  = os.path.join(os.path.abspath(os.pardir))
	try:
		rFile = ''
		file_dir_extension = os.path.join(DIR+"/RIS/indexing/RIS.RUN/log/", '*'+filename+'*.results')
		print 'locating results file: '+file_dir_extension

		for name in glob.glob(file_dir_extension):
			print name
			rFile = name

 		with open (rFile, "r") as myfile:
 				dataStr=myfile.read()
 				myfile.close()

		
		return dataStr
	except Exception as E:
		print 'Results Error:'
		print E
		# Error, return empty xml #
		f =  DIR+'/RiQ/queries/'+filename
		outf = open(f,'r')
		qStr=outf.read()
		outf.close()
		selected_vars = getVars(qStr)
		data =  getXML(selected_vars)
		return data

def createQueryFile(queryStr,filename):
        f = open('queries/'+filename,'w')
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
	xmlDoc="""<?xml version="1.0"?><sparql xmlns="http://www.w3.org/2005/sparql-results#"><head>"""
	for v in variables:
		xmlDoc=xmlDoc+'<variable name="'+v+'"/>'
	xmlDoc = xmlDoc + '</head></sparql>'
	return xmlDoc
