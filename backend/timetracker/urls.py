from django.urls import path
from .views import (
    ProjectAPIView,
    TimerAPIView,
    OnholdTimerAPIView,
    UpdateProjectAPIView,
)

urlpatterns = [
    path('projects', ProjectAPIView.as_view(), name='projects'),
    path('projects/update', UpdateProjectAPIView.as_view(), name='projects.update'),
    path('timers', TimerAPIView.as_view(), name='timers'),
    path('onhold', OnholdTimerAPIView.as_view(), name='onhold'),
]