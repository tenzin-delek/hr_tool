from django.shortcuts import render, redirect
from .forms import LeaveBalanceForm, LeaveAvailedForm
from .models import LeaveBalance, LeaveAvailed
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import pandas as pd
import numpy as np

def upload_leave_balance(request):
    if request.method == 'POST':
        form = LeaveBalanceForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file and save data to the database
            handle_uploaded_file(request.FILES['leave_balance_file'], 'leave_balance')
            return redirect('home')
    else:
        form = LeaveBalanceForm()

    return render(request, 'upload_leave_balance.html', {'form': form})

def upload_leave_availed(request):
    if request.method == 'POST':
        form = LeaveAvailedForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the uploaded file and save data to the database
            handle_uploaded_file(request.FILES['leave_availed_file'], 'leave_availed')
            return redirect('home')
    else:
        form = LeaveAvailedForm()

    return render(request, 'upload_leave_availed.html', {'form': form})

def handle_uploaded_file(file, sheet_type):
    if sheet_type == 'leave_balance':
        df = pd.read_excel(file, sheet_name=0, header=2)
        # Handle Leave Balance data
        # Extract necessary columns and save to the database
        leave_balance_data = df[['Emp ID', 'Name', 'Region', 'COFF', 'EL', 'LWP', 'RH', 'SL', 'WFH']]
        leave_balance_data = leave_balance_data.drop(columns=['Name'])  # Ignore the 'Name' column
        leave_balance_data.columns = ['emp_id', 'region', 'coff', 'el', 'lwp', 'rh', 'sl', 'wfh']  # Rename columns to match model

        # Handle NaN values by replacing them with 0
        leave_balance_data = leave_balance_data.replace({np.nan: 0})

        # Ensure all numeric columns have valid numeric values
        numeric_columns = ['coff', 'el', 'lwp', 'rh', 'sl', 'wfh']
        for col in numeric_columns:
            leave_balance_data[col] = pd.to_numeric(leave_balance_data[col], errors='coerce').fillna(0)

        LeaveBalance.objects.bulk_create([LeaveBalance(**row) for row in leave_balance_data.to_dict('records')])

    elif sheet_type == 'leave_availed':
        df = pd.read_excel(file, sheet_name=0, header=1)
        print(df.columns)
        # Handle Leave Availed data
        # Extract necessary columns and save to the database
        leave_availed_data = df[['Emp ID', 'Name', 'Leave Type', 'Action', 'Date', 'Debit']]
        leave_availed_data.columns = ['emp_id', 'name', 'leave_type', 'action', 'date', 'debit']  # Rename columns to match model

        # Handle NaN values by replacing them with 0
        leave_availed_data = leave_availed_data.replace({np.nan: 0})

        # Ensure 'debit' column has valid numeric values
        leave_availed_data['debit'] = pd.to_numeric(leave_availed_data['debit'], errors='coerce').fillna(0)

        # Ensure 'date' column is in DateTime format
        leave_availed_data['date'] = pd.to_datetime(leave_availed_data['date'], errors='coerce')

        LeaveAvailed.objects.bulk_create([LeaveAvailed(**row) for row in leave_availed_data.to_dict('records')])

def generate_pdf(request):
    # Fetch data from the database
    leave_balance_data = LeaveBalance.objects.all()
    leave_availed_data = LeaveAvailed.objects.all()

    template_path = 'pdf_template.html'
    context = {'leave_balance_data': leave_balance_data, 'leave_availed_data': leave_availed_data}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="leave_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response
