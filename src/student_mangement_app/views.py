from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth import  login, logout
from django.urls import reverse
from student_mangement_app.EmailBackEnd import EmailBackEnd
from student_mangement_app.models import Courses, CustomUser, SessionYearModel
from django.core.files.storage import FileSystemStorage

# Create your views here.

def demo(request):
    return render(request,'demo.html')


def ShowLoginPage(request):
    return render(request,"login_page.html")



def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user= EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        
        if user!=None:
            if user.active_status == False:
                return HttpResponseRedirect(reverse("wait"))
                
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request,"فشل تسجيل الدخول , الرجاء التأكد من الإيميل وكلمة المرور")
            return HttpResponseRedirect("/")



def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup_admin(request):
    return render(request,"signup_admin_page.html")

def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"signup_student_page.html",{"courses":courses,"session_years":session_years})

def signup_staff(request):
    return render(request,"signup_staff_page.html")



def do_admin_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1,active_status= False)
        user.save()
        messages.success(request,"تم إنشاء الحساب بنجاح")
        return HttpResponseRedirect(reverse("wait"))
    except:
        messages.error(request," فشل إنشاء الحساب")
        return HttpResponseRedirect(reverse("show_login"))

def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2,active_status= False)
        user.staffs.address=address
        user.save()
        messages.success(request,"تم إنشاء الحساب بنجاح")
        return HttpResponseRedirect(reverse("wait"))
    except:
        messages.error(request," فشل إنشاء الحساب")
        return HttpResponseRedirect(reverse("show_login"))

def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    profile_pic = request.FILES['profile_pic']
    fs=FileSystemStorage(location='media/student_pic/')
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)

    try:
        user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                            first_name=first_name, user_type=3,active_status= False)
        user.students.address = address
        course_obj = Courses.objects.get(id=course_id)
        user.students.course_id = course_obj
        session_year = SessionYearModel.object.get(id=session_year_id)
        user.students.session_year_id = session_year
        user.students.gender = sex
        user.students.profile_pic = profile_pic_url
        user.save()
        messages.success(request,"تم إنشاء الحساب بنجاح")
        return HttpResponseRedirect(reverse("wait"))
    except:
        messages.error(request, "Failed to Add Student")
        return HttpResponseRedirect(reverse("show_login"))


def wait(request):
    return render(request,'wait.html')

