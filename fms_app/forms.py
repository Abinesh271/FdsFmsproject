from datetime import date
from django import forms
from django.contrib.auth.models import User
from .models import Faculty, Qualification, Subject, SubjectAllocation, LeaveRequest, PerformanceEvaluation


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class FacultyForm(BootstrapModelForm):
    class Meta:
        model = Faculty
        fields = ['faculty_id', 'name', 'profile_photo', 'gender', 'dob', 'email', 'phone', 'address', 'department', 'designation', 'joining_date', 'employment_type', 'experience', 'status']
        widgets = {'dob': forms.DateInput(attrs={'type': 'date'}), 'joining_date': forms.DateInput(attrs={'type': 'date'}), 'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control'})}

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError('Enter a valid 10 digit phone number.')
        return phone

    def clean_joining_date(self):
        value = self.cleaned_data['joining_date']
        if value > date.today():
            raise forms.ValidationError('Joining date cannot be in the future.')
        return value


class QualificationForm(BootstrapModelForm):
    class Meta:
        model = Qualification
        fields = ['faculty', 'degree', 'specialization', 'institution', 'university', 'year', 'percentage_cgpa', 'qualification_type', 'certificate', 'remarks']


class SubjectForm(BootstrapModelForm):
    class Meta:
        model = Subject
        fields = ['subject_code', 'subject_name', 'department', 'semester', 'academic_year', 'credits', 'hours_per_week', 'status']


class AllocationForm(BootstrapModelForm):

    class Meta:
        model = SubjectAllocation
        fields = [
            'faculty',
            'subject',
            'department',
            'semester',
            'academic_year',
            'hours_per_week',
            'status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Show active subjects in the dropdown
        self.fields['subject'].queryset = Subject.objects.filter(
            status='Active'
        )

    def clean(self):
        cleaned = super().clean()

        faculty = cleaned.get('faculty')
        subject = cleaned.get('subject')
        department = cleaned.get('department')

        if faculty and subject:
            if faculty.department_id != subject.department_id:
                raise forms.ValidationError(
                    'Faculty and subject must belong to the same department.'
                )

        if faculty and department:
            if faculty.department_id != department.id:
                raise forms.ValidationError(
                    'Selected department does not match the faculty department.'
                )

        return cleaned


class LeaveForm(BootstrapModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['faculty', 'leave_type', 'from_date', 'to_date', 'reason']
        widgets = {'from_date': forms.DateInput(attrs={'type': 'date'}), 'to_date': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('from_date')
        end = cleaned.get('to_date')
        faculty = cleaned.get('faculty')
        if start and end and end < start:
            raise forms.ValidationError('To date cannot be before from date.')
        if faculty and start and end:
            overlap = LeaveRequest.objects.filter(faculty=faculty, status='Approved', from_date__lte=end, to_date__gte=start)
            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)
            if overlap.exists():
                raise forms.ValidationError('This faculty member already has approved leave for the selected dates.')
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.number_of_days = (obj.to_date - obj.from_date).days + 1
        if commit:
            obj.save()
        return obj


class PerformanceForm(BootstrapModelForm):
    class Meta:
        model = PerformanceEvaluation
        fields = ['faculty', 'evaluation_period', 'evaluation_date', 'teaching_effectiveness', 'attendance_punctuality', 'subject_completion', 'student_feedback', 'academic_contribution', 'research_publications', 'department_activities', 'overall_performance', 'remarks']
        widgets = {'evaluation_date': forms.DateInput(attrs={'type': 'date'})}


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('ADMIN', 'Administrator'), ('HOD', 'HOD'), ('FACULTY', 'Faculty')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']
