from django import forms
from .models import *
import math
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
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            
        }
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        if fname.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("First name must only consist of alphabetic characters.")
        return fname.strip()
    
    def clean_lname(self):
        lname = self.cleaned_data.get('lname')
        if lname.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("Last name must only consist of alphabetic characters.")
        return lname.strip()
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("City must only consist of alphabetic characters.")
        return city.strip()

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("State/Country must only consist of alphabetic characters.")
        return state.strip()
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        if zipcode.isnumeric() == False:
            raise forms.ValidationError("Zipcode must only consist of numbers.")
        return zipcode.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11 or not phone.isdecimal():
            raise forms.ValidationError("Phone number must be 11 numbers (09234567890).")
        elif phone[0] != '0' or phone[1] != '9':
            raise forms.ValidationError("Phone number must start with 0 and 9 (09234567890).")
        return phone

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
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        if fname.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("First name must only consist of alphabetic characters.")
        return fname.strip()
    
    def clean_lname(self):
        lname = self.cleaned_data.get('lname')
        if lname.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("Last name must only consist of alphabetic characters.")
        return lname.strip()

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

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
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
            'fname': forms.TextInput(attrs={'class': 'form-control col-lg-5 col-sm-4'}),
            'lname': forms.TextInput(attrs={'class': 'form-control col-lg-5 col-sm-4'}),
            'address': forms.TextInput(attrs={'class': 'form-control col-lg-5 col-sm-4'}),
            'city': forms.TextInput(attrs={'class': 'form-control col-lg-5 col-sm-4'}),
            'state': forms.TextInput(attrs={'class': 'form-control col-lg-5 col-sm-4'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control col-lg-5 col-sm-4'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
        }
    def clean_fname(self):
        fname = self.cleaned_data.get('fname')
        if fname.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("First name must only consist of alphabetic characters.")
        return fname.strip()
    
    def clean_lname(self):
        lname = self.cleaned_data.get('lname')
        if lname.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("Last name must only consist of alphabetic characters.")
        return lname.strip()
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("City must only consist of alphabetic characters.")
        return city.strip()

    def clean_state(self):
        state = self.cleaned_data.get('state')
        if state.replace(' ', '').isalpha() == False:
            raise forms.ValidationError("State/Country must only consist of alphabetic characters.")
        return state.strip()
    
    def clean_zipcode(self):
        zipcode = self.cleaned_data.get('zipcode')
        if zipcode.isnumeric() == False:
            raise forms.ValidationError("Zipcode must only consist of numbers.")
        return zipcode.strip()

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11 and phone.isdecimal():
            raise forms.ValidationError("Phone number must be 11 numbers (09234567890).")
        elif phone[0] != '0' and phone[1] != '9':
            raise forms.ValidationError("Phone number must start with 0 (09234567890).")
        return phone