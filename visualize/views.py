from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
import os
import subprocess
from subprocess import call
from PIL import Image
def land(request):
	return render_to_response('visualize.html', { 'TITLE': 'Visualize Query'})


def getQueryInfo(request):
	with open('queries/temp.info') as json_file:
		json_data = json.load(json_file)

	return HttpResponse(json.dumps(json_data), content_type="application/json")


def getQueryCandidates(request):
	q = open('output/candidatedataindecimal.txt')
	candidates = {}
	i=0
	for line in q:
		candidates[i]=line.rstrip()
		i=i+1
	q.close
	jobj = {}
	jobj['candidates']=candidates

	return HttpResponse(json.dumps(jobj), content_type="application/json")


def getQueryTree(request):
	DIR  = os.path.join(os.path.abspath(os.pardir))
	imgFlag = request.GET['exec']
	if(imgFlag=='yes'):
		cmd = [ "javac "+DIR+"/RIS/antlr/sparql/*.java"]
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p_stdout = p.stdout.read()
		p_stderr = p.stderr.read()
		print p_stderr


		cmd = [ "cd "+DIR+"/RIS/antlr/sparql ; pwd ; java org.antlr.v4.runtime.misc.TestRig Sparql query -ps "+DIR+"/RiQ/output/temp.ps "+DIR+"/RiQ/queries/temp.q"]
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p_stdout = p.stdout.read()
		p_stderr = p.stderr.read()
		print p_stdout
		print p_stderr

		cmd = [ "convert  -background white -alpha remove "+DIR+"/RiQ/output/temp.ps "+DIR+"/RiQ/output/temp.png"]
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p_stdout = p.stdout.read()
		p_stderr = p.stderr.read()
		print p_stdout
		print p_stderr


	try:
		with open(DIR+"/RiQ/output/temp.png", "rb") as f:
			return HttpResponse(f.read(), content_type="image/png")
	except IOError:
		img = Image.new('RGBA', (500, 300), (140,183,193,0))
		response = HttpResponse(content_type="image/jpeg")
		img.save(response, "JPEG")
		return response

def getOptimizedQueryTree(request):
	DIR  = os.path.join(os.path.abspath(os.pardir))
	imgFlag = 	request.GET['new']
	candidate = request.GET['cand']

	if(imgFlag=='yes'):
		binaryCandidate = str(bin(int(candidate.strip("Candidate"))))[2:]

		optDir = DIR+'/RIS/indexing/RIS.RUN/log/'
		optQuery = optDir+'dbpedia.g.q4.' + '0000001000000000'+'.rqmod'


		cmd = [ "cd "+DIR+"/RIS/antlr/sparql ; pwd ; java org.antlr.v4.runtime.misc.TestRig Sparql query -ps "+DIR+"/RiQ/output/tempOpt.ps "+optQuery]
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p_stdout = p.stdout.read()
		p_stderr = p.stderr.read()
		print p_stdout
		print p_stderr



		cmd = [ "convert  -background white -alpha remove "+DIR+"/RiQ/output/tempOpt.ps "+DIR+"/RiQ/output/tempOpt.png"]
		p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		p_stdout = p.stdout.read()
		p_stderr = p.stderr.read()
		print p_stdout
		print p_stderr


	try:
		with open(DIR+"/RiQ/output/tempOpt.png", "rb") as f:
			return HttpResponse(f.read(), content_type="image/png")
	except IOError:
		img = Image.new('RGBA', (500, 300), (140,183,193,0))
		response = HttpResponse(content_type="image/jpeg")
		img.save(response, "JPEG")
		return response
