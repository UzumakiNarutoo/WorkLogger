from django.forms.fields import DateField, DurationField
from django.forms.widgets import PasswordInput
from logger.models import User
from django import forms
from .models import User, Project
from datetime import date

class SignInForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=250, widget=PasswordInput)


class TimeLogForm(forms.Form):
    duration = forms.DecimalField(max_digits=10, decimal_places=2)
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    remarks = forms.CharField(widget=forms.Textarea)
    date = forms.DateTimeField(widget=forms.SelectDateWidget)


class LoadLogsForm(forms.Form):
    select_date = forms.DateTimeField(widget=forms.SelectDateWidget(), initial=date.today())
