from datetime import date
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .decorators import get_role, role_required
from .forms import FacultyForm, QualificationForm, SubjectForm, AllocationForm, LeaveForm, PerformanceForm, UserCreateForm
from .models import Department, Faculty, Qualification, Subject, SubjectAllocation, Workload, LeaveRequest, PerformanceEvaluation, UserProfile


def login_page(request):
    return render(request, 'registration/login.html')


@login_required
def dashboard(request):
    role = get_role(request.user)
    faculties = Faculty.objects.all()
    if role == 'HOD':
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.department:
            faculties = faculties.filter(department=profile.department)
    if role == 'FACULTY':
        faculties = faculties.filter(user=request.user)
    context = {
        'role': role,
        'own_faculty': Faculty.objects.filter(user=request.user).first(),
        'total_faculty': faculties.count(),
        'active_faculty': faculties.filter(status='Active').count(),
        'departments': Department.objects.filter(status=True).count(),
        'subjects': Subject.objects.filter(status='Active').count(),
        'pending_leaves': LeaveRequest.objects.filter(status='Pending').count() if role != 'FACULTY' else LeaveRequest.objects.filter(faculty__user=request.user, status='Pending').count(),
        'allocations': SubjectAllocation.objects.filter(status='Active').count(),
        'high_workload': [f for f in faculties if f.allocations.filter(status='Active').aggregate(total=Sum('hours_per_week'))['total'] and f.allocations.filter(status='Active').aggregate(total=Sum('hours_per_week'))['total'] > 20][:5],
        'recent_evaluations': PerformanceEvaluation.objects.select_related('faculty').order_by('-evaluation_date')[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
@role_required('ADMIN', 'HOD')
def faculty_list(request):
    qs = Faculty.objects.select_related('department').all().order_by('name')
    q = request.GET.get('q', '')
    department = request.GET.get('department', '')
    designation = request.GET.get('designation', '')
    status = request.GET.get('status', '')
    if get_role(request.user) == 'HOD':
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.department:
            qs = qs.filter(department=profile.department)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(faculty_id__icontains=q) | Q(email__icontains=q))
    if department:
        qs = qs.filter(department_id=department)
    if designation:
        qs = qs.filter(designation__icontains=designation)
    if status:
        qs = qs.filter(status=status)
    paginator = Paginator(qs, 8)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'faculty/list.html', {'page': page, 'departments': Department.objects.filter(status=True), 'q': q, 'designation': designation, 'status': status})


@login_required
@role_required('ADMIN', 'HOD')
def faculty_add(request):
    form = FacultyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        faculty = form.save()
        messages.success(request, 'Faculty profile added successfully.')
        return redirect('faculty_detail', faculty.pk)
    return render(request, 'faculty/form.html', {'form': form, 'title': 'Add Faculty', 'button': 'Save Faculty'})


@login_required
@role_required('ADMIN', 'HOD')
def faculty_edit(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if get_role(request.user) == 'HOD' and faculty.department != getattr(request.user.userprofile, 'department', None):
        messages.error(request, 'You can edit only your department faculty.')
        return redirect('faculty_list')
    form = FacultyForm(request.POST or None, request.FILES or None, instance=faculty)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Faculty profile updated.')
        return redirect('faculty_detail', faculty.pk)
    return render(request, 'faculty/form.html', {'form': form, 'title': 'Edit Faculty', 'button': 'Update Faculty', 'faculty': faculty})


@login_required
def faculty_detail(request, pk):
    faculty = get_object_or_404(Faculty.objects.select_related('department'), pk=pk)
    if get_role(request.user) == 'FACULTY' and faculty.user != request.user:
        messages.error(request, 'You can view only your profile.')
        return redirect('dashboard')
    return render(request, 'faculty/detail.html', {'faculty': faculty, 'qualifications': faculty.qualifications.all(), 'allocations': faculty.allocations.select_related('subject'), 'leaves': faculty.leaves.order_by('-applied_date')[:5], 'evaluations': faculty.evaluations.order_by('-evaluation_date')[:5]})


@login_required
@role_required('ADMIN')
def faculty_delete(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        faculty.delete()
        messages.success(request, 'Faculty profile deleted.')
    return redirect('faculty_list')


@login_required
def qualification_list(request):
    qs = Qualification.objects.select_related('faculty').order_by('-year')
    if get_role(request.user) == 'FACULTY':
        qs = qs.filter(faculty__user=request.user)
    elif get_role(request.user) == 'HOD':
        qs = qs.filter(faculty__department=getattr(request.user.userprofile, 'department', None))
    return render(request, 'qualification/list.html', {'qualifications': qs})


@login_required
@role_required('ADMIN', 'HOD')
def qualification_add(request):
    form = QualificationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        messages.success(request, 'Qualification saved successfully.')
        return redirect('qualification_list')
    return render(request, 'qualification/form.html', {'form': form, 'title': 'Add Qualification'})


@login_required
@role_required('ADMIN', 'HOD')
def qualification_edit(request, pk):
    obj = get_object_or_404(Qualification, pk=pk)
    form = QualificationForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save(); messages.success(request, 'Qualification updated.'); return redirect('qualification_list')
    return render(request, 'qualification/form.html', {'form': form, 'title': 'Edit Qualification'})


@login_required
@role_required('ADMIN', 'HOD')
def qualification_delete(request, pk):
    obj = get_object_or_404(Qualification, pk=pk)
    if request.method == 'POST': obj.delete(); messages.success(request, 'Qualification deleted.')
    return redirect('qualification_list')


@login_required
@role_required('ADMIN', 'HOD')
def subject_list(request):
    qs = Subject.objects.select_related('department').order_by('subject_code')
    q = request.GET.get('q', '')
    department = request.GET.get('department', '')
    if q: qs = qs.filter(Q(subject_code__icontains=q) | Q(subject_name__icontains=q))
    if department: qs = qs.filter(department_id=department)
    return render(request, 'subject/list.html', {'subjects': qs, 'departments': Department.objects.filter(status=True), 'q': q, 'selected_department': department})


@login_required
@role_required('ADMIN', 'HOD')
def subject_add(request):
    form = SubjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request, 'Subject added.'); return redirect('subject_list')
    return render(request, 'subject/form.html', {'form': form, 'title': 'Add Subject'})


@login_required
@role_required('ADMIN', 'HOD')
def subject_edit(request, pk):
    obj = get_object_or_404(Subject, pk=pk); form = SubjectForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request, 'Subject updated.'); return redirect('subject_list')
    return render(request, 'subject/form.html', {'form': form, 'title': 'Edit Subject'})


@login_required
@role_required('ADMIN')
def subject_delete(request, pk):
    obj = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST': obj.delete(); messages.success(request, 'Subject deleted.')
    return redirect('subject_list')


@login_required
@role_required('ADMIN', 'HOD', 'FACULTY')
def allocation_list(request):
    qs = SubjectAllocation.objects.select_related('faculty', 'subject', 'department').order_by('-allocation_date')
    if get_role(request.user) == 'HOD': qs = qs.filter(department=getattr(request.user.userprofile, 'department', None))
    if get_role(request.user) == 'FACULTY': qs = qs.filter(faculty__user=request.user)
    department = request.GET.get('department', '')
    semester = request.GET.get('semester', '')
    year = request.GET.get('academic_year', '')
    if department: qs = qs.filter(department_id=department)
    if semester: qs = qs.filter(semester=semester)
    if year: qs = qs.filter(academic_year=year)
    return render(request, 'allocation/list.html', {'allocations': qs, 'departments': Department.objects.filter(status=True), 'selected_department': department, 'selected_semester': semester, 'selected_year': year})


@login_required
@role_required('ADMIN', 'HOD')
def allocation_add(request):
    form = AllocationForm(request.POST or None)
    if get_role(request.user) == 'HOD': form.fields['department'].queryset = Department.objects.filter(pk=getattr(request.user.userprofile, 'department_id', None))
    if request.method == 'POST' and form.is_valid():
        obj = form.save()
        Workload.objects.update_or_create(faculty=obj.faculty, subject=obj.subject, academic_year=obj.academic_year, semester=obj.semester, defaults={'hours_per_week': obj.hours_per_week})
        messages.success(request, 'Subject allocated and workload updated.')
        return redirect('allocation_list')
    return render(request, 'allocation/form.html', {'form': form, 'title': 'Allocate Subject'})


@login_required
@role_required('ADMIN', 'HOD')
def allocation_delete(request, pk):
    obj = get_object_or_404(SubjectAllocation, pk=pk)
    if request.method == 'POST':
        Workload.objects.filter(faculty=obj.faculty, subject=obj.subject, academic_year=obj.academic_year, semester=obj.semester).delete()
        obj.delete(); messages.success(request, 'Allocation removed and workload recalculated.')
    return redirect('allocation_list')


@login_required
@role_required('ADMIN', 'HOD', 'FACULTY')
def workload(request):
    faculties = Faculty.objects.select_related('department').all()
    if get_role(request.user) == 'HOD': faculties = faculties.filter(department=getattr(request.user.userprofile, 'department', None))
    if get_role(request.user) == 'FACULTY': faculties = faculties.filter(user=request.user)
    rows = []
    for faculty in faculties:
        total = faculty.allocations.filter(status='Active').aggregate(total=Sum('hours_per_week'))['total'] or 0
        rows.append({'faculty': faculty, 'total': total, 'items': faculty.allocations.filter(status='Active').select_related('subject')})
    return render(request, 'workload/dashboard.html', {'rows': rows})


@login_required
@role_required('ADMIN', 'HOD', 'FACULTY')
def leave_list(request):
    qs = LeaveRequest.objects.select_related('faculty', 'approved_by').order_by('-applied_date')
    if get_role(request.user) == 'HOD': qs = qs.filter(faculty__department=getattr(request.user.userprofile, 'department', None))
    if get_role(request.user) == 'FACULTY': qs = qs.filter(faculty__user=request.user)
    status = request.GET.get('status', '')
    if status: qs = qs.filter(status=status)
    return render(request, 'leave/list.html', {'leaves': qs, 'status': status, 'role': get_role(request.user)})


@login_required
@role_required('ADMIN', 'HOD', 'FACULTY')
def leave_add(request):
    form = LeaveForm(request.POST or None)
    role = get_role(request.user)
    if role == 'FACULTY':
        form.fields['faculty'].queryset = Faculty.objects.filter(user=request.user)
        faculty = Faculty.objects.filter(user=request.user).first()
        if faculty: form.fields['faculty'].initial = faculty
    elif role == 'HOD':
        form.fields['faculty'].queryset = Faculty.objects.filter(department=getattr(request.user.userprofile, 'department', None))
    if request.method == 'POST' and form.is_valid(): form.save(); messages.success(request, 'Leave request submitted.'); return redirect('leave_list')
    return render(request, 'leave/form.html', {'form': form})


@login_required
@role_required('ADMIN', 'HOD')
def leave_action(request, pk, action):
    leave = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST' and leave.status == 'Pending':
        if action == 'approve': leave.status = 'Approved'; message = 'Leave approved.'
        else: leave.status = 'Rejected'; message = 'Leave rejected.'
        leave.approved_by = request.user; leave.approval_date = timezone.now(); leave.remarks = request.POST.get('remarks', '')
        leave.save(); messages.success(request, message)
    return redirect('leave_list')


@login_required
@role_required('ADMIN', 'HOD', 'FACULTY')
def performance_list(request):
    qs = PerformanceEvaluation.objects.select_related('faculty', 'evaluator').order_by('-evaluation_date')
    if get_role(request.user) == 'HOD': qs = qs.filter(faculty__department=getattr(request.user.userprofile, 'department', None))
    if get_role(request.user) == 'FACULTY': qs = qs.filter(faculty__user=request.user)
    return render(request, 'performance/list.html', {'evaluations': qs})


@login_required
@role_required('ADMIN', 'HOD')
def performance_add(request):
    form = PerformanceForm(request.POST or None)
    if get_role(request.user) == 'HOD': form.fields['faculty'].queryset = Faculty.objects.filter(department=getattr(request.user.userprofile, 'department', None))
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False); obj.evaluator = request.user; obj.save(); messages.success(request, f'Evaluation saved. Score: {obj.total_score}/100 ({obj.rating}).'); return redirect('performance_list')
    return render(request, 'performance/form.html', {'form': form})


@login_required
@role_required('ADMIN', 'HOD')
def performance_delete(request, pk):
    obj = get_object_or_404(PerformanceEvaluation, pk=pk)
    if request.method == 'POST': obj.delete(); messages.success(request, 'Evaluation deleted.')
    return redirect('performance_list')


@login_required
@role_required('ADMIN')
def user_add(request):
    form = UserCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False); role = form.cleaned_data['role']; user.set_password(form.cleaned_data['password']); user.save()
        UserProfile.objects.create(user=user, role=role)
        messages.success(request, 'User account created.')
        return redirect('dashboard')
    return render(request, 'dashboard/user_form.html', {'form': form})


@login_required
@role_required('ADMIN')
def reports(request):
    return render(request, 'reports/index.html', {
        'department_rows': Department.objects.annotate(faculty_count=Count('faculty'), subject_count=Count('subject')),
        'allocation_count': SubjectAllocation.objects.count(),
        'leave_count': LeaveRequest.objects.count(),
        'evaluation_count': PerformanceEvaluation.objects.count(),
    })
