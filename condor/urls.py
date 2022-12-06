from django.urls import path
from condor import views

urlpatterns = [
    path('ec2list', views.Ec2ListView.as_view()),
    path('ec2az', views.Ec2AvailZView.as_view()),
    path('ec2start', views.Ec2StartView.as_view()),
    path('ec2ar', views.Ec2AvailRView.as_view()),
    path('ec2stop', views.Ec2StopView.as_view()),
    path('ec2create', views.Ec2CreateView.as_view()),
    path('ec2reboot', views.Ec2RebootView.as_view()),
    path('ec2listimage', views.Ec2ListImageView.as_view()),

    path('ec2ssm', views.Ec2SSMView.as_view()),
    path('ec2ce', views.Ec2CEView.as_view())
]