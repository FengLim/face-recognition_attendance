from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    objects = models.Manager()
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    objects = models.Manager()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Staffs.objects.create(admin=instance)
        if instance.user_type==3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1), address="", profile_pic="", gender="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.staffs.save()
    if instance.user_type==3:
        instance.students.save()