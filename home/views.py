from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime
from dateutil import tz

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def home(request):
	from_zone = tz.tzutc()
	to_zone = tz.gettz('America/Chicago')

	utc = datetime.utcnow()
	utc = utc.replace(tzinfo=from_zone)
	central = utc.astimezone(to_zone)
	
	cIp = get_client_ip(request)
	f = open('alog.txt','a')
	f.write(str(central)+" "+str(cIp)+'\n')
	f.close()

	return render_to_response('home.html', { 'TITLE': 'RIQ'})


