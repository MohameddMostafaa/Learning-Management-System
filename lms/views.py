from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django import forms
from django.db.models import Q
import json
from .models import *
from .forms import *
from django.contrib import messages
from .tokens import account_activation_token



def index(request):
    if request.method == "GET":

        pendingAccs = None
        pendingExist = None
        courses = None
        coursesExist = None

        if request.user.is_authenticated:
            accType = request.user.type
            accType = str(accType)
            if accType == "admin":
                pendingAccs = PendingAccounts.objects.filter(emailVerified=True)
                pendingCount = pendingAccs.count()
                if int(pendingCount) == 0:
                    pendingExist = False
                else:
                    pendingExist = True
        
            elif accType == "moderator":
                courses = Courses.objects.filter(group=request.user.group)
                if int(Courses.objects.filter(group=request.user.group).count()) == 0:
                    coursesExist = False
                else:
                    coursesExist = True


            else:
                enrolledCourses = Enrollment.objects.filter(user=request.user)
                enrolledCoursesIDs = enrolledCourses.values_list('course__id', flat=True)
                courses = Courses.objects.filter(id__in=enrolledCoursesIDs)
                if int(Courses.objects.filter(id__in=enrolledCoursesIDs).count()) == 0:
                    coursesExist = False
                else:
                    coursesExist = True

            return render(request, f"lms/{accType}.html", {
                "courses": courses,
                "pending": pendingAccs,
                "pendingExist": pendingExist,
                "coursesExist": coursesExist
            })
        
        else:
            return HttpResponseRedirect(reverse("login"))
        



def add_student(request):
    if request.method == "GET":
        studentForm = None
        if request.user.is_authenticated:
            accType = request.user.type
            accType = str(accType)

            if accType == "moderator":
                studentForm = AddStudent()

            return render(request, "lms/addStudent.html", {
                "studentForm": studentForm,
            })
    
        else:
            return HttpResponseRedirect(reverse("login"))
    
    if request.method == "POST":
        if 'studentAdded' in request.POST:
            student = AddStudent(request.POST)
            if student.is_valid():
                newStudent = student.save(commit=False)
                newStudent.password = make_password(newStudent.password)
                if User.objects.filter(username=newStudent.username).exists():
                    return HttpResponse("This username already exists")
                newStudent.group = request.user.group
                newStudent.type = AccountTypes.objects.get(name="student")
                newStudent.save()

                return HttpResponseRedirect(reverse("index"))
            
def add_teacher(request):
    if request.method == "GET":
        teacherForm = None
        if request.user.is_authenticated:
            accType = request.user.type
            accType = str(accType)

            if accType == "moderator":
                teacherForm = AddTeacher()

            return render(request, "lms/addTeacher.html", {
                "teacherForm": teacherForm,
            })
    
        else:
            return HttpResponseRedirect(reverse("login"))
    
    if request.method == "POST":
        if 'teacherAdded' in request.POST:
            teacher = AddTeacher(request.POST)
            if teacher.is_valid():
                newTeacher = teacher.save(commit=False)
                newTeacher.password = make_password(newTeacher.password)
                if User.objects.filter(username=newTeacher.username).exists():
                    return HttpResponse("This username already exists")
                newTeacher.group = request.user.group
                newTeacher.type = AccountTypes.objects.get(name="teacher")
                newTeacher.save()

                return HttpResponseRedirect(reverse("index"))


def add_course(request):
    if request.method == "GET":
        courseForm = None
        if request.user.is_authenticated:
            accType = request.user.type
            accType = str(accType)

            if accType == "moderator":
                courseForm = AddCourse()

            return render(request, "lms/addCourse.html", {
                "courseForm": courseForm,
            })
    
        else:
            return HttpResponseRedirect(reverse("login"))
    
    if request.method == "POST":
        if 'courseAdded' in request.POST:
            course = AddCourse(request.POST)
            if course.is_valid():
                newCourse = course.save(commit=False)

                if Courses.objects.filter(name=newCourse.code).exists():
                    return HttpResponse("A Course with that name already exists")
                newCourse.group = request.user.group
                newCourse.save()
            
                return HttpResponseRedirect(reverse("index"))



def login_view(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "lms/login.html")
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "lms/login.html", {
                "message": "Please enter valid username/password"
            })
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "GET":
        return render(request, "lms/register.html", {
            "regForm": RegisterForm()
        })
    
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            PendingUser = form.save(commit=False)
            PendingUser.group = form.cleaned_data.get('group')
            if User.objects.filter(username=PendingUser.username).exists():
                return render(request, "lms/register.html", {
                    "message" : "Username already taken"
                })

            PendingUser.save()

            activateEmail(request, PendingUser, form.cleaned_data.get('email'))
            
            
            return render(request, "lms/login.html", {
                "message" : "Please go to your email's inbox and click on received activation link to confirm and complete the registration. Your account won't be considered for acceptance unless your email is verified. <b>Note:</b> Check your spam folder."
            })
        
        else:
            return render(request, "lms/register.html", {
                "message" : "Invalid Register Form"
            })

def pending(request, user_id):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":
            pendingUser = PendingAccounts.objects.get(pk=user_id)
            data = json.load(request)
            message = data.get('message')
            if message == "accept":
                if RegisteredGroups.objects.filter(name=pendingUser.group).exists():
                   pass
                else:
                    newGroup = RegisteredGroups(name=pendingUser.group) 
                    newGroup.save()

                newUser = User(username=pendingUser.username, password=pendingUser.password, email=pendingUser.email, group=RegisteredGroups.objects.get(name=pendingUser.group), type=AccountTypes.objects.get(name="moderator"))
                newUser.save()
                pendingUser.delete()
            elif message == "reject":
                pendingUser.delete()
            return JsonResponse({'status': 'Accept/Reject process succeeded!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    

def course(request, course_code):
    if request.method == "GET":

        eligible = False
        enrolled = None
        not_enrolled = None
        postForm = None
        posts = None
        postsExist = None
        usersExist = None

        accType = str(request.user.type)
        course = Courses.objects.get(code=course_code)

        if (request.user.group == course.group and accType == "moderator") or (request.user.group == course.group and Enrollment.objects.filter(user=request.user, course=course).exists()):
            
            eligible = True
            
            posts = Posts.objects.filter(course=course)

            if int(Posts.objects.filter(course=course).count()) == 0:
                postsExist = False
            else:
                postsExist = True
            
            if (int(User.objects.filter(group=course.group, type=AccountTypes.objects.get(name="student")).count())) + (int(User.objects.filter(group=course.group, type=AccountTypes.objects.get(name="teacher")).count())) == 0:
                usersExist = False
            else:
                usersExist = True

            if accType == "moderator":
                enrolledUsers = Enrollment.objects.filter(course=Courses.objects.get(code=course_code))
                enrolledIDs = enrolledUsers.values_list('user__id', flat=True)
                enrolled = User.objects.filter(id__in=enrolledIDs)
                not_enrolled = User.objects.filter((Q(group=course.group, type=AccountTypes.objects.get(name="student")) | Q(group=course.group, type=AccountTypes.objects.get(name="teacher"))) & ~Q(id__in=enrolledIDs))

            elif accType == "teacher":
                postForm = AddPost()

        return render(request, "lms/course.html", {
            "course": course,
            "eligible": eligible,
            "accType": accType,
            "enrolled": enrolled,
            "not_enrolled": not_enrolled,
            "postForm": postForm,
            "posts": posts,
            "postsExist": postsExist,
            "usersExist": usersExist
        })

    if request.method == "POST":
        post = AddPost(request.POST, request.FILES)
        if post.is_valid():
            newPost = post.save(commit=False)
            newPost.user = request.user
            newPost.course = Courses.objects.get(code=course_code)
            if request.FILES:
                newPost.file = request.FILES['file']
            newPost.save()
            return HttpResponseRedirect(reverse("course", args=[course_code]))




def enroll(request, user_id, course_code):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == "POST":
            userObject = User.objects.get(pk=user_id)
            courseObject = Courses.objects.get(code=course_code)
            data = json.load(request)
            message = data.get('message')
            if message == "enroll":
                new_enrollment = Enrollment(user=userObject, course=courseObject)
                new_enrollment.save()
            elif message == "unenroll":
                remove_enrollment = Enrollment.objects.get(user=userObject, course=courseObject)
                remove_enrollment.delete()
            return JsonResponse({'status': 'Enroll/Unenroll process succeeded!'})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    

def post(request, course_code, post_id):
    if request.method == "GET":
        eligible = False
        post = None
        submissionForm = None
        submissions = None
        mySubmission = None
        accType = str(request.user.type)
        course = Courses.objects.get(code=course_code)
        if (request.user.group == course.group and accType == "moderator") or (request.user.group == course.group and Enrollment.objects.filter(user=request.user, course=course).exists()):
            eligible = True
            post = Posts.objects.get(pk=post_id)

            if (post.canSubmit == "on") and (accType == "student"):
                if Submissions.objects.filter(user=request.user, post=post).exists():
                    mySubmission = Submissions.objects.get(user=request.user, post=post)
                else:
                    submissionForm = AddSubmission()

        
            if accType == "teacher":
                submissions = Submissions.objects.filter(post=post)

        return render(request, "lms/post.html", {
            'eligible': eligible,
            'course': course,
            "post": post,
            "submissionForm": submissionForm,
            "submissions": submissions,
            "mySubmission": mySubmission
        })
    
    if request.method == "POST":
        submission = AddSubmission(request.POST, request.FILES)
        if submission.is_valid():
            newSubmission = submission.save(commit=False)
            newSubmission.user = request.user
            newSubmission.post = Posts.objects.get(pk=post_id)
            newSubmission.file = request.FILES['file']
            newSubmission.save()
            return HttpResponseRedirect(reverse("post", args=[course_code, post_id]))


def activateEmail(request, PendingUserInstance, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('lms/template_activate_account.html', {
        'user': PendingUserInstance.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(PendingUserInstance.pk)),
        'token': account_activation_token.make_token(PendingUserInstance),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Please go to you email <b>{to_email}</b> inbox and click on \
            received activation link to confirm and complete the registration. Your account won't be considered for acceptance unless your email is verified. Note: Check your spam folder.")
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        if PendingAccounts.objects.filter(pk=uid).exists():
            user = PendingAccounts.objects.get(pk=uid)

        else:
            user = None

    except(TypeError, ValueError, OverflowError) as e:
        user = None


    if user is not None and account_activation_token.check_token(user, token):
        user.emailVerified = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return HttpResponseRedirect(reverse("login"))
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return HttpResponseRedirect(reverse("index"))