from django import forms

class TrendForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=100)
