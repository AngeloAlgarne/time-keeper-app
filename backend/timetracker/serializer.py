from rest_framework import serializers
from .models import Project, Timer, OnholdTimer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = '__all__'
        
class OnholdTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnholdTimer
        fields = '__all__'