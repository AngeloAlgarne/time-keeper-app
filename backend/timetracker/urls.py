from django.urls import path
from .views import (
    ProjectAPIView,
    TimerAPIView
)

urlpatterns = [
    path('projects', ProjectAPIView.as_view(), name='projects'),
    path('timers', TimerAPIView.as_view(), name='timers'),
]