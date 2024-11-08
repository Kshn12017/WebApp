from django.db import models
import os

# Create your models here.
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
    approver = models.ForeignKey(Approver, on_delete=models.CASCADE)

    def __str__(self):
        return f"Level {self.level_number} - {self.approver}"

