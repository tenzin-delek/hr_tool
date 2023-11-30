from django import forms

class LeaveBalanceForm(forms.Form):
    leave_balance_file = forms.FileField()

class LeaveAvailedForm(forms.Form):
    leave_availed_file = forms.FileField()

# from django import forms
# from .models import LeaveBalance, LeaveAvailed

# class LeaveBalanceForm(forms.ModelForm):
#     class Meta:
#         model = LeaveBalance
#         fields = '__all__'  # Use '__all__' to include all fields from the model, or specify the fields you want.

# class LeaveAvailedForm(forms.ModelForm):
#     class Meta:
#         model = LeaveAvailed
#         fields = '__all__'  # Adjust this based on the actual fields in your LeaveAvailed model.
