import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .models import User

import pyotp

# Create your views here.

class RegisterView(APIView):
 serializer_class = UserSerializer
 queryset = User.objects.all()

 def post(self, request):
  """
  Register View
  """
  serializer = self.serializer_class(data = request.data)
  if serializer.is_valid():
   serializer.save()
   return Response({ "user_id": serializer.data['id'], "status": "Registration successful", "message": "Registered successfully, please login" }, 
    status=status.HTTP_201_CREATED)
  else:
   return Response({ "status": "Registration failed", "message": str(serializer.errors) }, 
    status=status.HTTP_400_BAD_REQUEST)
  
# auth_app/views.py
class Set2FAView(APIView):
    """
    Get the image of the QR Code
    """
    def post(self, request):
        user = self.getUserService(request)
        if user == None:
            return Response({"status": "fail", "message": f"No user with the corresponding username and password exists" }, status=status.HTTP_404_NOT_FOUND)

        qr_code = self.getQRCodeService(user)
        return Response({"qr_code": qr_code})

    def getUserService(self, request):
        """
        Get the user with a particular user_id
        """
        try:
            data = request.data
            user_id = data.get('user_id', None)
            user = User.objects.get(id = user_id)
            return user
        except:
            return None

    def getQRCodeService(self, user):
        """
        Generate the QR Code image, save the otp_base32 for the user
        """
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
        name=user.username.lower(), issuer_name="localhost.com")

        user.otp_base32 = otp_base32
        user.save()
        qr_code = requests.post('http://localhost:8001/get-qr-code/', json = {'otp_auth_url': otp_auth_url}).json()

        return qr_code['qr_code_link']
    

# class QRCode(APIView):
#    def 