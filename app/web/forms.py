from django import forms




class ZipcodeForm(forms.Form):
    zipcode = forms.IntegerField(
        label="5 digit US zipcode",
        max_value=99999,
        min_value=1)