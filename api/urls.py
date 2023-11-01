from django.contrib import admin
from django.urls import path
from .views import *
userdocument_list = UserDocumentViewSet.as_view({'get': 'list', 'post': 'create'})
userdocument_detail = UserDocumentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})
urlpatterns = [
    path('register/',RegisterUser.as_view()),
    path('me/', RetrieveUserView.as_view()),
    path('user/<id>', GetUser.as_view()),
    path('update/user/<id>', ProfileUpdateView.as_view()),
    path('admin/search/',UserSearchView.as_view()),
    path('userdocuments/', userdocument_list, name='userdocument-list'),
    path('userdocuments/<int:pk>/', userdocument_detail, name='userdocument-detail'),
    path('follow-doctor/<int:doctor_id>/', FollowDoctorView.as_view(), name='follow-doctor'),


]