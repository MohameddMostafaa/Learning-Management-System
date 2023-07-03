from .models import *

def my_context_processor(request):

    coursesContext = None
    coursesExistContext = None
    if request.user.is_authenticated:
        accTypeContext = request.user.type
        accTypeContext = str(accTypeContext)

        if accTypeContext == "moderator":
            coursesContext = Courses.objects.filter(group=request.user.group)
            if int(Courses.objects.filter(group=request.user.group).count()) == 0:
                coursesExistContext = False
            else:
                coursesExistContext = True

        elif accTypeContext == "admin":
            pass

        else:
            enrolledCoursesContext = Enrollment.objects.filter(user=request.user)
            enrolledCoursesIDsContext = enrolledCoursesContext.values_list('course__id', flat=True)
            coursesContext = Courses.objects.filter(id__in=enrolledCoursesIDsContext)
            if int(Courses.objects.filter(id__in=enrolledCoursesIDsContext).count()) == 0:
                coursesExistContext = False
            else:
                coursesExistContext = True

    return {
        "coursesContext": coursesContext,
        "coursesExistContext": coursesExistContext 
    }