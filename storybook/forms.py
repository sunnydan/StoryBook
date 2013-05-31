from django import forms
from tinymce.widgets import TinyMCE

class NodeForm(forms.Form):
    action = forms.CharField(min_length=2, max_length=30, label="What do you want to do next?")
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 15}),max_length=200, label="")
