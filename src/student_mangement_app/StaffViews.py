from django.shortcuts import render
from student_mangement_app.models import Attendance, AttendanceProgram, AttendanceReport, ContactStaff, Courses, CustomUser, FeedBackStaffs, LeaveReportStaff, SessionYearModel, Staffs, StudentInfo, StudentInfoReport, StudentResult, Students, Subjects
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .filters import StaffInfoStudentFilter


def staff_home(request):
    #For Fetch All Student Under Staff
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count=Students.objects.filter(course_id__in=final_course).count()

    #Fetch All Attendance Count
    attendance_count=Attendance.objects.filter(subject_id__in=subjects).count()

    #Fetch All Approve Leave
    staff=Staffs.objects.get(admin=request.user.id)
    leave_count=LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count=subjects.count()

    #Fetch Attendance Data by Subject
    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request,"staff_template/staff_home_template.html",{"students_count":students_count,"attendance_count":attendance_count,"leave_count":leave_count,"subject_count":subject_count,"subject_list":subject_list,"attendance_list":attendance_list,"student_list":student_list,"present_list":student_list_attendance_present,"absent_list":student_list_attendance_absent})



def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_take_attendance.html",{"subjects":subjects,"session_years":session_years})

#to get all student in staff_take_attendance
@csrf_exempt #decorator to dont need to pass csrf token when using ajax
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)  #function converts a Python object into a json string    



@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=request.POST.get("attendance_date")
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    print(student_ids)
    json_sstudent=json.loads(student_ids) #loads() takes in a string and returns a json object
    #print(data[0]['id'])


    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")




#######update attendance function ########### 

def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})

#to get all attendance in staff_update_attendance
@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)



@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)
    json_sstudent=json.loads(student_ids)


    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")




def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_template/staff_apply_leave.html",{"leave_data":leave_data})

def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_apply_leave"))
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStaff(staff_id=staff_obj,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "تم إرسال الطلب بنجاح")
            return HttpResponseRedirect(reverse("staff_apply_leave"))
        except:
            messages.error(request, "فشل إرسال الطلب")
            return HttpResponseRedirect(reverse("staff_apply_leave"))


def staff_feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_template/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_feedback_save"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "تم إرسال الشكوى بنجاح")
            return HttpResponseRedirect(reverse("staff_feedback"))
        except:
            messages.error(request, "فشل إرسال الشكوى")
            return HttpResponseRedirect(reverse("staff_feedback"))


def staff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    staff=Staffs.objects.get(admin=user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "تم تعديل الملف الشخصي بنجاح")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "فشل تعديل الملف الشخصي")
            return HttpResponseRedirect(reverse("staff_profile"))



def staff_add_result(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()
    return render(request,"staff_template/staff_add_result.html",{"subjects":subjects,"session_years":session_years})

def save_student_result(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id=request.POST.get('student_list')
    assignment_marks1=request.POST.get('assignment_marks1')
    assignment_marks2=request.POST.get('assignment_marks2')
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')


    student_obj=Students.objects.get(admin=student_admin_id)
    subject_obj=Subjects.objects.get(id=subject_id)

    try:
        check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_assignment1_marks=assignment_marks1
            result.subject_assignment2_marks=assignment_marks2
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "تم تعديل النتائج بنجاح")
            return HttpResponseRedirect(reverse("staff_add_result"))
        else:
            result=StudentResult(student_id=student_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment1_marks=assignment_marks1,subject_assignment2_marks=assignment_marks2)
            result.save()
            messages.success(request, "تم إضافة النتائج بنجاح")
            return HttpResponseRedirect(reverse("staff_add_result"))
    except:
        messages.error(request, "فشل إضافة النتائج")
        return HttpResponseRedirect(reverse("staff_add_result"))    


@csrf_exempt
def fetch_result_student(request):
    subject_id=request.POST.get('subject_id')
    student_id=request.POST.get('student_id')
    student_obj=Students.objects.get(admin=student_id)
    result=StudentResult.objects.filter(student_id=student_obj.id,subject_id=subject_id).exists()
    if result:
        result=StudentResult.objects.get(student_id=student_obj.id,subject_id=subject_id)
        result_data={"exam_marks":result.subject_exam_marks,"assign1_marks":result.subject_assignment1_marks,"assign2_marks":result.subject_assignment2_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")



def manager_msg(request):
    staff_obj = Staffs.objects.get(admin_id=request.user.id)
    manager_msg = ContactStaff.objects.filter(staff_id= staff_obj)
    
    return render(request,"staff_template/manager_contact.html",{"messages":manager_msg})

    
def att_program_t(request):


    # staff = Staffs.objects.get(admin=request.user.id)
    subjects = Subjects.objects.filter(staff_id = request.user.id)
    course_id_list=[]
    for subject in subjects:
        course=Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course=[]
    #removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)


    print(final_course)
    try:
        att = AttendanceProgram.objects.filter(course_id__in= final_course)
    except:
        att = None


    return render(request,"staff_template/attendance_program.html",{'att':att})


def staff_add_info(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.object.all()

    staff_id = Staffs.objects.get(admin_id=request.user.id)
    info_all = StudentInfoReport.objects.filter(staff_id=staff_id)

    myfilter = StaffInfoStudentFilter(request.GET, queryset= info_all)
    info_all = myfilter.qs

    return render(request,"staff_template/staff_add_info.html",{"subjects":subjects,"session_years":session_years,'info_all':info_all,'myfilter':myfilter})

@csrf_exempt
def save_staff_add_info(request):
    student_id=request.POST.get("student_id")
    subject_id=request.POST.get("subject_id")
    info_data=request.POST.get("info_data")
    session_year_id=request.POST.get("session_year_id")


   
    staff_id = Staffs.objects.get(admin_id=request.user.id)
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    student=Students.objects.get(admin=student_id)
      
    try:

        info = StudentInfo.objects.filter(student_id =student ,subject_id=subject_model,session_year_id=session_model).exists()
        if(info):
            info = StudentInfo.objects.get(student_id =student ,subject_id=subject_model,session_year_id=session_model)
           
        else:
            info = StudentInfo(student_id =student ,subject_id=subject_model,session_year_id=session_model)
            info.save()

    
        student_info_report = StudentInfoReport.objects.filter(staff_id=staff_id,student_id=student,studentInfo_id=info).exists()
        if(student_info_report):
            
            student_info_report = StudentInfoReport.objects.get(staff_id=staff_id,student_id=student,studentInfo_id=info)
            student_info_report.info = info=info_data
            student_info_report.save()
        else :
            student_info_report=StudentInfoReport(info=info_data,staff_id=staff_id,student_id=student,studentInfo_id=info)
            student_info_report.save()




       
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")



def show_info(request, id):
    info = StudentInfoReport.objects.get(id = id)
  
    return render(request,"staff_template/show_info.html",{'info':info})



def edit_student_info(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.object.all()
    return render(request,"staff_template/edit_student_info.html",{"subjects":subjects,"session_year_id":session_year_id})


@csrf_exempt
def get_info_student(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    student_info=StudentInfo.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)

    info_report=StudentInfoReport.objects.filter(studentInfo_id__in=student_info,)
    list_data=[]

    for student in info_report:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def get_info_content(request):
    student=request.POST.get("student_id")
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")

    student_id = Students.objects.get(admin=student)  
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    staff_id = Staffs.objects.get(admin_id=request.user.id)

    student_info=StudentInfo.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    info_report=StudentInfoReport.objects.get(staff_id=staff_id,studentInfo_id__in=student_info,student_id = student_id)
    info_data={'info':info_report.info}
    return JsonResponse(json.dumps(info_data),content_type="application/json",safe=False)

   
   

@csrf_exempt
def save_update_info(request):
    student_id=request.POST.get("student_id")
    subject_id=request.POST.get("subject_id")
    info_data=request.POST.get("info_data")
    session_year_id=request.POST.get("session_year_id") 

    staff_id = Staffs.objects.get(admin_id=request.user.id)
    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.object.get(id=session_year_id)
    student=Students.objects.get(admin=student_id)

    student_info=StudentInfo.objects.filter(subject_id=subject_model,session_year_id=session_model)
    try:
        student_info_report = StudentInfoReport.objects.get(staff_id=staff_id,student_id=student,studentInfo_id__in=student_info)
        student_info_report.info = info_data
        student_info_report.save()
     
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

# def get_students2(request):
#     subject_id=request.POST.get("subject")
#     session_year=request.POST.get("session_year")

#     subject=Subjects.objects.get(id=subject_id)
#     session_model=SessionYearModel.object.get(id=session_year)
#     students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
#     list_data=[]

#     for student in students:
#         data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
#         list_data.append(data_small)
#     return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)  #function converts a Python object into a json string    
