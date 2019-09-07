from django import forms

class AddForm(forms.Form):
	a = forms.IntegerField()
	b = forms.IntegerField()
	
class MoiveForm(forms.Form):
	movie_name = forms.CharField()
	
class MoiveTypeForm(forms.Form):
	type = forms.IntegerField()
	movie_name = forms.CharField()