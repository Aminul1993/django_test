from django import forms

class TODO(forms.Form):
    gid = forms.CharField(max_length=200, required=False)
    completed = forms.BooleanField(required=False)
    name = forms.CharField(max_length=100)
    notes = forms.CharField(max_length=200, required=False)