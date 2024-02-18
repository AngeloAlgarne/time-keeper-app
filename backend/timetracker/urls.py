from django.urls import path
from .views import (
    ProjectAPIView,
    TimerAPIView,
    OnholdTimerAPIView,
    CompletedTimerAPIView,
    LoginAPIView,
    SignUpAPIView
)

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('signup', SignUpAPIView.as_view(), name='signup'),
    path('projects', ProjectAPIView.as_view(), name='projects'),
    path('timers', TimerAPIView.as_view(), name='timers'),
    path('onhold', OnholdTimerAPIView.as_view(), name='onhold'),
    path('completed', CompletedTimerAPIView.as_view(), name='completed'),
]