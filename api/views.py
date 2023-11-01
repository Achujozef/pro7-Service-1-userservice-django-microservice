from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from .serializer import UserCreateSerializer, UserSerializer, UserDocumentSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import jwt
from rest_framework import generics
from .producer import publish



class RegisterUser(APIView):
    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.create(serializer.validated_data)

        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class RetrieveUserView(APIView):

    def get(self, request):
        queryset = UserAccount.objects.filter(is_staff = False).all().order_by('-date_joined')
        serialized = UserSerializer(queryset, many=True)

        return Response(serialized.data)



class BlacklistTokenUpdateView(APIView):
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class GetUser(APIView):
    def get(self,request, id):
        try:
            user = UserAccount.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)        
        except UserAccount.DoesNotExist:
            raise Http404

class ProfileUpdateView(APIView):
    def post(self, request ,id):
        user = UserAccount.objects.get(id=id)
        userData =  UserSerializer(instance=user, data=request.data, partial=True)
        if userData.is_valid():
            userData.save()
            return Response(userData.data, status=status.HTTP_200_OK)
        return Response(400)
     
class UserSearchView(APIView):
    def get(self, request):
        keyword = request.GET.get('query')
        print(keyword)
        users = UserAccount.objects.filter(Q(name__icontains = keyword) | Q(phonenumber__icontains = keyword) , is_staff = False)
        serialized = UserSerializer(users, many=True)
        return Response(serialized.data)

class usertestView(APIView):
    def get(self,request):
        print('Njan Rabbit Useril  Ethiyalloooo')
        publish()

class UserDocumentViewSet(viewsets.ViewSet):
    def list (self, request):
        queryset = UserDocument.objects.all()
        serializer = UserDocumentSerializer(queryset,many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer =UserDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            user_document= UserDocument.objects.get(pk=pk)
        except UserDocument.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=UserDocumentSerializer(user_document)
        return Response(serializer.data)
    def update (self, request, pk=None):
        try:
            user_document= UserDocument.objects.get(pk=pk)
        except UserDocument.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer=UserDocumentSerializer(user_document,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk=None):
        try:
            user_document= UserDocument.objects.get(pk=pk)

        except UserDocument.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user_document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FollowDoctorView(APIView):    #http://localhost:8000/api/follow-doctor/2/?user_id=1
    def post(self, request, doctor_id):
        #user = request.user  # Assuming you are using authentication
        user_id = request.query_params.get('user_id')
        user=UserAccount.objects.get(pk=user_id)
        try:
            Follower.objects.get(user=user, doctor_id=doctor_id).delete()
            return Response({'message': 'Unfollowed'}, status=status.HTTP_200_OK)
        except Follower.DoesNotExist:
            Follower.objects.create(user=user, doctor_id=doctor_id)
            return Response({'message': 'Followed'}, status=status.HTTP_201_CREATED)
    
