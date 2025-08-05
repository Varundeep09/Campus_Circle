from django import forms

class NewThreadForm(forms.Form):
    recipients = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter usernames separated by commas'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), max_length=1000)