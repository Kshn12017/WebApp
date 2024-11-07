from django.urls import path
from . import views

urlpatterns = [
    path('', views.process_selection, name='process_selection'),
    path('load-process-codes/', views.load_process_codes, name='load_process_codes'),

]
