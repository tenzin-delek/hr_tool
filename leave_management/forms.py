from django import forms

class LeaveBalanceForm(forms.Form):
    leave_balance_file = forms.FileField()

class LeaveAvailedForm(forms.Form):
    leave_availed_file = forms.FileField()

