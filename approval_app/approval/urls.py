from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_selection, name='process_selection'),
    path('load-process-codes/', views.load_process_codes, name='load_process_codes'),
    path('manage-processes/', views.manage_processes, name='manage_processes'),
    path('add-approver/', views.add_approver, name='add_approver'),

]
