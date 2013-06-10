from django import forms
from tinymce.widgets import TinyMCE

class pageForm(forms.Form):
    short_desc = forms.CharField(
        min_length=2,
        max_length=30,
        initial=" Enter short description here",
        widget=forms.TextInput(attrs={'size':'30'}),
        )
    illustration = forms.ImageField()
    long_desc = forms.CharField(widget=TinyMCE(attrs={'cols': 100, 'rows': 15}),max_length=200, label="")
    
    def is_valid(self):
        valid = super(pageForm, self).is_valid()
        if not valid:
            return valid
        if self.cleaned_data['short_desc'] == self.fields['short_desc'].initial:
            self._errors['short_desc'] = 'No short description entered'
            return False
        return True
    
    
