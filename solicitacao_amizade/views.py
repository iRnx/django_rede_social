from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import UserProfile, FriendRequest
from django.contrib.auth.models import User
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='/auth/login/')
def lista_usuario(request):
    usuarios = UserProfile.objects.all()
    return render(request, 'solicitacao_amizade/lista_usuarios.html', {'usuarios': usuarios})


@login_required(login_url='/auth/login/')
def ver_usuario(request, id):

    usuario_id = get_object_or_404(UserProfile, id=id)
    usuario_requisicao = UserProfile.objects.filter(user=request.user).first()
   
    solicitacoes = FriendRequest.objects.filter(to_user=usuario_requisicao)
    todas_solicitacoes = solicitacoes.count()
    
    recipient = get_object_or_404(User, username=usuario_id.user)

    amigos = usuario_requisicao.friends.all()
    is_friend = False
        
    for amigo in amigos:
        if amigo.user.username == recipient.username:
            is_friend = True
            break

    context = {
        'usuario': usuario_id,
        'solicitacoes': solicitacoes,
        'recipient': recipient,
        'is_friend': is_friend,
        'sender_profile': usuario_requisicao,
        'todas_solicitacoes': todas_solicitacoes,
 
        }

    return render(request, 'solicitacao_amizade/ver_usuario.html', context)
    

@login_required(login_url='/auth/login/')
def send_friend_request(request, username):

    recipient = get_object_or_404(User, username=username) # renan é o perfil onde estou
    sender_profile = UserProfile.objects.get(user=request.user) # teste o cara q esta logado
    recipient_profile = UserProfile.objects.get(user=recipient) # pegando o renan no userprofile.

    # Verifica se uma solicitação de amizade já existe
    verifica_solicitacao_existe = FriendRequest.objects.filter(from_user=sender_profile, to_user=recipient_profile).exists()
    if not verifica_solicitacao_existe:
        friend_request = FriendRequest(from_user=sender_profile, to_user=recipient_profile)
        friend_request.save()
        messages.success(request, f'Solicitação enviada para "{friend_request.to_user}"')

    return redirect(reverse('ver_usuario', kwargs={'id': sender_profile.pk}))


@login_required(login_url='/auth/login/')
def accept_friend_request(request):
    
    user_profile = UserProfile.objects.filter(user=request.user).first()
    friend_request = FriendRequest.objects.filter(to_user=user_profile).first()
    
    if user_profile == friend_request.to_user:
        friend_request.accepted = True
        friend_request.save()

        user_profile.friends.add(friend_request.from_user)
        user_profile.save()
        # messages.success(request, f'Solicitação enviada para {friend_request.to_user}')

        FriendRequest.objects.filter(to_user=user_profile, accepted=True).delete()

    return redirect(reverse('ver_usuario', kwargs={'id': user_profile.pk}))


@login_required(login_url='/auth/login/')
def reject_friend_request(request, username):
    # friend_request = get_object_or_404(FriendRequest, id=request_id)
    user_profile = UserProfile.objects.filter(user=request.user).first()
    friend_request = FriendRequest.objects.filter(to_user=user_profile).first()
    if friend_request.to_user == user_profile:
        friend_request.delete()
    return redirect(reverse('ver_usuario', kwargs={'id': user_profile.pk}))


@login_required(login_url='/auth/login/')
def desfazer_amizade(request, id):
    perfil_logado = UserProfile.objects.filter(user=request.user).first()  # Perfil do usuário logado
    perfil_amigo = get_object_or_404(UserProfile, id=id)  # Perfil do amigo a ser desfeito

    # Verifique se perfil_amigo está na lista de amigos de perfil_logado
    if perfil_amigo in perfil_logado.friends.all():
        perfil_logado.friends.remove(perfil_amigo)  # Remove perfil_amigo da lista de amigos de perfil_logado
        perfil_amigo.friends.remove(perfil_logado)  # Remove perfil_logado da lista de amigos de perfil_amigo

        # Você pode adicionar qualquer lógica adicional aqui, como notificar os usuários sobre a ação de desfazer amizade

    return redirect('ver_usuario', id=id)  # Redireciona de volta para a visualização do usuário


@login_required(login_url='/auth/login/')
def friend_list(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    friends = user_profile.friends.all()

    return render(request, 'solicitacao_amizade/friend_list.html', {'friends': friends, 'user_profile': user_profile})
