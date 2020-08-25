from django import forms
from .models import *

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            'fname',
            'lname',
            'address',
            'city',
            'state',
            'zipcode',
            'phone',
            'instructions'
        ]
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'fname',
            'lname',
        ]
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control'}),
            'lname': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = [
            'description',
            'item',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'item': forms.HiddenInput(attrs={'id': 'orderitem-id'})
        }
    