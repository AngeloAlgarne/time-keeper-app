# from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db import models
from rest_framework import views, response

from .models import Project, Timer, OnholdTimer
from .serializer import (
    ProjectSerializer, 
    TimerSerializer, 
    OnholdTimerSerializer
)


class BaseAPIClass(views.APIView):
    
    model_class:models.Model = None

    
    def get_parse_objects(self, queryset:models.QuerySet) -> models.QuerySet:
        '''
        Transform the queryset into a dictionary for get requests
        '''
        return [model_to_dict(record) for record in queryset]
    
    
    def get(self, request):
        if not self.model_class:
            raise Exception('Implementation Error: include a model to this APIView.')
        
        queryset = self.model_class.objects.all()
        output = self.get_parse_objects(queryset)
        
        return response.Response(output)
    
    
    def post(self, request):
        raise NotImplementedError('Post method called without proper implementation. '\
            +'It is recommended to include a "serializer_class" instance variable.')
        

class ProjectAPIView(BaseAPIClass):
    model_class = Project
    serializer_class = ProjectSerializer
    
    # Override
    def get_parse_objects(self, queryset) -> models.QuerySet:
        return [
            {**model_to_dict(record), 
             "created_at": record.created_at,}
            for record in queryset
        ]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data)


class TimerAPIView(BaseAPIClass):
    model_class = Timer
    serializer_class = TimerSerializer
    
    # Override
    def get_parse_objects(self, queryset) -> models.QuerySet:
        output = []
        for record in queryset:
            record_as_dict = {}
            record_as_dict.update(model_to_dict(record))
            record_as_dict.update({
                'project_name': record.project.name,
                'project_description': record.project.description,
                'project_created_at': record.project.created_at,
            })
            output.append(record_as_dict)
        return output
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data)
