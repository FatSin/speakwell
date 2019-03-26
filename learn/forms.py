from django import forms

class RegisterForm(forms.Form):

    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    lang_display = forms.CharField(max_length=50)
