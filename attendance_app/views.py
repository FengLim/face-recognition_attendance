from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from attendance_app.EmailBackEnd import EmailBackEnd
from attendance_app.models import CustomUser


def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "login_page.html")


def register(request):
    return render(request, "register.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allow</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))

        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : " + request.user.email + "usertype : " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def student_signup(request):
    return render(request, "student_signup.html")


def do_student_signup(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")

    try:
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=3)
        user.save()
        messages.success(request, "Successfully Created Student Account")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request, "Failed to Created Student Account")
        return HttpResponseRedirect(reverse("show_login"))
