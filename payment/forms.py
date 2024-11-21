from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_first_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}), required=True)
    shipping_last_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}), required=True)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Address'}), required=True)
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address1'}), required=True)
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address2'}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City'}), required=True)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State'}), required=True)
    shipping_pincode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Pincode'}), required=True)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}), required=True)
	
    class Meta:
        model = ShippingAddress
        fields = ['shipping_first_name','shipping_last_name','shipping_email','shipping_address1','shipping_address2','shipping_city','shipping_state','shipping_pincode','shipping_country']
        exclude = ['user',]


class PaymentForm(forms.Form):
    card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name on Card'}), required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Number'}), required=True)
    card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Expiry'}), required=True)
    card_cvv_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card CVV'}), required=True)
    card_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Address 1'}), required=True)
    card_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Address 2'}), required=True)
    card_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card city'}), required=True)
    card_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card State'}), required=True)
    card_pincode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Pincode'}), required=True)
    card_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Card Country'}), required=True)
	
    
    