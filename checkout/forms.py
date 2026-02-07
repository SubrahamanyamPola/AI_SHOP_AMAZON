
from django import forms
class AddressForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    address = forms.CharField()
    city = forms.CharField()
    country = forms.CharField()
