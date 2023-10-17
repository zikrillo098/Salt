from django import forms


class EmailShareForms(forms.Form):
    name = forms.CharField(max_length=160)
    email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    to = forms.EmailField()
