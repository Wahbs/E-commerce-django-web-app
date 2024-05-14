from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import Authentification.models
import Discussion.models
from Discussion.forms import *
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User as UserModel
from django.db.models import Q
import json, datetime
from django.core import serializers
from Discussion.forms import *


# Create your views here.
@login_required
def home_chat(request):
    # User = User
    # users = User.objects.all()
    chats = {}
    conversations = chatMessages.objects.filter(Q(user_from=request.user.id) | Q(user_to=request.user.id))
    discussion = []
    users = []
    produits = []
    for conv in conversations:
        if conv.produit:
            if conv.produit not in produits:
                produits.append(conv.produit)
            if conv.user_from != request.user:
                users.append(conv.user_from)
            if conv.user_to != request.user:
                users.append(conv.user_to)

    discussions = []
    for prod in produits:
        for conv in conversations:
            if conv.produit == prod:
                dict = {}
                if conv.user_to != request.user:
                    dict['user'] = conv.user_to
                    dict['produit'] = conv.produit
                    dict['photo'] = Photo.objects.filter(produit_id=conv.produit)[0]
                    dict['NonLu'] = chatMessages.objects.filter(Q(user_to=request.user.id,
                                                             produit=conv.produit, statut=False)).count()
                    msg = chatMessages.objects.filter(
                        Q(user_from=conv.user_from, user_to=conv.user_to, produit=conv.produit) |
                        Q(user_from=conv.user_to, user_to=conv.user_from, produit=conv.produit)
                    )
                    msg = msg.order_by('date_created')
                    if msg.count() > 0:
                        date = datetime.date
                        today = date.strftime(date.today(), '%d/%m/%Y')
                        dernier_msg = msg.reverse()[0]
                        date_msg = date.strftime(dernier_msg.date_created, '%d/%m/%Y')
                        dict['dernier_msg'] = msg.reverse()[0]

                        if date_msg == today:
                            dict['date'] = date.strftime(dernier_msg.date_created, '%H:%M')
                        elif int(date_msg.split('/')[0]) == int(today.split('/')[0]) - 1:
                            dict['date'] = datetime.date.strftime(dernier_msg.date_created, 'hier %H:%M')
                        elif int(date_msg.split('/')[0]) >= int(today.split('/')[0]) - 6:
                            dict['date'] = datetime.date.strftime(dernier_msg.date_created, '%a %H:%M')
                        else:
                            dict['date'] = date_msg
                    else:
                        dict['dernier_msg'] = ''
                if conv.user_from != request.user:
                    dict['user'] = conv.user_from
                    dict['produit'] = conv.produit
                    dict['photo'] = Photo.objects.filter(produit_id=conv.produit)[0]
                    dict['NonLu'] = chatMessages.objects.filter(Q(user_to=request.user.id,
                                                             produit=conv.produit, statut=False)).count()
                    msg = chatMessages.objects.filter(
                        Q(user_from=conv.user_from, user_to=conv.user_to, produit=conv.produit) |
                        Q(user_from=conv.user_to, user_to=conv.user_from, produit=conv.produit)
                    )
                    msg = msg.order_by('date_created')
                    if msg.count() > 0:
                        dict['dernier_msg'] = msg.reverse()[0]
                    else:
                        dict['dernier_msg'] = ''

                discussion.append(conv)
                discussions.append(dict)
                break

    if request.method == 'GET' and 'u' in request.GET:
        # chats = chatMessages.objects.filter(Q(user_from=request.user.id & user_to=request.GET['u']) | Q(user_from=request.GET['u'] & user_to=request.user.id))
        req = request.GET['u'].split('/')
        client = req[0]
        produit = req[1]
        chats = chatMessages.objects.filter(
            Q(user_from=request.user.id, user_to=client, produit=produit) |
            Q(user_from=client, user_to=request.user.id, produit=produit))
        chats = chats.order_by('date_created')
        sms = chatMessages.objects.filter(Q(user_to=request.user.id, user_from=client, produit=produit))
        for chat in sms:
            chat.statut = True
            chat.save()

    elif request.method == 'POST' and 'u' in request.POST:
        req = request.POST['u'].split('/')
        client = req[0]
        produit = req[1]
        chats = chatMessages.objects.filter(
            Q(user_from=request.user.id, user_to=client, produit=produit) | Q(user_from=client, user_to=request.user.id,
                                                                              produit=produit))
        chats = chats.order_by('date_created')
        sms = chatMessages.objects.filter(Q(user_to=request.user.id, user_from=client, produit=produit))
        for chat in sms:
            chat.statut = True
            chat.save()

    context = {
        "page": "home_chat",
        "users": users,
        "discussion": discussion,
        "discussions": discussions,
        "chats": chats,
        "chat_id": int(req[0] if request.method == 'GET' and 'u' in request.GET else 0),
        "produit_id": int(req[1] if request.method == 'GET' and 'u' in request.GET else 0),
    }
    return render(request, "Discussion/home_chat.html", context)


def actualise_chat(request, chat_id, prod_id):
    User = Authentification.models.User
    users = User.objects.all()
    chats = chatMessages.objects.filter(
        Q(user_from=request.user.id, user_to=chat_id, produit_id=prod_id) |
        Q(user_from=chat_id, user_to=request.user.id, produit_id=prod_id)
    )
    chats = chats.order_by('date_created')
    Msg_non_lu = []
    for u in users:
        SMS_non_lu = {}
        SMS_non_lu['user'] = u
        SMS_non_lu['nombre'] = chatMessages.objects.filter(Q(user_to=request.user.id, user_from=u, produit_id=prod_id, statut=False)).count()
        Msg_non_lu.append(SMS_non_lu)

    context = {
        "page": "home_chat",
        "users": users,
        "chats": chats,
        "chat_id": chat_id,
        "Msg_non_lu": Msg_non_lu,
    }
    return render(request, "Discussion/message.html", context)


def actualise_list_discussion(request, chat_id, prod_id):
    conversations = chatMessages.objects.filter(Q(user_from=request.user.id) | Q(user_to=request.user.id))
    discussion = []
    users = []
    produits = []
    for conv in conversations:
        if conv.produit:
            if conv.produit not in produits:
                produits.append(conv.produit)
            if conv.user_from != request.user:
                users.append(conv.user_from)
            if conv.user_to != request.user:
                users.append(conv.user_to)
    discussions = []
    for prod in produits:
        for conv in conversations:
            if conv.produit == prod:
                dict = {}
                if conv.user_to != request.user:
                    dict['user'] = conv.user_to
                    dict['produit'] = conv.produit
                    dict['photo'] = Photo.objects.filter(produit_id=conv.produit)[0]
                    dict['NonLu'] = chatMessages.objects.filter(Q(user_to=request.user.id,
                                                                  produit=conv.produit, statut=False)).count()
                    msg = chatMessages.objects.filter(
                        Q(user_from=conv.user_from, user_to=conv.user_to, produit=conv.produit) |
                        Q(user_from=conv.user_to, user_to=conv.user_from, produit=conv.produit)
                    )
                    msg = msg.order_by('date_created')
                    if msg.count() > 0:
                        date = datetime.date
                        today = date.strftime(date.today(), '%d/%m/%Y')
                        dernier_msg = msg.reverse()[0]
                        date_msg = date.strftime(dernier_msg.date_created, '%d/%m/%Y')
                        dict['dernier_msg'] = msg.reverse()[0]

                        if date_msg == today:
                            dict['date'] = date.strftime(dernier_msg.date_created, '%H:%M')
                        elif int(date_msg.split('/')[0]) == int(today.split('/')[0]) - 1:
                            dict['date'] = datetime.date.strftime(dernier_msg.date_created, 'hier %H:%M')
                        elif int(date_msg.split('/')[0]) >= int(today.split('/')[0]) - 6:
                            dict['date'] = datetime.date.strftime(dernier_msg.date_created, '%a %H:%M')
                        else:
                            dict['date'] = date_msg
                    else:
                        dict['dernier_msg'] = ''
                if conv.user_from != request.user:
                    dict['user'] = conv.user_from
                    dict['produit'] = conv.produit
                    dict['photo'] = Photo.objects.filter(produit_id=conv.produit)[0]
                    dict['NonLu'] = chatMessages.objects.filter(Q(user_to=request.user.id,
                                                                  produit=conv.produit, statut=False)).count()
                    msg = chatMessages.objects.filter(
                        Q(user_from=conv.user_from, user_to=conv.user_to, produit=conv.produit) |
                        Q(user_from=conv.user_to, user_to=conv.user_from, produit=conv.produit)
                    )
                    msg = msg.order_by('date_created')
                    if msg.count() > 0:
                        dict['dernier_msg'] = msg.reverse()[0]
                    else:
                        dict['dernier_msg'] = ''
                discussion.append(conv)
                discussions.append(dict)
                break
    context = {
        "users": users,
        "discussion": discussion,
        "discussions": discussions,
        "chat_id": chat_id,
        "produit_id": prod_id,
    }
    return render(request, "Discussion/list_discussion.html", context)


@login_required
def send_chat(request):
    if request.method == 'GET':
        u_from = Authentification.models.User.objects.get(id=request.GET['user_from'])
        u_to = Authentification.models.User.objects.get(id=request.GET['user_to'])
        msg = request.GET['message']
        if msg != '':
            if request.GET['produit']:
                chatMessages.objects.create(user_from=u_from, user_to=u_to, message=msg, produit_id=request.GET['produit'],
                                            date_created=datetime.datetime.now())
            else:
                chatMessages.objects.create(user_from=u_from, user_to=u_to, message=msg,
                                            date_created=datetime.datetime.now())

    else:
        fichier_form = EnvoieFichier_form(request.POST, request.FILES)
        msg = request.POST['message']
        if msg != '':
            if request.POST['produit']:
                chatMessages.objects.create(user_from_id=request.POST['user_from'], user_to_id=request.POST['user_to'],
                                            message=msg, produit_id=request.POST['produit'], date_created=datetime.datetime.now())
            else:
                chatMessages.objects.create(user_from_id=request.POST['user_from'], user_to_id=request.POST['user_to'],
                                            message=msg, date_created=datetime.datetime.now())

        if request.FILES:
            images = request.FILES.getlist('photo')
            for image in images:
                chatMessages.objects.create(user_from_id=request.POST['user_from'], user_to_id=request.POST['user_to'],
                                            fichier_message=image, produit_id=request.POST['produit'],
                                            date_created=datetime.datetime.now())

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def supprime_chat(request, msg_id):
    if msg_id > 0:
        chat = chatMessages.objects.filter(id=msg_id)
        chat.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))