import django_filters
from .models import Students, Staffs,StudentInfoReport

class TypeFilterStudent(django_filters.FilterSet):

    #filter contains
    # admin = django_filters.CharFilter( label =" ابحث", lookup_expr='icontains')
    class Meta:
        model = Students
        fields = {
            
            'admin__first_name':['icontains'],
             'admin__last_name':['icontains'],
        
        }
       

class TypeFilterStaff(django_filters.FilterSet):
    
    #filter contains
    # admin = django_filters.CharFilter( label =" ابحث", lookup_expr='icontains')
    class Meta:
        model = Staffs
        fields = {
            
          'admin__first_name':['icontains'],
             'admin__last_name':['icontains'],
        
        }
       

class StaffInfoStudentFilter(django_filters.FilterSet):
    class Meta:
        model = StudentInfoReport
        fields ={ 'student_id__admin__first_name':['icontains'],
        'student_id__admin__last_name':['icontains'],
        # 'staff_id__admin__first_name':['icontains'],
        'studentInfo_id__subject_id__subject_name':['icontains'],
        }
       

class AdminInfoStudentFilter(django_filters.FilterSet):
    class Meta:
        model = StudentInfoReport
        fields ={ 'student_id__admin__first_name':['icontains'],
        'student_id__admin__last_name':['icontains'],
        'staff_id__admin__first_name':['icontains'],
        'staff_id__admin__last_name':['icontains'],
        'studentInfo_id__subject_id__subject_name':['icontains'],
        }
       