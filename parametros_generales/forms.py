from django import forms
from parametros_generales.models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        widgets = {
            'nationality': forms.RadioSelect
        }
        exclude = []


class AssignSubstituteForm(forms.Form):
    employees = forms.ModelChoiceField(queryset=Employee.objects.filter(type='S'))
    employee = forms.IntegerField(widget=forms.HiddenInput())