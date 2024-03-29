from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from student_mangement_app.forms import EditResultForm
from student_mangement_app.models import Students, Subjects, StudentResult


class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        staff_id=request.user.id
        edit_result_form=EditResultForm(staff_id=staff_id)
        return render(request,"staff_template/edit_student_result.html",{"form":edit_result_form})

    def post(self,request,*args,**kwargs):
        form=EditResultForm(staff_id=request.user.id,data=request.POST)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            assignment1_marks = form.cleaned_data['assignment1_marks']
            assignment2_marks = form.cleaned_data['assignment2_marks']
            exam_marks = form.cleaned_data['exam_marks']
            subject_id = form.cleaned_data['subject_id']

            student_obj = Students.objects.get(admin=student_admin_id)
            subject_obj = Subjects.objects.get(id=subject_id)
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_assignment1_marks=assignment1_marks
            result.subject_assignment2_marks=assignment2_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "تم تحديث النتائج  ")
            return HttpResponseRedirect(reverse("edit_student_result"))
        else:
            messages.error(request, "فشل تحديث النتائج ")
            form=EditResultForm(request.POST,staff_id=request.user.id)
            return render(request,"staff_template/edit_student_result.html",{"form":form})


