from datetime import date,timezone
from django.forms.utils import to_current_timezone
from django.shortcuts import render, redirect
from django.views import generic

from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import *
from .forms import *

from django.db.models import Sum

from datetime import datetime, timedelta

def get_today_hours(day=date.today()):
    total_today_hours = Log.objects.filter(date=day).aggregate(Sum('hours'))['hours__sum']
    if total_today_hours is None:
        total_today_hours = 0 
    return total_today_hours


def get_week_hours(day=date.today()):
    a_date = day
    days = timedelta(7)
    new_date = a_date - days

    total_today_hours = Log.objects.filter(date__gte=new_date, date__lte=a_date).aggregate(Sum('hours'))['hours__sum']
    if total_today_hours is None:
        total_today_hours = 0 
    return total_today_hours


def get_month_hours(day=date.today()):
    a_date = day
    days = timedelta(30)
    new_date = a_date - days

    total_today_hours = Log.objects.filter(date__gte=new_date, date__lte=a_date).aggregate(Sum('hours'))['hours__sum']
    if total_today_hours is None:
        total_today_hours = 0 
    return total_today_hours


class SignInPage(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'logger/signin.html', {'form':SignInForm})
    

    def post(self, request):
        data = SignInForm(request.POST)
        if data.is_valid():
            username = data.cleaned_data.get('username')
            password = data.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logs = Log.objects.filter(date=date.today())
                current_day = date.today()
                return render(request, 'logger/page.html', {
                    'username':request.user.username,
                    'form':TimeLogForm, 
                    'today':get_today_hours(current_day),
                    'week':get_week_hours(current_day),
                    'month':get_month_hours(current_day),
                    'select_day':LoadLogsForm,
                    'logs':logs
                })
        
        return render(request, 'logger/signin.html', {'form':SignInForm})


class Page(generic.View):
    def get(self, request, *args, **kwargs):
        logs = Log.objects.filter(date=date.today())
        current_day = date.today()
        return render(request, 'logger/page.html', {
            'username':request.user.username,
            'form':TimeLogForm, 
            'today':get_today_hours(current_day),
            'week':get_week_hours(current_day),
            'month':get_month_hours(current_day),
            'select_day':LoadLogsForm,
            'logs':logs
        })
        
    
    def post(self, request):
        data = TimeLogForm(request.POST)
        if data.is_valid():
            log = Log.objects.create(
                user = request.user,
                project = data.cleaned_data['project'],
                remarks = data.cleaned_data['remarks'],
                hours = data.cleaned_data['duration'],
                date = data.cleaned_data['date']
            )
        else:
            print("Data is not valid")


        date_data = LoadLogsForm(request.POST)
        current_day = date.today()
        logs = Log.objects.filter(date=date.today())
        if date_data.is_valid():
            current_day = date_data.cleaned_data['select_date']
            logs = Log.objects.filter(date=current_day)


        return render(request, 'logger/page.html', {
            'username':request.user.username,
            'form':TimeLogForm, 
            'today':get_today_hours(current_day),
            'week':get_week_hours(current_day),
            'month':get_month_hours(current_day),
            'select_day':LoadLogsForm,
            'logs':logs
        })
        