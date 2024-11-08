from django import forms
from .models import *

class ProcessSelectionForm(forms.Form):
    process = forms.ModelChoiceField(
        queryset=Process.objects.all(),
        empty_label="Choose a Process",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    process_code = forms.ModelChoiceField(
        queryset=ProcessCode.objects.none(),
        empty_label="Choose a Process Code",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ['name']
        labels = {'name': 'Process Name'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Process Name'}),
        }


class ProcessCodeForm(forms.ModelForm):
    class Meta:
        model = ProcessCode
        fields = ['process', 'code_name']
        widgets = {
            'process': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_process_code_form',
                }),
            'code_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_code_name',
                'placeholder': 'Enter Code Name',
                }),
        }

class ApproverForm(forms.ModelForm):
    class Meta:
        model = Approver
        fields = ['name']
        widgets = {
           'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'id_code_name',
                'placeholder': 'Enter Approver Name',
                }),
        }
        labels = {'name': 'Approver Name'}

class ApprovalLevelForm(forms.ModelForm):
    class Meta:
        model = ApprovalLevel
        fields = ['process', 'process_code', 'level_number', 'approver']
        widgets = {
            'process': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_process_approval_form',
                'placeholder': 'Select a process'
            }),
            'process_code': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_process_code',
                'placeholder': 'Select a process code'
            }),
            'level_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Approval Level Number'
            }),
            'approver': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Approver'
            }),
        }
        labels = {
            'process': 'Process',
            'process_code': 'Process Code',
            'level_number': 'Approval Level',
            'approver': 'Approver',
        }

