from django.urls import path
from . import views

urlpatterns = [

    path('lista_usuarios/', views.lista_usuario, name='lista_usuario'),
    path('ver_usuario/<int:id>', views.ver_usuario, name='ver_usuario'),


    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
    path('reject_friend_request/', views.reject_friend_request, name='reject_friend_request'),
    path('friends/', views.friend_list, name='friend_list'),

]