from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Account)

admin.site.register(Process)
admin.site.register(ProcessCode)
admin.site.register(UploadedFile)
admin.site.register(ApprovalLevel)
admin.site.register(Approver)