from django import forms
from .models import Essay

class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['email', 'essay_text']

        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control transparent', 'placeholder':'Your email here'}),
            'essay_text': forms.Textarea(attrs={'class':'form-control transparent', 'placeholder':'Copy paste your essay here', 'rows':14}),
        }
