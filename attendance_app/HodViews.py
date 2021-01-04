from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from attendance_app.models import CustomUser, Courses, Staffs, Students

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def admin_home(request):
    return render(request, "hod_template/home_content.html")

def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request, "Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect("/add_staff")

def add_student(request):
    courses=Courses.objects.all()
    return render(request, "hod_template/add_student_template.html",{"courses":courses})

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        profile_pic=request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        try:
            user=CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
            user.students.address=address
            course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=course_obj

            user.students.profile_pic=profile_pic_url
            user.students.gender=sex
            user.save()
            messages.success(request, "Successfully Added Student")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect("/add_student")


def add_course(request):
    return render(request, "hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model=Courses(course_name=course)
            course_model.save()
            messages.success(request, "Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request, "Failed to Add Course")
            return HttpResponseRedirect("/add_course")

def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/manage_student_template.html",{"students":students})

def manage_course(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/manage_course_template.html",{"courses":courses})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()

            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        except:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)

def edit_student(request,student_id):
    courses=Courses.objects.all()
    student=Students.objects.get(admin=student_id)
    return render(request,"hod_template/edit_student_template.html",{"student":student,"courses":courses})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        address = request.POST.get("address")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")

        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email
            user.save()

            student=Students.objects.get(admin=student_id)
            student.address=address
            student.gender=sex
            course=Courses.objects.get(id=course_id)
            student.course_id=course
            student.save()
            messages.success(request, "Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/"+student_id)
        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/"+student_id)

def attendance_check(request):
    path = r'D:\WinLib\Desktop\attendance-system\AiProject\ImagesAttendance'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(name):
        ### can include database here
        with open('Attendance.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)

        cv2.imshow('Webcam', img)
        #cv2.waitKey(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
            return HttpResponseRedirect("/add_staff")




    # imgElon = face_recognition.load_image_file(r'C:\Users\User10\Desktop\python\test.jpg')
    # imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)