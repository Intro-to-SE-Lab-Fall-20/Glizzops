from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ComposeForm(forms.Form):
    email_address = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=TinyMCE(mce_attrs={'width': 800}))

    class Media:
        js = ('/site_media/static/tiny_mce/tinymce.min.js',)