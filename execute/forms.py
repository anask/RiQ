from django import forms


class ExecuteForm(forms.Form):

	BTC = 'BTC'
	LOGD = 'LOGD'
	D10 = 'D10'
	LUBM = 'LUBM'

	MY_CHOICESDATASET = (
		(BTC, 'BTC (prebuilt)'),
 		(LUBM, 'LUBM (prebuilt)'),
# 		(LOGD, 'LOGD'),
# 		(D10,'D10-SML'),


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
		(OPTENABLED ,'Enable'),
		(OPTDISABLED ,'Disable'),

	)

	QBTC1 = 'BTC1'
	QBTC2 = 'BTC2'
	QBTC3 = 'BTC3'
	QBTC4 = 'BTC4'
	QBTC5 = 'BTC5'
	QBTC6 = 'BTC6'
	QBTC7 = 'BTC7'
	QBTC8 = 'BTC8'
	QBTC9 = 'BTC9'
	QBTC10 = 'BTC10'
	QBTC11 = 'BTC11'

	QLUBM1 = 'LUBM1'
	QLUBM2 = 'LUBM2'
	QLUBM3 = 'LUBM3'
	QLUBM4 = 'LUBM4'
	QLUBM5 = 'LUBM5'
	QLUBM6 = 'LUBM6'
	QLUBM7 = 'LUBM7'
	QLUBM8 = 'LUBM8'
	QLUBM9 = 'LUBM9'
	QLUBM10 = 'LUBM10'
	QLUBM11 = 'LUBM11'
	CUS = 'CUSTOM'

	MY_CHOICESQUERY=(
#		( QBTC1,'B1'),
#		( QBTC2,'B2'),
#		( QBTC3,'B3'),
		( QBTC4,'B4'),
		( QBTC5,'B5'),
		( QBTC6,'B6'),
		( QBTC7,'B7'),
		( QBTC8,'B8'),
		( QBTC9,'B9'),
		( QBTC10,'B10'),
		( QBTC11,'B11'),

		( QLUBM1,'L1'),
		( QLUBM2,'L2'),
		( QLUBM3,'L3'),
		( QLUBM4,'L4'),
		( QLUBM5,'L5'),
		( QLUBM6,'L6'),
		( QLUBM7,'L7'),
		( QLUBM8,'L8'),
		( QLUBM9,'L9'),
		( QLUBM10,'L10'),
		( QLUBM11,'L11'),

		( CUS,'CUSTOM'),
	

	)

	dataset = forms.ChoiceField(choices=MY_CHOICESDATASET, widget = forms.Select)
	cache = forms.ChoiceField(choices=MY_CHOICESCACHE, widget = forms.RadioSelect())

	optimize = forms.ChoiceField(choices=MY_CHOICESOPTIMIZATION, widget = forms.RadioSelect())

	query = forms.ChoiceField(choices=MY_CHOICESQUERY, widget = forms.RadioSelect())
