from django import forms


class ExecuteForm(forms.Form):

	BTC = 'BTC'
	LOGD = 'LOGD'
	D10 = 'D10'


	MY_CHOICESDATASET = (
		(BTC, 'BTC'),
		(LOGD, 'LOGD'),
		(D10,'D10-SML'),


	)

	COLDC = 'cold'
	WARMC = 'warm'

	MY_CHOICESCACHE = (
		(COLDC, 'Cold'),
		(WARMC , 'Warm'),
	)

	OPTENABLED  = 'opt'
	OPTDISABLED = 'nopt'


	MY_CHOICESOPTIMIZATION = (
		(OPTENABLED ,'Enabled'),
		(OPTDISABLED ,'Disabled'),

	)

	QBTC1 = 'BTC1'
	QBTC2 = 'BTC2'
	DBPDSB1 = 'DBPD1'
	DBPDSB2 = 'DBPD2'
	DBPDSB9 = 'DBPD9'
	CUS = 'CUSTOM'

	MY_CHOICESQUERY=(
		( QBTC1 ,'BTC - 1'),
		( QBTC2,'BTC - 2'),
		( DBPDSB1,'DBPD SB - 1'),
		( DBPDSB2,'DBPD SB - 2'),
		( DBPDSB2,'DBPD SB - 9'),
		( CUS,'CUSTOM'),
	)

	dataset = forms.ChoiceField(choices=MY_CHOICESDATASET, widget = forms.Select)
	cache = forms.ChoiceField(choices=MY_CHOICESCACHE, widget = forms.RadioSelect())

	optimize = forms.ChoiceField(choices=MY_CHOICESOPTIMIZATION, widget = forms.RadioSelect())

	query = forms.ChoiceField(choices=MY_CHOICESQUERY, widget = forms.RadioSelect())
