from datetime import datetime, timezone

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db import models
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import views, response, serializers, status
from rest_framework.authtoken.models import Token

from .models import Project, Timer, OnholdTimer
from .serializer import (
    ProjectSerializer, 
    TimerSerializer, 
    UserSerializer,
)


class LoginAPIView(views.APIView):
    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return response.Response("missing user", status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return response.Response({'token': token.key, 'user': serializer.data})


class SignUpAPIView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return response.Response({'token': token.key, 'user': serializer.data})
        return response.Response(serializer.errors, status=status.HTTP_200_OK)
    

class BaseAPIViewClass(LoginRequiredMixin, views.APIView):
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
        return response.Response(serializer.errors, status=status.HTTP_200_OK)
        

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
        queryset = queryset.filter(completed_at__isnull=True)
        
        output = []
        for record in queryset:
            record_as_dict = model_to_dict(record) # all other field values
            record_as_dict.update({
                # "onhold": bool(record.active_onhold),
                "duration_seconds": record.compute_duration_seconds(),
                "created_at": record.created_at,
                "completed_at": record.completed_at,
                'project_name': record.project.name,
                'project_description': record.project.description,
                'project_created_at': record.project.created_at,
            })
            output.append(record_as_dict)
        return output
        

class OnholdTimerAPIView(BaseAPIViewClass):
    pass
    '''
    This APIView class is unused. For scalability purposes, this is good.
    But for this first version, a simpler process flow is needed. 
    '''
    # model_class = OnholdTimer
    # serializer_class = OnholdTimerSerializer
    
    # def get_parse_objects(self) -> models.QuerySet:
    #     queryset = Timer.objects.filter(active_onhold__isnull=False)        
    #     output = []
    #     for record in queryset:
    #         record_as_dict = model_to_dict(record)
    #         record_as_dict.update({
    #             'duration_seconds': record.main_timer.duration_seconds,
    #             'created_at': record.main_timer.created_at,
    #             'project_name': record.main_timer.project.name,
    #             'project_description': record.main_timer.project.description,
    #             'project_created_at': record.main_timer.project.created_at,
    #         })
    #         output.append(record_as_dict)
    #     return output


class CompletedTimerAPIView(BaseAPIViewClass):
    model_class = Timer
    serializer_class = TimerSerializer
    
    def get_parse_objects(self, queryset) -> models.QuerySet:
        queryset = queryset.filter(completed_at__isnull=False)
        
        output = []
        for record in queryset:
            record_as_dict = model_to_dict(record)
            print(record.compute_duration_seconds())
            record_as_dict.update({
                # "onhold": bool(record.active_onhold),
                "duration_seconds": record.compute_duration_seconds(),
                "created_at": record.created_at,
                "completed_at": record.completed_at,
                'project_name': record.project.name,
                'project_description': record.project.description,
                'project_created_at': record.project.created_at,
            })
            output.append(record_as_dict)
        return output
    
    def put(self, request):
        '''
        Process PUT requests
        '''
        
        # Fetch timer
        try:
            timer = Timer.objects.get(id=request.data.get('timer'))
        except Timer.DoesNotExist:
            return HttpResponse(status=500)
        
        timer.completed_at = datetime.now(timezone.utc)
        timer.duration_seconds = timer.compute_duration_seconds()
        
        timer.save(update_fields=['duration_seconds', 'completed_at'])
        
        serializer = self.serializer_class(timer)
        return response.Response(serializer.data)