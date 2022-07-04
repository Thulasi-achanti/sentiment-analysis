from django import forms
class TwitterForm(forms.Form):
   word=forms.CharField(max_length=30)