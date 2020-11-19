
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    department = forms.CharField(max_length=20)
    year = forms.CharField(max_length=10)
    otp = forms.CharField(min_length=6, max_length=6,required=False)
    
    class Meta:
        model = User
        fields = ["username", "email", "department", "year", "password1", "password2","otp"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["department"]
        user.email = self.cleaned_data["email"]
        user.last_name = self.cleaned_data["year"]
        if commit:
            user.save()
        return user





