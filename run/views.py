from django.shortcuts import render
import json
import time
import subprocess
import sys, os
import traceback
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
import shutil
import time
import urllib
from threading import Thread
def start ():

	cmd = ["virtuoso-t","-f"]
        print 'Starting Virtuoso..'
        p = subprocess.Popen(cmd, cwd="/var/lib/virtuoso/db", shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_stdout = p.stdout.read()
        p_stderr = p.stderr.read()
        if len(p_stderr)>0:
             print 'Virtuoso Start Error:'
             print(p_stderr)
	print p_stdout

def stop ():

        cmd = ["pkill","virtuoso"]
        print 'Stopping Virtuoso..'
        p = subprocess.Popen(cmd, cwd="/var/lib/virtuoso/db", shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p_stdout = p.stdout.read()
        p_stderr = p.stderr.read()
        if len(p_stderr)>0:
             print 'Virtuoso Stop Error:'
             print(p_stderr)
        print p_stdout

def runq(filename):
		print 'Reading query for virtuoso..'
                with open ("queries/"+filename, "r") as qFile:
                     query = qFile.read().replace('\n', ' ').replace("<div>","").replace("</div>","").strip()
                qFile.close()

                myParameters = {'query': query, 'format': 'application/sparql-results+xml','timeout':'90000000','debug':'on'}
                print 'Issuing request..'

                myPort = "8890"
                myURL = "http://localhost:%s/sparql?%s" % (myPort, urllib.urlencode(myParameters))
                data = urllib.urlopen(myURL).read()
                print 'received response'
                return data

def runMultiToolQuery(filename,query,args,tools):
		print '\n\nFilename: '+filename
		times = ['-1','-1','-1']

		if(filename=='temp.q'):
			status='execute'
		else:
			status='linked'
		sFile = open('status/'+status,'a')
		if (tools[0]==True):
			sFile.write('Running Query via RIQ..\n')
			sFile.flush()
			start = time.time()
			results1 = runQuery(query, args,filename,'riq')
			end = time.time()
			sFile.write('RIQ Finished.\n')
			if (results1.startswith("error")):
				times[0] ='0/'+str(end-start)
				#isFile.write('RIQ: '+results1+' ['+str(times[0])+']\n')
				if 'NoMatch' not in results1:#found a real error
					print 'Querying RIQ: found an error!'
					sFile.close()
					return 'error'
			if(status=='linked'):
				times[0] = getRiqTime(filename,args)[0]
			elif times[0] == '-1':
				rtime = getRiqTime(filename,args)
				times[0] = str(rtime[0])+'/'+str(rtime[1])

		if (tools[1]==True):
			if 'cold' in args:
				print 'Run jena in Cold'
				clearCache()
			sFile.write('Running Query via JenaTDB..\n')
			sFile.flush()
			start = time.time()
			results2 = ""#runQuery(query, args,filename,'jena')
			end = time.time()
			sFile.write('Jena Finished.\n')
			times[1] = str(round(end - start,3))
			if (results2.startswith("error")):
				sFile.write('Error JenaTDB')
				sFile.close()
				return 'error'
            
		if (tools[2]==True):
			if 'cold' in args:
				print 'Run virt in Cold'
				clearCache()
                        sFile.write('Running Query via Virtuoso..\n')
                        sFile.flush()
                        start = time.time()
                        results3 = ""#runQuery(query, args,filename,'virt')
                        end = time.time()
			print 'Virtuoso: '+results3
                        sFile.write('Virtuoso Finished.\n')
                        times[2] = str(round(end - start-100,3))
                        if (results3.startswith("error")):
                                sFile.write('Error Virtuoso')
                                sFile.close()
                                return 'error'
			
			#Thread(target=stopVirt, args=()).start()

		tTime = str(times[0])+','+str(times[1])+','+str(times[2])
		sFile.write('Times:'+tTime+'\n')
		sFile.close()
		return 'Finished'

def getRiqTime(filename,args):
	cache = 'warm'
	if 'none' in args:
		cache = 'none'
	elif 'cold' in args:
		cache = 'cold'

	opt = 'nopt'
	if '-O' in args:
		opt='opt'
	print 'RIQ Times..'
        DIR  = os.path.join(os.path.abspath(os.pardir))
        file_dir_extension = os.path.join(DIR+"/RIS/indexing/RIS.RUN/log/", '*'+filename+'*.'+opt+'.'+cache+'.all.json')
	t = '-1'        
	print 'Matching timing file: '+file_dir_extension
	rTime = fTime = 1 
        try:
		jfile= ''
                for name in glob.glob(file_dir_extension):
                        print name
			jfile = name

		jfile = open(jfile,'r')                        
		jdata = json.load(jfile)
		rTime = jdata['refine']['avg_refine_t']
		fTime = jdata['filter']['avg_filter_t']
		t = str(round(float(rTime)+float(fTime),3))
		jfile.close()
      	except Exception as E:
                print 'Riq Time Error:'
                print E	

	return [t,fTime]

def runQuery(query,args,filename,tool):

	createQueryFile(query,filename)
	DIR  = os.path.join(os.path.abspath(os.pardir))
	args = args.split()

	print 'Running Tool Query via '+tool
	if tool == 'riq':
		cmd = [ DIR+"/RIS/indexing/RIS/scripts/run_riq_query.py", "-C", "config-files/riq.conf","-q", "queries/"+filename, "-f" ,"xml"]
		if 'cold' in args:
			for a in args:
				cmd.append(a)
		elif '-O' in args:
			cmd.append('-O')
		print 'Command: '+str(cmd)
 		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 		p_stdout = p.stdout.read()
 		p_stderr = p.stderr.read()
		
 		#iprint(p_stdout)
 		if len(p_stderr)>0:
 			print(p_stderr)
		output = p_stdout.split('\n')
		e=0
		print('runQuery output:')
		for s in output:
			print s
			if s.startswith("error"):
				e = 1
			if e == 1: #what error?
				if 'pattern: ^candidate GRAPHID:' in s:
					return 'error:NoMatch'
		if e==1:
			return 'error'
		print 'RIQ Finished'
	elif tool == 'jena':
		#cmd = [ DIR+"/RIS/scripts/run_query_all.sh", "/mnt/data2/datasets/btc-2012-split-clean/btc-2012-split-clean.nq.tdb", "queries/"+filename,"tdb"]
		#for a in args:
                #        cmd.append(a)
		cmd = ['/home/vsfgd/Jena/apache-jena-2.11.1/bin/tdbquery','--loc','/mnt/data2/datasets/btc-2012-split-clean/btc-2012-split-clean.nq.tdb','--file', 'queries/'+filename,'--results','xml']
		print 'Issuing Jena CMND:'
		print cmd
 		p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 		p_stdout = p.stdout.read()
 		p_stderr = p.stderr.read()
                if len(p_stderr)>0:
                        print(p_stderr)
                        return 'error'
		xml =  p_stdout.split('<?xml version="1.0"?>')
		if (len(xml)>1):	
			p_stdout='<?xml version="1.0"?>'+xml[1]
		fout = open('output/jena/'+filename,'w')
 		fout.write(p_stdout)
		fout.close()
		print 'Jena Finished'
	
        elif tool == 'virt':
		"""
                print 'Reading query for virtuoso..'
                with open ("queries/"+filename, "r") as qFile:
                     query = qFile.read().replace('\n', ' ')
                qFile.close()

                myParameters = {'query': query, 'format': 'application/sparql-results+xml','timeout':'90000000','debug':'on'}
                print 'Issuing request..'

                myPort = "8890"
                myURL = "http://localhost:%s/sparql?%s" % (myPort, urllib.urlencode(myParameters))
                data = urllib.urlopen(myURL).read()
                print 'received response'
                """
       		t = Thread(target=start, args=()).start()

        	time.sleep(100)
        	data=runq(filename)
        	stop()
               	fout = open('output/virt/'+filename,'w')
                fout.write(data)
                fout.close()

		print 'Virtuoso Finished'
		
	return 'done'
def clearCache():
	call(["static/scripts/run_clear_cache.sh"])

def getXMLResultsFromTSV (filename,n):
	with open (filename, "r") as f:
        	line=f.readline()
                while 'WARN' in line: # skip warnings
                	line=f.readline()

		tsvVariable = line.strip().split('\t')

		xmlHeader = XMLHeader(tsvVariable)  # convert TSV header to XML header.
		xmlBody   = XMLBody(f,tsvVariable,n)
		xmlDoc = '<?xml version="1.0"?> <sparql xmlns="http://www.w3.org/2005/sparql-results#">'+ xmlHeader + xmlBody + '</sparql>'
                f.close()
		return xmlDoc

def XMLHeader(variables):
		xmlHeader = '<head>'
		for v in variables:
			xmlHeader += '<variable name="'+v+'"/>'
		xmlHeader += '</head>'
		return xmlHeader


def XMLBody(infile, variables, limit):
	xmlBody = '<results>'

	count = 0
	line = infile.readline()

	while line and count < limit:
		count += 1
		values = line.strip().split('\t')
		xmlBody += XMLBodyResult(variables,values)
		line = infile.readline()

	if (count == limit):
		values = ["Only showing first "+str(limit)] * len(variables)
		xmlBody += XMLBodyResult(variables,values)
	
	xmlBody += '</results>'


	return xmlBody

def XMLBodyResult (variables,values):
	if len(values) != len(variables):
			print ("XMLBodyResult: Severe Parsing Issue!")
	result = '<result>' 
	for v in range(len(values)):
		result += '<binding name="' + variables[v]+'"><val>'+  safe(values[v])  + '</val></binding>'

	result += '</result>'
	return result

def safe(the_str):
	if the_str.startswith("<") and the_str.endswith(">"):
		the_str = the_str[1:-1]
	elif '^^' in the_str:
		the_str = the_str.split('^^')[0]
	return the_str


def getXMLResults(filename,n):
 	with open (filename, "r") as f:
                                        line=f.readline()
                                        while 'WARN' in line:
                                               line=f.readline()
                                        #number of results
					i=0
                                        lines = line
                                        while line and i < n :
                                                line = f.readline()
                                                lines = lines + line
                                        	if '/result' in line:
							#if filename=='temp.q'
                                                	i = i + 1
                                        if i > n - 1:
	
                                                lines = lines + ' </results></sparql>'
                                                #lines = lines + ' <result><binding name="EOF"><literal xml:lang="en">Showing first 200 results </literal></binding></result></results></sparql>'
	f.close()

		#print lines
	return lines


def getQueryResults(filename,tool,cache):
	print 'Getting Results..'
	DIR  = os.path.join(os.path.abspath(os.pardir))
        rFile = ''
        if tool=='jena' or tool=='virt':
                file_dir_extension = os.path.join(DIR+"/RiQ/output/"+tool, filename)
	else:
        	file_dir_extension = os.path.join(DIR+"/RIS/indexing/RIS.RUN/log/", '*'+filename+'*.'+cache+'.*results')
        
	print 'locating results file: '+file_dir_extension

	try:
		for name in glob.glob(file_dir_extension):
			print 'Found file: '+name
			rFile = name

			return getXMLResults(rFile,200)
			#return getXMLResultsFromTSV(rFile,200)


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
        f.write(queryStr.replace("<div>","").replace("</div>","").strip())
        f.close()

def getVars (query):
        vrs=[]
        ast = fyzz.parse(query)
        if ast.selected == ['*']:
                varNDXs = [word for word in query.split(" ") if word.startswith('?')]
                for v in varNDXs:
                        if v.endswith('}') or v.endswith('{') or v .endswith('.'):
                                v = v[:-1]
                        if v not in vrs:
                                vrs.append(v)
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

def removePreviousRunFiles(caller):
	DIR  = os.path.join(os.path.abspath(os.pardir))

	if caller=='execute':
		filename='temp.q'
		#os.remove(DIR+'/RiQ/status/execute')

	log_dir_extension = os.path.join(DIR+"/RIS/indexing/RIS.RUN/log/", '*'+filename+'*')
	print 'removing files in: '+log_dir_extension
	try:
		for name in glob.glob(log_dir_extension):
			if os.path.isfile(name):
				os.remove(name)
			else:
				shutil.rmtree(name)
	except Exception, err:
		 print sys.exc_info()[0]
