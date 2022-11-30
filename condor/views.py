from rest_framework.views import APIView
import boto3

from rest_framework.response import Response
from django.conf import settings

class Ec2ListView(APIView):
    def get(self, request):
        ec2 = boto3.resource('ec2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        for instance in ec2.instances.all():
            print(instance.id)

        return Response({'good'}, status=200)  # 프론트로 전달