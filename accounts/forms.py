from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Edit_Profile_Form(forms.Form):
    username = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username