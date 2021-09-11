from django import forms
from django.forms import ChoiceField
from student_mangement_app.models import Courses, SessionYearModel, Subjects



class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

# class DateInput(forms.DateInput):
#     input_type = "date"

    
class AddStudentForm(forms.Form):
    email=forms.EmailField(label="الإيميل",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="كلمة المرور",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="الاسم الأول ",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="الاسم الأخير ",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="اسم المستخدم",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    address=forms.CharField(label="العنوان",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
 

    gender_choice=(
        ("ذكر","ذكر"),
        ("انثى","انثى")
    )

    # course=forms.ChoiceField(label="الصف",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    course = forms.ModelChoiceField(label='الصف',required=True, widget=forms.Select(attrs={"class":"form-control"}), queryset=Courses.objects.all())
    sex=forms.ChoiceField(label="الجنس",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    # session_year_id=forms.ChoiceField(label=" العام الدراسي",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ModelChoiceField(label=" العام الدراسي",required=True, widget=forms.Select(attrs={"class":"form-control"}), queryset=SessionYearModel.object.all())
    profile_pic=forms.FileField(label=" صورة للطالب",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditStudentForm(forms.Form):
    email=forms.EmailField(label="الإيميل",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="الاسم الأول ",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="الاسم الأخير ",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="اسم المستخدم",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    address=forms.CharField(label="العنوان",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))




    gender_choice=(
        ("ذكر","ذكر"),
        ("انثى","انثى")
    )

    course = forms.ModelChoiceField(label='الصف',required=True, widget=forms.Select(attrs={"class":"form-control"}), queryset=Courses.objects.all())
  
    sex=forms.ChoiceField(label="الجنس",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ModelChoiceField(label=" العام الدراسي",required=True, widget=forms.Select(attrs={"class":"form-control"}), queryset=SessionYearModel.object.all())
    profile_pic=forms.FileField(label="صورة شخصية للطالب ",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}),required=False)



class EditResultForm(forms.Form):
  
    def __init__(self, *args, **kwargs):
        self.staff_id=kwargs.pop("staff_id")
        staff_ida = self.staff_id
        print( self.staff_id)
        print( staff_ida)
        super(EditResultForm,self).__init__(*args,**kwargs)
        subject_list=[]
        try:
            subjects=Subjects.objects.filter(staff_id=self.staff_id)
            for subject in subjects:
                subject_single=(subject.id,subject.subject_name)
                subject_list.append(subject_single)
        except:
            subject_list=[]
        self.fields['subject_id'].choices=subject_list

   

    subject_id=forms.ChoiceField(label="المادة",widget=forms.Select(attrs={"class":"form-control"}))
    session_ids = forms.ModelChoiceField(label=" العام الدراسي",required=True, widget=forms.Select(attrs={"class":"form-control"}), queryset=SessionYearModel.object.all())
    # session_ids=forms.ChoiceField(label="الفصل ",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    student_ids=ChoiceNoValidation(label="الطالب",widget=forms.Select(attrs={"class":"form-control"}))
    assignment1_marks=forms.CharField(label="مذاكرة اولى ",widget=forms.TextInput(attrs={"class":"form-control"}))
    assignment2_marks=forms.CharField(label=" مذاكرة ثانية",widget=forms.TextInput(attrs={"class":"form-control"}))
    exam_marks=forms.CharField(label=" درجة الامتحان",widget=forms.TextInput(attrs={"class":"form-control"}))


