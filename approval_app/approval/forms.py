from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# write your logic below

User = get_user_model()

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


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        fields = ['username', 'password']
        

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match.")