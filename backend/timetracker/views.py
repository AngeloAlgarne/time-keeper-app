from datetime import datetime, timezone

from django.forms.models import model_to_dict
from django.db import models
from django.http import HttpResponse
from rest_framework import views, response, serializers, generics

from .models import Project, Timer, OnholdTimer
from .serializer import (
    ProjectSerializer, 
    TimerSerializer, 
    OnholdTimerSerializer
)


class BaseAPIViewClass(views.APIView):
    '''
    A template class for the main api views.\n
    Post method needs to be overriden. Variables `model_class` and `serializer_class` are required.\n
    Override the method `get_parse_objects` to customize object values to return.
    '''
    model_class:models.Model = None
    serializer_class:serializers.ModelSerializer = None

    
    def get_parse_objects(self, queryset:models.QuerySet) -> models.QuerySet:
        '''
        Transform the queryset into a dictionary for get requests.\n
        Override this function to customize what values to return for response objects.
        '''
        return [model_to_dict(record) for record in queryset]
    
    
    def get(self, request):
        '''
        Process GET requests
        '''
        if not self.model_class:
            raise Exception('Implementation Error: include a model to this APIView.')
        
        queryset = self.model_class.objects.all()
        output = self.get_parse_objects(queryset)
        
        return response.Response(output)
    
    
    def post(self, request):
        '''
        Process POST requests
        '''
        if not self.model_class:
            raise Exception('Implementation Error: include a model to this APIView.')
        
        serializer:serializers.ModelSerializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data)
        

class ProjectAPIView(BaseAPIViewClass):
    model_class = Project
    serializer_class = ProjectSerializer
    
    def get_parse_objects(self, queryset) -> models.QuerySet:
        '''
        This overridden function has filtering: 
        only include projects with no timer in the queryset. 
        '''
        queryset = queryset.filter(timer__isnull=True)
        return [{**model_to_dict(record), "created_at": record.created_at}
            for record in queryset]


class TimerAPIView(BaseAPIViewClass):
    model_class = Timer
    serializer_class = TimerSerializer
    
    def get_parse_objects(self, queryset) -> models.QuerySet:
        output = []
        for record in queryset:
            record_as_dict = model_to_dict(record)
            record_as_dict.update({
                "onhold": bool(record.active_onhold),
                "created_at": record.created_at,
                "completed_at": record.completed_at,
                'project_name': record.project.name,
                'project_description': record.project.description,
                'project_created_at': record.project.created_at,
            })
            output.append(record_as_dict)
        return output
        

class OnholdTimerAPIView(BaseAPIViewClass):
    '''
    This APIView class is unused. For scalability purposes, this is good.
    But for this first version, a simpler process flow is needed. 
    '''
    model_class = OnholdTimer
    serializer_class = OnholdTimerSerializer
    
    def get_parse_objects(self) -> models.QuerySet:
        queryset = Timer.objects.filter(active_onhold__isnull=False)        
        output = []
        for record in queryset:
            record_as_dict = model_to_dict(record)
            record_as_dict.update({
                'duration_ms': record.main_timer.duration_ms,
                'created_at': record.main_timer.created_at,
                'project_name': record.main_timer.project.name,
                'project_description': record.main_timer.project.description,
                'project_created_at': record.main_timer.project.created_at,
            })
            output.append(record_as_dict)
        return output


class CompletedTimerAPIView(TimerAPIView):
    '''
    Inherits TimerAPIView and recalls `get_parse_objects` through `super()`.
    This is just to add a filter for all completed projects.
    '''
    def get_parse_objects(self, queryset:models.QuerySet) -> models.QuerySet:
        queryset = queryset.filter(completed_at__isnull=False)
        return super().get_parse_objects(queryset)
    
    def put(self, request):
        '''
        Process PUT requests
        '''
        
        # Fetch timer
        try:
            timer = Timer.objects.get(id=request.data.get('timer'))
        except Timer.DoesNotExist:
            return HttpResponse(status=500)
        
        # Process the completion data
        # processed_data = {**request.data}
        # processed_data.pop('timer')
        
        date_now = datetime.now(timezone.utc)
        timer.duration_ms = (date_now - timer.created_at).seconds
        timer.completed_at = date_now
        
        timer.save(update_fields=['duration_ms', 'completed_at'])
        
        serializer = self.serializer_class(timer)
        return response.Response(serializer.data)