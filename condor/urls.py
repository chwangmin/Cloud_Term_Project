from django.urls import path
from condor import views

urlpatterns = [
    path('ec2list/', views.Ec2ListView.as_view())
]