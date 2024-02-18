from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Timer(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Unnecessary without OnholdTimer
    date_ref = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Date Reference')
    active_onhold = models.ForeignKey('OnholdTimer', on_delete=models.PROTECT, null=True, blank=True)
    duration_seconds = models.BigIntegerField(default=0, blank=True)
    
    def compute_duration_seconds(self):
        date_now = timezone.now()
        return (date_now - self.created_at).total_seconds()
    

class OnholdTimer(models.Model):
    main_timer = models.ForeignKey(Timer, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)