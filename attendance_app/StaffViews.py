from django.shortcuts import render


def staff_home(request):
    return render(request, "staff_template/staff_home_template.html")

def attendance(request):
    return render(request, "staff_template/staff_home_template.html")

def showStudentDetails(request):
    return render(request, "staff_template/staff_home_template.html")