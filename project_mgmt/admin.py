from django.contrib import admin

from .models import Project, Task, ProjectType, HistoryAndTransActions
from .models import CostType, CostUnit, TaskIssue, ProjectIssue, IssueCategory, ProjectStatus
from .models import ProjectCalendar, WorkingDay
# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(ProjectType)
admin.site.register(CostType)
admin.site.register(CostUnit)
admin.site.register(TaskIssue)
admin.site.register(ProjectIssue)
admin.site.register(IssueCategory)
admin.site.register(HistoryAndTransActions)
admin.site.register(ProjectCalendar)
admin.site.register(WorkingDay)
admin.site.register(ProjectStatus)