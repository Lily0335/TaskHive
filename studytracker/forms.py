from django import forms
from .models import StudySession

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['date', 'hours', 'note']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'input-field'}),
            'hours': forms.NumberInput(attrs={'step': '0.5', 'class': 'input-field'}),
            'note': forms.TextInput(attrs={'class': 'input-field'})
        }
