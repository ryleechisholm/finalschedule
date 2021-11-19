from django.shortcuts import render, redirect
from app.decorators import unauthenticated_user
from .forms import CreateUserForm, MessageForm, UpdateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users
from .models import *
import random
from typing import List
from dataclasses import dataclass


@unauthenticated_user
def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect.')
        context = {}
        return render(request, 'login.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('login_page')

@unauthenticated_user
def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login_page')
    context = {'form':form}
    return render(request, 'signup.html', context)

@login_required(login_url='login')
def updateprofile(request):
    form = UpdateUserForm()
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            user_name = request.user.username
            user_ = Employee.objects.get(name=user_name)
            user_.name = form.cleaned_data['name']
            user_.email = form.cleaned_data['email']
            user_.phone = form.cleaned_data['phone']
            user_.save()
            return redirect('profile')
    context = {'form': form}
    return render(request, 'updateinfo.html', context)

@login_required(login_url='login_page')
def home(request):
    employees = Employee.objects.all()
    # "empoyees" is an inside joke from when my friend/classmate found that typo I made :)
    empoyees = []
    days = Day.objects.all()
    for employee in employees:
        em_list = []
        for day in days:
            job_ = ""
            emps = [day.manager, day.doctor1, day.doctor2, day.nurse1, day.nurse2, day.nurse3, day.nurse4, day.nurse5, day.nurse6]
            if employee.name in emps:
                if employee.job == "Nurse":
                    job_ = "nurse"
                elif employee.job == "Doctor":
                    job_ = 'doctor'
                elif employee.job == "Manager":
                    job_ = 'manager'
            else:
                job_ = 'off'
            em_list.append(job_)
        new_emp = Empoyee(employee.name, em_list)
        empoyees.append(new_emp)

    return render(request, "home.html", {'empoyees':empoyees, 'days': days})

@dataclass
class Empoyee:
    name: str
    emp_list: List[str]

@login_required(login_url='login_page')
def profile(request):
    user_name = request.user.username
    current_user = Employee.objects.get(name=user_name)
    return render(request, "profile.html", {'current_user':current_user})

@login_required(login_url='login_page')
def admin_only(request):
    empoyees = Employee.objects.all()
    return render(request, "admins.html", {'empoyees':empoyees})

def make_schedule(request):
    Day.objects.all().delete()
    sun = Day()
    sun.save()
    mon = Day()
    mon.save()
    tues = Day()
    tues.save()
    wed = Day()
    wed.save()
    thurs = Day()
    thurs.save()
    fri = Day()
    fri.save()
    sat = Day()
    sat.save()
    week = Day.objects.all()
    for day in week:
        manager = random.choice(Employee.objects.filter(job='Manager'))
        day.manager = manager.name
        doctor1 = random.choice(Employee.objects.filter(job='Doctor'))
        day.doctor1 = doctor1.name
        doctor2 = random.choice(Employee.objects.filter(job='Doctor'))
        while day.doctor2 == day.doctor1:
            doctor2 = random.choice(Employee.objects.filter(job='Doctor'))
        day.doctor2 = doctor2.name
        nurse_set = Employee.objects.filter(job="Nurse")
        nurses = []
        for nurse in nurse_set:
            nurses.append(nurse.name)
        day.nurse1 = random.choice(nurses)
        day.nurse2 = random.choice(nurses)
        while day.nurse2 == day.nurse1:
            day.nurse2 = random.choice(nurses)
        day.nurse3 = random.choice(nurses)
        while day.nurse3 == day.nurse2 or day.nurse3 == day.nurse1:
            day.nurse3 = random.choice(nurses)
        day.nurse4 = random.choice(nurses)
        while day.nurse4 == day.nurse3 or day.nurse4 == day.nurse2 or day.nurse4 == day.nurse1:
            day.nurse4 = random.choice(nurses)
        day.nurse5 = random.choice(nurses)
        while day.nurse5 == day.nurse4 or day.nurse5 == day.nurse3 or day.nurse5 == day.nurse2 or day.nurse5 == day.nurse1:
            day.nurse5 = random.choice(nurses)
        day.nurse6 = random.choice(nurses)
        while day.nurse6 == day.nurse5 or day.nurse6 == day.nurse4 or day.nurse6 == day.nurse3 or day.nurse6 == day.nurse2 or day.nurse6 == day.nurse1:
            day.nurse6 = random.choice(nurses)
        day.save()
    return redirect('home')

@login_required(login_url='login')
def messagepage(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            user_name = request.user.username
            post = form.save()
            post.content = form.cleaned_data['content']
            post.user = user_name
            post.save()
            # new_post = Message(user=Employee.objects.get(id=request.user.id), content=content)
    chat_messages = Message.objects.all()
    context = {'form':form, 'chat_messages':list(reversed(chat_messages))}
    return render(request, "messageform.html", context)
    