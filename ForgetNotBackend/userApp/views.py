# -- coding: utf-8 --**
from datetime import datetime

import random

import requests
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache

from rest_framework.decorators import api_view
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

from ForgetNotBack.settings import SECRET_KEY
from .models import User, Event, Event_User_Relation, Label, Contact_Msg
from .services import create_label, delete_label, get_label, update_label, LabelSerializer, UserSerializer, create_user, \
    EventUserRelationSerializer, validate_label_owner, delete_event, update_user, get_user, \
    EventUserRelationSerializerToUserDetails, EventUserRelationSerializerToUserEventDetails
from .utils import Token, MailSender, MyResponse, send_verification_code_email, send_invite_email, send_contact_email
from django.shortcuts import render

token_confirm = Token(SECRET_KEY)


# Create your views here.


def login_out(func):
    def wrapper(request, *args, **kwargs):

        if not request.session.get('user'):
            return MyResponse(status=HTTP_401_UNAUTHORIZED, msg="have not login")
        else:
            res = func(request, *args, **kwargs)
            return res

    return wrapper


@api_view(["POST"])
def authenticate(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = User.objects.get(email=email, is_visitor=False)
    except ObjectDoesNotExist:
        return MyResponse(msg="user is not exist", status=HTTP_401_UNAUTHORIZED)

    if check_password(password, user.password):
        request.session['user'] = UserSerializer(user).data
        user.save()
        response = MyResponse(msg="login success")
    else:
        response = MyResponse(msg="password error",
                              status=HTTP_401_UNAUTHORIZED)

    return response


@api_view(["POST"])
def register(request):
    email = request.POST.get('email')
    try:
        User.objects.get(email=email, is_visitor=False)
    except ObjectDoesNotExist:
        user = request.POST.dict()
        cache_key = f"verification_code_{email}"
        stored_code = cache.get(cache_key)
        code = request.POST.get('verify_code')
        if stored_code != int(code):
            return MyResponse(status=HTTP_400_BAD_REQUEST, msg="verify code wrong")
        user['password'] = make_password(user['password'])
        del user['verify_code']
        create_user(**user)
        return MyResponse(msg="re success")
    return MyResponse(status=HTTP_401_UNAUTHORIZED, msg="user exist")


@api_view(["post"])
def create_event_view(request):
    user_id = request.session.get("user")['id']
    # try:
    #     label = Label.objects.get(owner_id=user_id, id=request.POST.get('label_id'))
    # except ObjectDoesNotExist:
    #     return MyResponse(status=HTTP_401_UNAUTHORIZED, msg="Label not belong this user")
    title = request.POST.get('title')
    startTime = datetime.fromtimestamp(
        int(request.POST.get('startDate')) / 1000)
    endTime = datetime.fromtimestamp(int(request.POST.get('endDate')) / 1000)
    description = request.POST.get('notes', "")
    label = request.POST.get('label_id')
    if request.POST.get('allDay') == "false":
        allDay = False
    else:
        allDay = True
    rRule = request.POST.get('rRule')
    exDate = request.POST.get('exDate')

    event = Event.objects.create(title=title,
                                 notes=description,
                                 startDate=startTime,
                                 endDate=endTime,
                                 allDay=allDay,
                                 rRule=rRule,
                                 exDate=exDate)

    Event_User_Relation.objects.create(
        event=event, user_id=user_id, type=0, status=1, label_id=label)

    return MyResponse(msg="Create successfully.", data=event.id)


@api_view(['POST'])
def update_user_view(request):
    user_id = request.session.get("user")['id']
    first_name = request.POST.get('firstName')
    last_name = request.POST.get('lastName')
    gender = request.POST.get('gender')
    birthday = request.POST.get('birthday')
    email = request.POST.get('email')
    user = update_user(user_id, first_name=first_name, last_name=last_name, gender=gender,
                       birthday=birthday, email=email)
    return MyResponse(UserSerializer(user).data)


@api_view(['GET'])
def get_user_view(request):
    user_id = request.session.get('user')['id']
    user = get_user(user_id)
    return MyResponse(UserSerializer(user).data)


@api_view(["get"])
def get_event_list(request):
    user_id = request.session.get('user')['id']
    label_id = request.GET.get('id')
    events = Event_User_Relation.objects.filter(
        user_id=user_id, label_id=label_id)
    e_list = [EventUserRelationSerializer(event).data for event in events]
    result = []
    for e in e_list:
        event = e['event']
        event['type'] = e['type']
        event['status'] = e['status']
        event['labelId'] = e['label']
        event['startTime'] = event['startDate']
        event['endTime'] = event['endDate']
        event.pop('startDate')
        event.pop('endDate')
        result.append(event)
    return MyResponse(data=result)


@api_view(["POST"])
def update_event_view(request):
    user_id = request.session.get('user')['id']
    title = request.POST.get('title')
    startTime = datetime.fromtimestamp(
        int(request.POST.get('startDate')) / 1000)
    endTime = datetime.fromtimestamp(int(request.POST.get('endDate')) / 1000)
    description = request.POST.get('notes', "")
    label = request.POST.get('label_id')
    if request.POST.get('allDay') == "false":
        allDay = False
    else:
        allDay = True
    rRule = request.POST.get('rRule')
    exDate = request.POST.get('exDate')
    event_id = request.POST.get('id')
    event = Event.objects.get(id=event_id)

    event.rRule = rRule
    event.allDay = allDay
    event.endDate = endTime
    event.startDate = startTime
    event.notes = description
    event.title = title
    event.exDate = exDate
    event.save()

    r = Event_User_Relation.objects.get(user_id=user_id,
                                        event_id=event_id)
    r.label_id = label
    r.save()

    return MyResponse()


@api_view(["POST"])
def delete_event_view(request):
    user_id = request.session.get('user')['id']
    event_id = request.POST.get('event_id')
    try:
        Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        return MyResponse(status=HTTP_401_UNAUTHORIZED, msg="have not permission")

    delete_event(event_id)

    return MyResponse(msg="delete success")


@api_view(['POST'])
def create_label_view(request):
    name = request.POST.get('name')
    try:
        owner_id = request.session.get("user")['id']
    except Exception as e:
        return MyResponse(HTTP_401_UNAUTHORIZED, "not login")
    color = request.POST.get('color')
    label = create_label(name=name, owner_id=owner_id, color=color)
    return MyResponse(LabelSerializer(label).data)


@api_view(['POST'])
def delete_label_view(request):
    try:
        owner_id = request.session.get("user")['id']
    except Exception as e:
        return MyResponse(HTTP_401_UNAUTHORIZED, "not login")
    label_id = request.POST.get('label_id')
    if not validate_label_owner(label_id, owner_id):
        return MyResponse(HTTP_401_UNAUTHORIZED, "label_id is not allowed for this user")
    delete_label(label_id=label_id)
    return MyResponse()


@api_view(['GET'])
def get_label_view(request):
    try:
        owner_id = request.session.get("user")['id']
    except Exception as e:
        return MyResponse(HTTP_401_UNAUTHORIZED, "not login")
    labels = get_label(owner=owner_id)
    data = [label for label in
            labels]

    serializer = LabelSerializer(data, many=True)
    return MyResponse(data=serializer.data)


@api_view(['POST'])
def update_label_view(request):
    label_id = request.POST.get('label_id')
    try:
        owner_id = request.session.get("user")['id']
    except Exception as e:
        return MyResponse(HTTP_401_UNAUTHORIZED, "not login")
    if not validate_label_owner(label_id, owner_id):
        return MyResponse(HTTP_401_UNAUTHORIZED, "label_id is not allowed for this user")
    name = request.POST.get('name')
    color = request.POST.get('color')
    owner = User.objects.get(id=owner_id) if owner_id else None
    label = update_label(label_id=label_id, name=name,
                         owner=owner, color=color)
    return MyResponse(LabelSerializer(label).data)


@api_view(['POST'])
def get_contact_view(request):
    email = request.POST.get("email")
    name = request.POST.get("name")
    message = request.POST.get("message")
    Contact_Msg.objects.create(email=email, name=name, message=message)
    send_contact_email(email=email, name=name)
    return MyResponse()


@api_view(["POST"])
def generate_verification_code(request):
    email = request.POST.get('email')
    if not email:
        return MyResponse(msg="Email is required.", status=HTTP_400_BAD_REQUEST)

    verification_code = random.randint(100000, 999999)
    cache_key = f"verification_code_{email}"
    cache.set(cache_key, verification_code,
              600)  # Store the verification code in Redis with a 60-second expiration time

    # Send the verification code to the user via email
    # (Replace this with your email sending function)
    send_verification_code_email(email, verification_code)

    return MyResponse(msg="Verification code sent.")


@api_view(["POST"])
def invite_visitor(request):
    email = request.POST.get('email')
    event_id = request.POST.get("event_id")
    host_id = request.session.get("user")['id']
    try:
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        create_user(email=email)
        user = User.objects.get(email=email)
    try:
        Event_User_Relation.objects.get(user=user, event_id=event_id)
        return MyResponse(status=HTTP_401_UNAUTHORIZED, msg="user have been invited")
    except ObjectDoesNotExist:
        label = Label.objects.get(owner=user)
        relation = Event_User_Relation.objects.create(event_id=event_id,
                                                      user=user,
                                                      type=1,
                                                      status=0,
                                                      label=label)
        event = Event.objects.get(id=event_id)
        host = User.objects.get(id=host_id)
        send_invite_email(email=email, event=event, user=host, rel=relation)
        return MyResponse(data=UserSerializer(user).data)


@api_view(['GET'])
def accept_invite(request):
    rel_id = request.GET.get('ref_id')
    rel = Event_User_Relation.objects.get(id=rel_id)
    event = Event.objects.get(id=rel.event_id)
    context = {
        'event_title': event.title,
        'start_time': event.startDate,
        'end_time': event.endDate,
        'notes': event.notes,
    }
    rel.status = 1
    rel.save()
    return render(request, 'accept_invitation.html', context)


@api_view(['GET'])
def reject_invite(request):
    rel_id = request.GET.get('ref_id')
    rel = Event_User_Relation.objects.get(id=rel_id)
    rel.status = 2
    rel.save()
    return render(request, 'decline_invitation.html')


@api_view(["GET"])
def invite_list(request):
    event_id = request.GET.get("event_id")
    host_id = request.session.get("user")['id']
    rel = Event_User_Relation.objects.filter(event_id=event_id).exclude(user_id=host_id)
    result = [EventUserRelationSerializerToUserDetails(r).data for r in rel]
    return MyResponse(data=result)


@api_view(["GET"])
def get_event_by_ref(request):
    ref_id = request.GET.get("ref_id")
    try:
        ref = Event_User_Relation.objects.get(id=ref_id)
        host_event = Event_User_Relation.objects.get(event_id=ref.event_id, type=0)
        host = User.objects.get(id=host_event.user_id)

        result = {
            "user": UserSerializer(host).data,
            "ref": EventUserRelationSerializerToUserEventDetails(ref).data
        }
    except ObjectDoesNotExist:
        return MyResponse(msg="ref not exist", status=HTTP_401_UNAUTHORIZED)

    return MyResponse(data=result)
