from django import forms

class PostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Leave a Post!"
        }
        ), required=False
    )
    image = forms.ImageField()

class LikeForm_Profile(forms.Form):
    post_id = forms.CharField()

class EditPost(forms.Form):
    body = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Edit The Post!"
        })
    )
    image = forms.ImageField(required=False)

