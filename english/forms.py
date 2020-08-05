from django.forms import ModelForm
from .models import Essay

class EssayForm(ModelForm):
    class Meta:
        model = Essay
        fields = ['email', 'essay_text']
