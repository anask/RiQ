from django import forms
from django.forms import ModelForm
from indexinfo.models import indexdata
import datetime


class IndexConstructionForm(ModelForm):

	BTC = 'BTC'
	LOGD = 'LOGD'


	MY_CHOICESDATASET = (
		(BTC, 'BTC'),
		(LOGD, 'LOGD'),


	)

	LHSKFIRST = 4
	LHSKSECOND = 8
	LHSKTHIRD = 16
	LHSKFOURTH = 30

	MY_CHOICESLHSK = (
		(LHSKFIRST, 4),
		(LHSKSECOND , 8),
		(LHSKTHIRD, 16),
		(LHSKFOURTH , 30),

	)

	LHSLFIRST = 4
	LHSLSECOND = 6
	LHSLTHIRD = 10
	LHSLFOURTH = 11

	MY_CHOICESLHSL = (
		(LHSLFIRST, 4),
		(LHSLSECOND , 6),
		(LHSLTHIRD, 10),
		(LHSLFOURTH , 11),

	)
	BLOOMCAPACITYFIRST = '2.5M'
	BLOOMCAPACITYSECOND = '5M'
	BLOOMCAPACITYTHIRD = '10M'


	MY_CHOICESBLOOMCAPACITY = (
		(BLOOMCAPACITYFIRST, '2.5M'),
		(BLOOMCAPACITYSECOND , '5M'),
		(BLOOMCAPACITYTHIRD, '10M'),
	)

	BLOOMERRORFIRST = 1
	BLOOMERRORSECOND = 5
	BLOOMERRORTHIRD = 10


	MY_CHOICESBLOOMERROR = (
		(BLOOMERRORFIRST, 1),
		(BLOOMERRORSECOND , 5),
		(BLOOMERRORTHIRD, 10),


	)

	dataset = forms.ChoiceField(choices=MY_CHOICESDATASET, widget = forms.Select)
	lhskparameter = forms.ChoiceField(choices=MY_CHOICESLHSK, widget = forms.Select)
	lhslparameter = forms.ChoiceField(choices=MY_CHOICESLHSL, widget = forms.Select)
	maximumgraphs = forms.CharField(label=(u'Maximum graphs'))
	bloomcapacity = forms.ChoiceField(choices=MY_CHOICESBLOOMCAPACITY, widget = forms.Select)
	bloomerror = forms.ChoiceField(choices=MY_CHOICESBLOOMERROR, widget = forms.Select)
	graphindex = forms.CharField(label=(u'Number of graphs to index'))


	class Meta:
			model = indexdata
			exclude = ('Dataset','LHSKParameter','LHSLParameter','MaximumGraphs','BloomError', 'BloomCapacity', 'IndexName','CreateDate', 'TotalGraphs', 'GraphIndex')


