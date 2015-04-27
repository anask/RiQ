from django.http import HttpResponse

def land(request):

	tool = "RIQ"
	if request.method == 'GET':
			# forward query to RIQ
			query =  request.GET['query']
			print 'RIQ RECEIVED:'
			print query
			results = runQuery(query,'warm 1',"tempLinked.q",'riq')
			return HttpResponse(content=results,content_type='xml; charset=utf-8')

	else:
			print ("RIQ GOT POST: ")
			print (request.POST)
			return HttpResponse(content="",content_type='xml; charset=utf-8')

