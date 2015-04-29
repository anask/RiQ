from django.http import HttpResponse
import sys
from run.views import runMultiToolQuery, getQueryResults
def land(request):
	print 'Received Request'
	if request.method == 'GET':
			# forward query to RIQ
                        query =  request.GET['query']
                        print 'RIQ ENDPOINT RECEIVED:'
                        print query
                        
                        try:
                                if 'tools' in request.GET:
                                        tools=[]
                                        toolstr = str(request.GET['tools'])

                                        if(toolstr[0]=='1'):
                                                tools.append(True)
                                        else:
                                                tools.append(False)
                                        if(toolstr[1]=='1'):
                                                tools.append(True)
                                        else:
                                                tools.append(False)
                                        if(toolstr[2]=='1'):
                                                tools.append(True)
                                        else:
                                                tools.append(False)
                                else:
                                
                                        tools=[True,False,False]
                                
                                print 'Issuing Multi-tool Query..'
				result ='error'
                                result = runMultiToolQuery("tempLinked.q",query,'-c warm',tools)
                                print 'Query Finished!'
                        except Exception, err:
                                 print sys.exc_info()[0]

                        if (result.startswith("error")):
                                output = 'Endpoint Error'
				print output
                        else:
				if tools[1]==True:
                                	output = getQueryResults('tempLinked.q','jena')			
                                else:
					output = getQueryResults('tempLinked.q','riq')			
				
			return HttpResponse(content=output,content_type='xml; charset=utf-8')

	else:
			print ("RIQ GOT POST: ")
			print (request.POST)
			return HttpResponse(content="",content_type='xml; charset=utf-8')

