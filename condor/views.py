from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import boto3
from django.conf import settings
from botocore.exceptions import ClientError

ec2client = boto3.client('ec2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)


# 1
class Ec2ListView(APIView):
    def get(self, request):
        data = {'ec2': []}

        response = ec2client.describe_instances()

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                data['ec2'].append({
                    "[id]": instance["InstanceId"],
                    "[AMI]": instance["ImageId"],
                    "[type]": instance["InstanceType"],
                    "[state]": instance["State"]["Name"],
                    "[monitoring state]": instance["Monitoring"]
                })

        return JsonResponse(data)


# 2
class Ec2AvailZView(APIView):
    def get(self, request):
        data = {'zone': []}
        response = ec2client.describe_availability_zones()
        for zone in response['AvailabilityZones']:
            data['zone'].append({
                "[id]": zone["ZoneId"],
                "[region]": zone["RegionName"],
                "[zone]": zone["ZoneName"],
            })
        return JsonResponse(data)


# 3
class Ec2StartView(APIView):
    def post(self, request):
        instance_id = request.data["instance_id"]
        try:
            ec2client.start_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

            # Dry run succeeded, run start_instances without dryrun
        try:
            response = ec2client.start_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
        return Response({
            'message': instance_id + ' start'
        })


# 4
class Ec2AvailRView(APIView):
    def get(self, request):
        data = {'zone': []}
        for region in ec2client.describe_regions()['Regions']:
            data['zone'].append({
                "[region]": region['RegionName'],
                "[endpoint]": region['Endpoint']
            })
        return JsonResponse(data)


# 5
class Ec2StopView(APIView):
    def post(self, request):
        instance_id = request.data["instance_id"]
        try:
            ec2client.stop_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                raise

            # Dry run succeeded, call stop_instances without dryrun
        try:
            response = ec2client.stop_instances(InstanceIds=[instance_id], DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
        return Response({
            'message': instance_id + ' stop'
        })


# 6
class Ec2CreateView(APIView):
    def post(self, request):
        image_id = request.data["image_id"]
        ec2 = boto3.resource('ec2', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType='t2.micro', )
        return Response({
            'message': image_id + ' create'
        })


# 7
class Ec2RebootView(APIView):
    def post(self, request):
        from botocore.exceptions import ClientError
        instance_id = request.data["instance_id"]

        try:
            ec2client.reboot_instances(InstanceIds=[instance_id], DryRun=True)
        except ClientError as e:
            if 'DryRunOperation' not in str(e):
                print("You don't have permission to reboot instances.")
                raise

        try:
            response = ec2client.reboot_instances(InstanceIds=[instance_id], DryRun=False)
            print('Success', response)
        except ClientError as e:
            print('Error', e)
        return Response({
            'message': instance_id + ' restart'
        })


# 8
class Ec2ListImageView(APIView):
    def get(self, request):
        data = {'image': []}
        images = ec2client.describe_images(Owners=['self'])
        for image in images['Images']:
            data['image'].append({
                "[ImageId]": image['ImageId'],
                "[Name]": image['Name'],
                "[Owner]": image['OwnerId']
            })
        return JsonResponse(data)


# 11
class Ec2SSMView(APIView):
    def post(self, request):
        ssm_client = boto3.client('ssm', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        instance_id = request.data["instance_id"]
        command = request.data["command"]

        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': [command]}, )

        import time
        time.sleep(1)

        command_id = response['Command']['CommandId']
        output = ssm_client.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        return Response({
            'message': output['StandardOutputContent']
        })


# 99
class Ec2QuitView(APIView):
    def get(self, request):
        return JsonResponse()
