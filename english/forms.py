from django import forms
from .models import Essay

class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['email', 'essay_text']

        widgets = {
            'email': forms.EmailInput(attrs={'class':'form-control transparent', 'placeholder':'Email here, so we know where to send your essay'}),
            'essay_text': forms.Textarea(attrs={'class':'form-control transparent', 'placeholder':'Copy and paste your essay here...', 'rows':12}),
        }
