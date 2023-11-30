from django.urls import path
from .views import upload_leave_balance, upload_leave_availed, generate_pdf

urlpatterns = [
    path('upload_leave_balance/', upload_leave_balance, name='upload_leave_balance'),
    path('upload_leave_availed/', upload_leave_availed, name='upload_leave_availed'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
]