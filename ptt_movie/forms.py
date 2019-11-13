from django import forms
from ptt_movie.models import Keyword,Keyword_Analysis

class AddForm(forms.Form):
	a = forms.IntegerField()
	b = forms.IntegerField()
	
class MoiveForm(forms.Form):
	movie_keyword_name = forms.CharField(label='電影關鍵字名稱')
	
	
class ItemForm(forms.ModelForm):
	name = forms.ModelChoiceField(Keyword.objects.all(), label='名稱', widget=forms.Select(attrs={'class':'form-control'}))
	comment = forms.CharField(label='評論', widget=forms.Textarea(attrs={'class': 'tinymceTextarea'}))
	article = forms.IntegerField(label='文章數', widget=forms.NumberInput(attrs={'class':'form-control'}))
	discussion = forms.IntegerField(label='討論數', widget=forms.NumberInput(attrs={'class':'form-control'}))
	good = forms.IntegerField(label='好評數', widget=forms.NumberInput(attrs={'class':'form-control'}))
	bad = forms.IntegerField(label='負評數', widget=forms.NumberInput(attrs={'class':'form-control'}))
	score = forms.IntegerField(label='評分', widget=forms.NumberInput(attrs={'class':'form-control'}))
	
	class Meta:
		model = Keyword_Analysis
		fields = ('name', 'article', 'discussion', 'good', 'bad', 'score' , 'comment',)