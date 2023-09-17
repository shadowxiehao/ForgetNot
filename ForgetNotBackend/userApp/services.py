from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from .models import Label, User, Event_User_Relation, Event


# User Service

# def get_user(user_id):
#     user = get_user_model()
#     try:
#         return user.objects.get(id=user_id)
#     except ObjectDoesNotExist:
#         return None


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'email', 'birthday', 'gender',
                  'firstName', 'lastName', 'is_visitor')


def create_user(email, password="", birthday=None, gender="female", firstName="", lastName="", is_visitor=True):
    if password is not None:
        is_visitor = False
    user = User.objects.create(email=email,
                               password=password,
                               birthday=birthday,
                               gender=gender,
                               firstName=firstName,
                               lastName=lastName,
                               is_visitor=is_visitor)
    try:
        Label.objects.get(owner=user)
    except ObjectDoesNotExist:
        create_label(name='Default', owner_id=user.id, color='#f8e71c')


def update_user(user_id, first_name=None, last_name=None, gender=None, birthday=None, email=None, password=None,
                is_visitor=None):
    user = User.objects.get(id=user_id)
    if first_name is not None:
        user.firstName = first_name
    if last_name is not None:
        user.lastName = last_name
    if gender is not None:
        user.gender = gender
    if birthday is not None:
        user.birthday = birthday
    if email is not None:
        user.email = email
    if password is not None:
        user.password = make_password(password)
    if is_visitor is not None:
        user.is_visitor = is_visitor
    user.save()
    return user


def get_user(user_id):
    user = User.objects.get(id=user_id)
    return user


# Label service

def create_label(name, owner_id, color):
    label = Label.objects.create(name=name, owner_id=owner_id, color=color)
    return label


def delete_label(label_id):
    label = Label.objects.get(id=label_id)
    label.delete()


def get_label(label_id=None, name=None, owner=None, color=None):
    if label_id:
        label = Label.objects.get(id=label_id)
        return [label]
    else:
        query = {}
        if name:
            query['name'] = name
        if owner:
            query['owner'] = owner
        if color:
            query['color'] = color
        labels = Label.objects.filter(**query)
        return labels


def update_label(label_id, name=None, owner=None, color=None):
    label = Label.objects.get(id=label_id)
    if name is not None:
        label.name = name
    if owner is not None:
        label.owner = owner
    if color is not None:
        label.color = color
    label.save()
    return label


# Check whether the owner of the label with the given label_id matches the owner_id
def validate_label_owner(label_id, owner_id):
    labels = get_label(label_id=label_id)
    if len(labels) == 1 and labels[0].owner.id == owner_id:
        return True
    else:
        return False


class LabelSerializer(serializers.ModelSerializer):
    # owner = UserSerializer()

    class Meta:
        model = Label
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventUserRelationSerializer(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Event_User_Relation
        fields = '__all__'


class EventUserRelationSerializerToUserDetails(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Event_User_Relation
        fields = '__all__'


class EventUserRelationSerializerToUserEventDetails(serializers.ModelSerializer):
    event = EventSerializer()

    class Meta:
        model = Event_User_Relation
        fields = '__all__'


def delete_event(event_id):
    Event_User_Relation.objects.filter(event_id=event_id).delete()
    Event.objects.get(id=event_id).delete()
