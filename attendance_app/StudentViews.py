from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from attendance_app.models import Courses, Students, CustomUser

import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def student_home(request):
    return render(request, "student_template/student_home_template.html")

def show_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    student=Students.objects.get(admin=user)
    return render(request, "student_template/show_profile.html",{"user":user,"student":student})

def edit_account(request,student_id):
    courses=Courses.objects.all()
    student=Students.objects.get(admin=student_id)
    return render(request,"student_template/edit_account_template.html",{"student":student,"courses":courses})

def edit_account_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        address = request.POST.get("address")

        profile_pic=request.FILES['profile_pic']
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()

            student=Students.objects.get(admin=student_id)
            student.address=address
            student.profile_pic = profile_pic_url
            student.save()
            messages.success(request, "Successfully Edited Student")
            return HttpResponseRedirect("/edit_account/"+student_id)
        except:
            messages.error(request, "Failed to Edit Student")
            return HttpResponseRedirect("/edit_account/"+student_id)

def attendance_check1(request):
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