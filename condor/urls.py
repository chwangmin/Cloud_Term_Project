from django.urls import path
from condor import views

urlpatterns = [
    path('ec2list/', views.Ec2ListView.as_view()),
    path('ec2start/', views.Ec2StartView.as_view()),
    path('ec2stop/', views.Ec2StopView.as_view())
]