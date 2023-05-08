from enum import Enum
from django.db import transaction
from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from .models import FriendRequest


User = get_user_model()


class FriendStatus(Enum):
    NOTHING = 'nothing'
    FRIEND = 'friend'
    INC_REQ = 'incoming_request'
    OUT_REQ = 'outgoing_request'


def make_friends(first_user: User,
                 second_user: User,
                 friend_request: FriendRequest):
    with transaction.atomic():
        first_user.friends.add(second_user)
        friend_request.delete()


def stop_being_friends(first_user: User,
                       second_user: User):
    first_user.friends.remove(second_user)


def friend_status(first_user: User,
                  second_user: User | int) -> tuple[FriendStatus, None | QuerySet]:
    second_user_id = second_user if isinstance(second_user, int) else second_user.id
    friends = first_user.friends.filter(id=second_user_id)
    incoming_req = first_user.incoming_requests.filter(user_from=second_user)
    outgoing_req = first_user.outgoing_requests.filter(user_to=second_user)
    if friends:
        return FriendStatus.FRIEND, None
    if incoming_req:
        return FriendStatus.INC_REQ, incoming_req
    if outgoing_req:
        return FriendStatus.OUT_REQ, outgoing_req
    return FriendStatus.NOTHING, None
