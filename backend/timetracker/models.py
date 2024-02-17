from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Timer(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    date_ref = models.DateTimeField(verbose_name='Date Reference')
    active_onhold = models.ForeignKey('OnholdTimer', null=True, blank=True)
    duration_ms = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class OnholdTimer(models.Model):
    timer = models.ForeignKey(Timer, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)