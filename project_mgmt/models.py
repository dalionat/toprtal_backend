from django.db import models
from organization_mgmt.models import Department
from django.contrib.auth.models import User


# Basic Info
class IssueCategory(models.Model):
    issue_category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.title
 
class CostUnit(models.Model):
    cost_unit_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, unique=True)
    fa_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.fa_title

class CostType(models.Model):
    cost_type_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    fa_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.ForeignKey(CostUnit, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.fa_title

class ProjectType(models.Model):
    project_type_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    fa_title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
class ProjectStatus(models.Model):
    project_status_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    

    
class ProjectCalendar(models.Model):
    project_calendar_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
class WorkingDay(models.Model):
    WORKING_DAYS = (
        ("Saturday","شنبه"),
        ("Sunday","یکشنبه"),
        ("Monday","دوشنبه"),
        ("Tuesday","سه شنبه"),
        ("Wednesday","چهارشنبه"),
        ("Thursday","پنج شنبه"),
    )
    working_day_id = models.AutoField(primary_key=True)
    calendar = models.ForeignKey(ProjectCalendar, on_delete=models.CASCADE, related_name="working_days")
    title = models.CharField(choices=WORKING_DAYS,max_length=50)
    start_at = models.TimeField()
    end_at = models.TimeField()

    def __str__(self) -> str:
        return self.calendar.title + ' ' + self.title + ' (' + str(self.start_at) + ' - ' + str(self.end_at) + ')'


# Models
class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department,to_field="department_id",on_delete=models.CASCADE, related_name="dep_projects")
    project_type = models.ForeignKey(ProjectType,to_field="project_type_id" ,on_delete=models.DO_NOTHING, related_name="projects")
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="manager_projects")
    status = models.ForeignKey(ProjectStatus, to_field="project_status_id", on_delete=models.DO_NOTHING)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    calendar = models.ForeignKey(ProjectCalendar, on_delete=models.DO_NOTHING, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="created_projects")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="updated_projects")
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
class ProjectCharter(models.Model):
    pass

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, to_field="project_id", on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=500)
    is_summery = models.BooleanField(default=0)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    actual_progress = models.DecimalField(max_digits=5, decimal_places=2)
    parent = models.ForeignKey("Task", on_delete=models.CASCADE, blank=True, null=True, related_name="childs")
    cost_type = models.ForeignKey(CostType,to_field="cost_type_id" ,on_delete=models.DO_NOTHING, null=True)
    cost = models.PositiveBigIntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="my_created_tasks")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="my_updated_tasks")
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    # assigneee configs
    assignee = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="my_assigments")
    status_manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="my_approval_assignments")

    def __str__(self) -> str:
        return self.title

    
class HistoryAndTransActions(models.Model):
    APPROVAL_STATUS = (
        ("pending", "در حال بررسی"),
        ("rejected", "رد شده"),
        ("approved", "تایید شده")
    )
    task = models.ForeignKey(Task,to_field="task_id" ,on_delete=models.CASCADE, related_name="transactions")
    from_actual = models.DecimalField(max_digits=5, decimal_places=2)
    to_actual = models.DecimalField(max_digits=5, decimal_places=2)
    approval_status = models.TextField(choices=APPROVAL_STATUS)
    submitted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="submitter_transactions")
    submitted_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    submbitter_description = models.TextField(blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="approver_transactions")
    approved_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    approver_description = models.TextField(blank=True)
    document = models.TextField(max_length=150, blank=True)

    
    
class ProjectIssue(models.Model):
    ISSUE_TYPE = (
        ("solvable", "قابل حل"),
        ("unsolvable", "غیر قابل حل"),
    )

    ISSUE_STATUS = (
        ("pending", "در حال اقدام"),
        ("rejected", "مرتفع شده"),
        ("approved", "مرتفع نشده")
    )

    project_issue_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project,to_field="project_id", on_delete=models.CASCADE)
    category = models.ForeignKey(IssueCategory,to_field="issue_category_id" ,on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)
    document = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="created_project_issues")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    type = models.CharField(choices=ISSUE_TYPE, max_length=50)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(choices=ISSUE_STATUS, max_length=50)
    responisble = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="responsible_project_issues")

    def __str__(self) -> str:
        return self.category + ' ' + self.project.title
    

class TaskIssue(models.Model):
    ISSUE_TYPE = (
        ("solvable", "قابل حل"),
        ("unsolvable", "غیر قابل حل"),
    )

    ISSUE_STATUS = (
        ("pending", "در حال اقدام"),
        ("rejected", "مرتفع شده"),
        ("approved", "مرتفع نشده")
    )

    task_issue_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task,to_field="task_id", on_delete=models.CASCADE)
    category = models.ForeignKey(IssueCategory,to_field="issue_category_id" ,on_delete=models.DO_NOTHING)
    description = models.TextField()
    document = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="created_task_issues")
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    type = models.CharField(choices=ISSUE_TYPE, max_length=50)
    deadline = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(choices=ISSUE_STATUS, max_length=50)
    responisble = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="responsible_task_issues")

    def __str__(self) -> str:
        return self.category + ' ' + self.task.title
    