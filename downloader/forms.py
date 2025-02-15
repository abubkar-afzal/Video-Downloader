from django import forms

class YouTubeForm(forms.Form):
    url = forms.URLField(label='YouTube URL', max_length=200)
    location = forms.CharField(label='Download Location', max_length=200, required=False, widget=forms.HiddenInput())

class InstagramForm(forms.Form):
    url = forms.URLField(label='Instagram Post URL', max_length=200)
    location = forms.CharField(label='Download Location', max_length=200, required=False, widget=forms.HiddenInput())
