from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.core.validators import EmailValidator
from .models import *
from .forms import *
import pandas as pd
from django.utils.safestring import mark_safe

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
            if not uploaded_file.file.path.lower().endswith(('.xls', '.xlsx')):
                raise ValidationError("Upload file must be an Excel file.")
            else:
                validate_excel_file(uploaded_file.file.path)
                msg = "File uploaded and validated successfully."
                messages.success(request, mark_safe(msg))
                return redirect('process_selection')
        except ValidationError as e:
            messages.error(request, mark_safe(e.message))
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
    process_codes = ProcessCode.objects.filter(process_id=process_id).values_list('id', 'code_name')
    return JsonResponse({'options': list(process_codes)})


def validate_excel_file(file_path):    
    # Attempt to read the file with pandas
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValidationError(f"Error reading Excel file: {str(e)}")

    # Check required columns
    required_columns = ['First Name', 'Last Name', 'Email', 'Roll Number']
    for column in required_columns:
        if column not in df.columns:
            raise ValidationError(f"The Excel file must contain the column {column}.")

    # Check at least one row of data
    if df.shape[0] < 1:
        raise ValidationError("The Excel file must contain at least one row of data.")

    # Check each row to ensure no required columns are empty
    for index, row in df.iterrows():
        missing_values = [col for col in required_columns if pd.isnull(row[col])]
        if missing_values:
            raise ValidationError(f"Row {index + 2} is missing values in columns: {', '.join(missing_values)}.")

    # Validate email addresses in the Email column
    from django.core.validators import EmailValidator
    email_validator = EmailValidator()
    for email in df['Email'].dropna():
        email_validator(email)
      
        
def manage_processes(request):
    if request.method == 'POST':
        process_form = ProcessForm(request.POST)
        code_form = ProcessCodeForm(request.POST)
        level_form = ApprovalLevelForm(request.POST)
        
        if process_form.is_valid():
            process_form.save()
            messages.success(request, "Process added successfully.")
            return redirect('manage_processes')
        
        if code_form.is_valid():
            code_name = code_form.cleaned_data['code_name']
            
            # Check if the ProcessCode with the same name already exists
            if ProcessCode.objects.filter(code_name=code_name).exists():
                messages.error(request, f"The Process Code '{code_name}' already exists.")
                return redirect('manage_processes')
            
            code_form.save()
            messages.success(request, "Process Code added successfully.")
            return redirect('manage_processes')
        
        if level_form.is_valid():
            level_number = level_form.cleaned_data['level_number']
            process_code = level_form.cleaned_data['process_code']
            
            # Ensure number is not negative
            if level_number <= 0:
                messages.error(request, "Approval Level must be a positive integer.")
                return redirect('manage_processes')
            
            # Ensure levels are created in order
            existing_levels = ApprovalLevel.objects.filter(process_code=process_code).order_by('level_number')
            
            # Check if the next level in sequence should be created
            if existing_levels.exists():
                next_expected_level = existing_levels.last().level_number + 1
            else:
                next_expected_level = 1
            
            if level_number != next_expected_level:
                messages.error(request, f"Please create {next_expected_level} level approval first.")
                return redirect('manage_processes')
            
            level_form.save()
            messages.success(request, "Approval Level added successfully.")
            return redirect('manage_processes')
    else:
        process_form = ProcessForm()
        code_form = ProcessCodeForm()
        level_form = ApprovalLevelForm()

    return render(request, 'manage_processes.html', {
        'process_form': process_form,
        'code_form': code_form,
        'level_form': level_form
    })
  
    
def add_approver(request):
    if request.method == 'POST':
        approver_form = ApproverForm(request.POST)
        if approver_form.is_valid():
            approver_form.save()
            messages.success(request, "Approver added successfully.")
            return redirect('add_approver')
    else:
        approver_form = ApproverForm()
    
    return render(request, 'add_approver.html', {'approver_form': approver_form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.first_name}!")
                return redirect('process_selection')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Error in form submission. Please try again.")
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            # Get the cleaned data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Create the user instance
            user = User(first_name=first_name, last_name=last_name, email=email)
            
            # Set the password using set_password to hash it
            user.set_password(password)
            
            # Optionally set other fields
            user.is_active = True  
            user.is_user = True  
            
            # Save the user instance to the database
            user.save()

            # Log the user in automatically after successful registration
            login(request, user)

            # Redirect to a success page (e.g., dashboard)
            messages.success(request, "Account created successfully!")
            messages.success(request, "You are now logged in.")
            return redirect('login')
        
        else:
            # If the form is invalid, render the form with errors
            messages.error(request, "There was an error with your form. Please check the errors below.")
    
    else:
        form = UserSignupForm()
    
    return render(request, 'signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')