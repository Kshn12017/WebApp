from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.validators import EmailValidator
from .models import *
from .forms import *
import pandas as pd

def process_selection(request):
    process_form = ProcessSelectionForm(request.POST or None)
    file_form = FileUploadForm(request.POST or None, request.FILES)
    
    if request.method == "POST" and process_form.is_valid() and file_form.is_valid():
        selected_process_code = process_form.cleaned_data['process_code']
        uploaded_file = file_form.save(commit=False)
        uploaded_file.process_code = selected_process_code
        uploaded_file.save()

        # Validate Excel File
        try:
            validate_excel_file(uploaded_file.file.path)
            messages.success(request, "File uploaded and validated successfully.")
            # Redirect to next step in the approval pipeline
            return redirect('process_selection')
        except ValidationError as e:
            messages.error(request, f"Validation error: {e}")
            uploaded_file.delete()
            
    else:
        process_form = ProcessSelectionForm()
        file_form = FileUploadForm()
        
    return render(request, "process_selection.html", {
        "process_form": process_form,
        "file_form": file_form
    })


def load_process_codes(request):
    process_id = request.GET.get('process_id')
    process_codes = ProcessCode.objects.filter(process_id=process_id)
    return JsonResponse(render_to_string('process_code_options.html', {'process_codes': process_codes}), safe=False)



def validate_excel_file(file_path):
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Check required columns
    required_columns = ['First Name', 'Last Name', 'Email', 'Roll Number']
    if not all(column in df.columns for column in required_columns):
        raise ValidationError("The Excel file must contain columns: First Name, Last Name, Email, Roll Number.")
    
    # Check at least one row of data
    if df.shape[0] < 1:
        raise ValidationError("The Excel file must contain at least one row of data.")
    
    # Validate email addresses
    email_validator = EmailValidator()
    for email in df['Email']:
        email_validator(email)
