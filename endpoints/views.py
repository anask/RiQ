from django.http import HttpResponse
from run.views import *

def land(request):

	tool = "RIQ"
	if request.method == 'GET':
			# forward query to RIQ
			query =  request.GET['query']
			print 'RIQ ENDPOINT RECEIVED:'
			print query
			try:
				result = runQuery(query,'-c warm',"tempLinked.q",'riq')
			except Exception, err:
				 print sys.exc_info()[0]
			if (result.startswith("error")):
                        	print 'Endpoint Error'
                	else:
                        	output = getQueryResults('tempLinked.q')

			return HttpResponse(content=output,content_type='xml; charset=utf-8')

	else:
			print ("RIQ GOT POST: ")
			print (request.POST)
			return HttpResponse(content="",content_type='xml; charset=utf-8')

