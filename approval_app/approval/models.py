from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import os

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,email,password=None):
        
        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_user = True
        user.is_active=True
        user.save(using=self._db)
        return user
    
    def create_project_director(self,first_name,last_name,email,password=None):

        user=self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_project_director = True
        user.is_active=True
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,email,password=None):

        user=self.model(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
        
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superadmin(self,first_name,last_name,email,password=None):

        user=self.model(
            email=self.normalize_email(email),
           
            password=password,
            first_name=first_name,
            last_name=last_name,
        
        )
        # user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.set_password(password)
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    
    push_token=models.CharField(max_length=100,null=True,blank=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    
    is_admin=models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)
    is_masteradmin=models.BooleanField(default=False)
    is_project_director=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    

    objects=MyAccountManager()

    def has_perm(self, perm, obj=None):
        if self.is_superadmin  or self.is_admin:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_superadmin or self.is_admin:
            return True
        return False
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Process(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProcessCode(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="codes")
    code_name = models.CharField(max_length=100)

    def __str__(self):
        return self.code_name

class UploadedFile(models.Model):
    process_code = models.ForeignKey(ProcessCode, on_delete=models.CASCADE, related_name="uploads")
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} for {self.process_code.code_name}"
    
    #Delete from system before deleting from database.
    def delete(self, *args, **kwargs):
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

class Approver(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ApprovalLevel(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE,)
    process_code = models.ForeignKey(ProcessCode, on_delete=models.CASCADE)
    level_number = models.IntegerField()
    approver = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Pending", choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")])

    def __str__(self):
        return f"{self.process_code} - Level {self.level_number} "

