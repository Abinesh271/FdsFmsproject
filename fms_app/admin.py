from django.contrib import admin

from .models import (
    Department,
    Faculty,
    Qualification,
    Subject,
    SubjectAllocation,
    Workload,
    LeaveRequest,
    PerformanceEvaluation,
    UserProfile,
)

admin.site.register(Department)
admin.site.register(Faculty)
admin.site.register(Qualification)
admin.site.register(Subject)

# Subject Allocation
admin.site.register(SubjectAllocation)

admin.site.register(Workload)
admin.site.register(LeaveRequest)
admin.site.register(PerformanceEvaluation)
admin.site.register(UserProfile)