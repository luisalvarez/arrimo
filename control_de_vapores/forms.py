from django import forms
from control_de_vapores.models import Movement, Parameter, EmployeeQuadrille


class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        exclude = ['parameter']


class ParameterForm(forms.ModelForm):
    class Meta:
        model = Parameter
        exclude = ['date_from', 'date_to', 'is_default']


class EmployeeQuadrilleForm(forms.ModelForm):
    class Meta:
        model = EmployeeQuadrille
        exclude = ['contribution', 'mutual_aid', 'fee', 'yola', 'fop', 'gross_salary', 'net_salary','harmful','past']