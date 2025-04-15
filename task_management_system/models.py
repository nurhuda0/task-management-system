from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    class Meta:
        app_label = 'task_management_system'  # Add this
        # Optional: set db_table if you want custom table name
        db_table = 'custom_users'
    
    ROLES = (
        ('admin', 'Admin'),
        ('user', 'Regular User'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    due_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_tasks', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_attachments/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Attachment for {self.task.title}"