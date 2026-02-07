
from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(required=False)
    cat = forms.CharField(required=False)

class ReviewForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
