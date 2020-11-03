from django import forms
from .models import Essay
from allauth.account.forms import LoginForm, SignupForm, ResetPasswordForm

class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['essay_text']

        widgets = {
            'essay_text': forms.Textarea(attrs={'class':'form-control transparent', 'placeholder':'Copy and paste your essay here...', 'rows':16}),
        }

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': 'Email ... ', 'class': 'form-control'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Password ... ', 'class': 'form-control'})

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': 'Email ... ', 'class': 'form-control'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password ... ', 'class': 'form-control'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Password again ... ', 'class': 'form-control'})

class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(CustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(attrs={'type': 'email', 'placeholder': 'Email ... ', 'class': 'form-control'})
