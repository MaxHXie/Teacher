from django import forms
from .models import Essay

class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['essay_text']

        widgets = {
            'essay_text': forms.Textarea(attrs={'class':'form-control transparent', 'placeholder':'Copy and paste your essay here...', 'rows':16}),
        }
