from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = [('ADMIN', 'Administrator'), ('HOD', 'HOD'), ('FACULTY', 'Faculty')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='FACULTY')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.role}'


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class Faculty(models.Model):
    EMPLOYMENT_CHOICES = [('Permanent', 'Permanent'), ('Contract', 'Contract'), ('Visiting', 'Visiting')]
    STATUS_CHOICES = [('Active', 'Active'), ('Inactive', 'Inactive')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    faculty_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    profile_photo = models.ImageField(upload_to='faculty/', blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    designation = models.CharField(max_length=80)
    joining_date = models.DateField()
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    experience = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.faculty_id} - {self.name}'


class Qualification(models.Model):
    TYPE_CHOICES = [('Academic', 'Academic'), ('Professional', 'Professional'), ('Certification', 'Certification')]
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='qualifications')
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=120)
    institution = models.CharField(max_length=150)
    university = models.CharField(max_length=150, blank=True)
    year = models.PositiveIntegerField()
    percentage_cgpa = models.CharField(max_length=20, blank=True)
    qualification_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Academic')
    certificate = models.FileField(upload_to='qualifications/', blank=True, null=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f'{self.degree} - {self.faculty.name}'


class Subject(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    subject_code = models.CharField(
        max_length=30,
        unique=True
    )

    subject_name = models.CharField(
        max_length=150
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT
    )

    semester = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8)
        ]
    )

    academic_year = models.CharField(
        max_length=20,
        default='2026-27'
    )

    credits = models.PositiveIntegerField(default=3)

    hours_per_week = models.PositiveIntegerField(default=3)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Active'
    )

    def __str__(self):
        return f'{self.subject_code} - {self.subject_name}'




class SubjectAllocation(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Completed', 'Completed')]
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='allocations')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='allocations')
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    semester = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=20)
    hours_per_week = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(40)])
    allocation_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['faculty', 'subject', 'academic_year', 'semester'], name='unique_faculty_subject_allocation')
        ]

    def __str__(self):
        return f'{self.faculty.name} - {self.subject.subject_code}'


class Workload(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='workload_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    hours_per_week = models.PositiveIntegerField()
    academic_year = models.CharField(max_length=20)
    semester = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.faculty.name} - {self.hours_per_week} hrs'


class LeaveRequest(models.Model):
    LEAVE_TYPES = [('Casual', 'Casual'), ('Sick', 'Sick'), ('Emergency', 'Emergency'), ('Permission', 'Permission'), ('Other', 'Other')]
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')]
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    from_date = models.DateField()
    to_date = models.DateField()
    number_of_days = models.PositiveIntegerField(default=1)
    reason = models.TextField()
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_leaves')
    approval_date = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f'{self.faculty.name} - {self.leave_type} - {self.status}'


class PerformanceEvaluation(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='evaluations')
    evaluator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='evaluations_done')
    evaluation_period = models.CharField(max_length=50)
    evaluation_date = models.DateField()
    teaching_effectiveness = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    attendance_punctuality = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    subject_completion = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    student_feedback = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    academic_contribution = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    research_publications = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    department_activities = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    overall_performance = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rating = models.CharField(max_length=30, default='Needs Improvement')
    remarks = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Final')

    def calculate_score(self):
        fields = [self.teaching_effectiveness, self.attendance_punctuality, self.subject_completion, self.student_feedback,
                  self.academic_contribution, self.research_publications, self.department_activities, self.overall_performance]
        return round(sum(fields) / 8 * 10, 2)

    def save(self, *args, **kwargs):
        self.total_score = self.calculate_score()
        if self.total_score >= 85:
            self.rating = 'Excellent'
        elif self.total_score >= 70:
            self.rating = 'Good'
        elif self.total_score >= 50:
            self.rating = 'Satisfactory'
        else:
            self.rating = 'Needs Improvement'
        super().save(*args, **kwargs)
