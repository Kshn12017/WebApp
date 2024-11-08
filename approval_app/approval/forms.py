from django import forms
from .models import *

class ProcessSelectionForm(forms.Form):
    process = forms.ModelChoiceField(queryset=Process.objects.all(), 
                                     label="Choose a Process",
                                     empty_label="Choose a Process")
    process_code = forms.ModelChoiceField(queryset=ProcessCode.objects.none(), 
                                          label="Choose a Process Code",
                                          empty_label="Choose a Process Code")


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['name']
        labels = {'name': 'Process Name'}


class ProcessCodeForm(forms.ModelForm):
    class Meta:
        model = ProcessCode
        fields = ['process', 'code_name']
        widgets = {
            'process': forms.Select(attrs={
                'id': 'id_process_code_form',
                }),
            'code_name': forms.TextInput(attrs={'id': 'id_code_name'}),
        }


class ApprovalLevelForm(forms.ModelForm):
    class Meta:
        model = ApprovalLevel
        fields = ['process', 'process_code', 'level_number', 'approver']
        widgets = {
            'process': forms.Select(attrs={
                'id': 'id_process_approval_form',
                }),
            'process_code': forms.Select(attrs={'id': 'id_process_code'}),
        }

