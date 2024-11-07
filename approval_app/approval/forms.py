from django import forms
from .models import *

class ProcessSelectionForm(forms.Form):
    process = forms.ModelChoiceField(queryset=Process.objects.all(), label="Select Process")
    process_code = forms.ModelChoiceField(queryset=ProcessCode.objects.none(), label="Select Process Code")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'process' in self.data:
            try:
                process_id = int(self.data.get('process'))
                self.fields['process_code'].queryset = ProcessCode.objects.filter(process_id=process_id)
            except (ValueError, TypeError):
                pass

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
