from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from index.models import indexdata,graphdata,queryfilenametable
from index.forms import IndexConstructionForm
from django.template import RequestContext



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

			print index
			indexdataobject.save()
			config = ConfigParser.RawConfigParser()
			config.optionxform=str
			config.read('textfile.txt')
			config.set('LSH','LSHK',form.cleaned_data['lhskparameter'])
			config.set('LSH','LSHL',form.cleaned_data['lhslparameter'])
			config.set('Limits', 'MAXCCSIZE',form.cleaned_data['maximumgraphs'])
#			config.set('Section=GRAPHS', 'GRAPHS2INDEX',form.cleaned_data['graphindex'])
			config.set('Dablooms', 'CAPACITY',form.cleaned_data['bloomcapacity'])
			config.set('Dablooms', 'ERROR_RATE',form.cleaned_data['bloomerror'])

			f = open('riqtemp.conf.py','w')

			config.write(f)
			f.close()

#			print 'locale encoding: ' + locale.getpreferredencoding()
			# read the riqtemp.conf
			# create riq.conf
			q = open('riqtemp.conf.py')
			r = open('riq.conf', 'w')
			for line in q:
				if line.find(' = ') != -1:
					r.write(line.replace(' = ', '='))
				else:
					r.write(line)
			q.close()
			r.close()

			# remove riqtemp.conf
			remove('riqtemp.conf.py')

			return render_to_response('IndexConstruction.html', {'form': form, 'NavMenu' : 'IndexConstruction','IndexName' : indexName}, context_instance=RequestContext(request))
		else:
			print 'form is invalid'
			print form.errors
			return render_to_response('IndexConstruction.html', {'form': form,'NavMenu' : 'IndexConstruction'}, context_instance=RequestContext(request))
	else:
		form = IndexConstructionForm()
		context = {'form': form,'TITLE' : 'Index Construction'}
		return render_to_response('index.html', context, context_instance=RequestContext(request))
