"""attendance_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from attendance_app import views, HodViews, StaffViews
from attendance_system import settings

urlpatterns = [
    path('demo',views.showDemoPage),
    path('admin/', admin.site.urls),
    path('',views.ShowLoginPage),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name='logout'),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_staff', HodViews.add_staff, name="add_staff"),
    path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
    path('add_student', HodViews.add_student, name="add_student"),
    path('add_student_save', HodViews.add_student_save, name="add_student_save"),
    path('add_course', HodViews.add_course, name="add_course"),
    path('add_course_save', HodViews.add_course_save, name="add_course_save"),
    path('manage_staff', HodViews.manage_staff, name="manage_staff"),
    path('manage_student', HodViews.manage_student, name="manage_student"),
    path('manage_course', HodViews.manage_course, name="manage_course"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff, name="edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
    path('edit_student/<str:student_id>', HodViews.edit_student, name="edit_student"),
    path('edit_student_save', HodViews.edit_student_save, name="edit_student_save"),

    # Staff
    path('staff_home', StaffViews.staff_home, name="staff_home"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)