from django import forms
from tinymce.widgets import TinyMCE

class NodeForm(forms.Form):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}),max_length=200)
