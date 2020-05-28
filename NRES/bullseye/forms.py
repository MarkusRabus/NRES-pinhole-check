from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.utils.timezone import now


class DateForm(forms.Form):
    # name = forms.CharField(label="Name")

    date = forms.DateField(label="Date", widget=DatePickerInput(                 
    	options={
		"format": "MM/DD/YYYY", # moment date-time format
        "showClose": True,
		"showClear": False,
		"showTodayButton": True,
		} ) 
    	)

SITE_CHOICES=[	('TLV','TLV'),
				('CPT','CPT'),
				('ELP','ELP'),
				('LSC','LSC'),]

class SiteForm(forms.Form):
	site = forms.ChoiceField(choices=SITE_CHOICES, widget=forms.RadioSelect)