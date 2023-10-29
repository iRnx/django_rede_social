from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile, FriendRequest
from django.contrib.auth.models import User


def lista_usuario(request):
    usuarios = UserProfile.objects.all()
    return render(request, 'lista_usuarios.html', {'usuarios': usuarios})


def ver_usuario(request, id):
    usuario = get_object_or_404(UserProfile, id=id)
    solicitacoes = FriendRequest.objects.filter(to_user=usuario)
    
    return render(request, 'ver_usuario.html', {'usuario': usuario, 'solicitacoes': solicitacoes})


def send_friend_request(request, username):

    recipient = get_object_or_404(User, username=username)
    sender_profile = UserProfile.objects.get(user=request.user)
    recipient_profile = UserProfile.objects.get(user=recipient)

    # if recipient_profile not in sender_profile.friends.all():
      
    # Verifica se uma solicitação de amizade já existe
    if not FriendRequest.objects.filter(from_user=sender_profile, to_user=recipient_profile).exists():
        friend_request = FriendRequest(from_user=sender_profile, to_user=recipient_profile)
        friend_request.save()

    return HttpResponse("Solicitação de amizade já enviada ou já são amigos.")


def accept_friend_request(request):
    
    user_profile = UserProfile.objects.filter(user=request.user).first()
    friend_request = FriendRequest.objects.filter(to_user=user_profile).first()
    
    if user_profile == friend_request.to_user:
        friend_request.accepted = True
        friend_request.save()
        user_profile.friends.add(friend_request.from_user)
        user_profile.save()
        
    return render(request, 'friend_requests.html')

# Parei aqui #
def reject_friend_request(request):
    # friend_request = get_object_or_404(FriendRequest, id=request_id)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    friend_request = FriendRequest.objects.filter(to_user=user_profile).first()
    if friend_request.to_user == request.user.userprofile:
        friend_request.delete()
    return redirect('friend_requests')


def friend_list(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    friends = user_profile.friends.all()
    
    return render(request, 'friend_list.html', {'friends': friends, 'user_profile': user_profile})