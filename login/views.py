from django.shortcuts import render
from .models import AuthUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from .models import Report


# Create your views here.

def loginView(request):
    return render(request, "login.html")


@login_required(login_url='loginView')
def home(request):
    return render(request, "home.html")


@login_required(login_url='loginView')
def editUserInfo(request):
    return render(request, "editUserInfo.html")


@login_required(login_url='loginView')
def addReport(request):
    return render(request, "addReport.html")


@login_required(login_url='loginView')
def addReportInformation(request):
    checkTitle = Report.objects.filter(report_title=request.POST.get('report_title'))
    if not checkTitle:
        report = Report(
            report_title=request.POST.get('report_title'),
            date=request.POST.get('report_date'),
            report_discription=request.POST.get('report_discription'),
            user_id=request.POST.get('user_id'),
        )
        report.save()
        messages.add_message(request, messages.INFO, 'Report Saved Successfully')
        return redirect('addReport')
    else:
        messages.add_message(request, messages.INFO, 'Report Title Already Exists')
        return redirect('addReport')


@login_required(login_url='loginView')
def viewAllReport(request):
    userId = 13
    viewAllReport = Report.objects.filter(user_id= userId)
    return render(request, 'viewAllReport.html', {'viewAllReport': viewAllReport})


def loginCheck(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, 'Wrong User Name Or Password')
            return redirect('loginView')
    messages.add_message(request, messages.INFO, 'You Have To Login First')
    return redirect('loginView')


def registration(request):
    checkData = AuthUser.objects.filter(email=request.POST.get('email'))
    if not checkData:
        User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=(request.POST.get('password')),
        )
        messages.add_message(request, messages.INFO, 'User Saved Successfully')
        return redirect('loginView')
    else:
        messages.add_message(request, messages.INFO, 'Email Already Exists')
        return redirect('loginView')


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Successfully logout')
    return redirect('loginView')
