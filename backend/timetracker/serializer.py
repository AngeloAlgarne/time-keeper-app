from rest_framework import serializers
from .models import Project, Timer, OnholdTimer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ['project']
        
class OnholdTimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnholdTimer
        exclude = ['end']