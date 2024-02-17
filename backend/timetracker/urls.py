from django.urls import path
from .views import (
    ProjectAPIView,
    TimerAPIView,
    OnholdTimerAPIView
)

urlpatterns = [
    path('projects', ProjectAPIView.as_view(), name='projects'),
    path('timers', TimerAPIView.as_view(), name='timers'),
    path('onhold', OnholdTimerAPIView.as_view(), name='onhold'),
]