from django import forms




class ZipcodeForm(forms.Form):
    zipcode = forms.IntegerField(
        label="5 digit US zipcode",
        max_value=99999,
        min_value=10000)

    forecast = forms.BooleanField(
        label="do you want 5 forecast days?",
        required=False   )

    def clean_zipcode(self):
        # this method is run after the data has been validated
        # zipcode needs to be a string
        data = self.cleaned_data["zipcode"]
        data = str(data)
        return data




# alternatively, base it off a string regex instead of an integer
class RegexZipcodeForm(forms.Form):
    zipcode = forms.RegexField(
        label="5 digit US zipcode",
        regex=r"^\d{5}$",
        strip=True)
