
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addstudent", views.add_student, name="addStudent"),
    path("addteacher", views.add_teacher, name="addTeacher"),
    path("addcourse", views.add_course, name="addCourse"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),
    path("pending/<int:user_id>", views.pending, name="pending"),
    path("courses/<str:course_code>", views.course, name="course"),
    path("enroll/<int:user_id>/<str:course_code>", views.enroll, name="enroll"),
    path("courses/<str:course_code>/<int:post_id>", views.post, name="post"),
]