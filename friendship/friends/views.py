from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from .serializers import FriendSerializer, FriendRequestSerializer
from .models import FriendRequest
from .services import (
    make_friends, stop_being_friends,
    friend_status, FriendStatus
)


User = get_user_model()


class FriendsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer

    def get_queryset(self):
        return self.request.user.friends.all()


class FriendshipDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id: int):
        other_user = get_object_or_404(User, id=user_id)
        response_data = {'user_id': user_id,
                         'status': friend_status(request.user,
                                                 other_user)[0].value}
        return Response(data=response_data)

    def delete(self, request, user_id: int):
        friend = get_object_or_404(request.user.friends, id=user_id)
        stop_being_friends(request.user, friend)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        incoming_ser = FriendRequestSerializer(request.user.incoming_requests.all(),
                                               many=True)
        outgoing_ser = FriendRequestSerializer(request.user.outgoing_requests.all(),
                                               many=True)
        return Response({'incoming': incoming_ser.data,
                         'outgoing': outgoing_ser.data})

    def post(self, request):
        data = request.data.copy()
        data['user_from'] = self.request.user.id
        ser = FriendRequestSerializer(data=data)
        ser.is_valid(raise_exception=True)
        other_user = ser.validated_data['user_to']
        fr_status, obj = friend_status(request.user, other_user)
        match fr_status:
            case FriendStatus.FRIEND:
                return Response(status=status.HTTP_409_CONFLICT,
                                data={'message': 'users are friends'})
            case FriendStatus.INC_REQ:
                make_friends(request.user, other_user, obj.first())
                return Response(status=status.HTTP_204_NO_CONTENT)
            case FriendStatus.OUT_REQ:
                request_ser = FriendRequestSerializer(obj.first())
                return Response(status=status.HTTP_200_OK,
                                data=request_ser.data)
            case FriendStatus.NOTHING:
                request_ser = FriendRequestSerializer(
                    FriendRequest.objects.create(user_from=request.user,
                                                 user_to=other_user)
                )
                return Response(status=status.HTTP_201_CREATED,
                                data=request_ser.data)


class FriendRequestDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_to: int):
        frequest_ser = FriendRequestSerializer(
            get_object_or_404(FriendRequest,
                              user_from=request.user,
                              user_to__id=user_to)
        )
        return Response(data=frequest_ser.data)

    def delete(self, request, user_to: int):
        frequest = get_object_or_404(FriendRequest,
                                     user_from=request.user,
                                     user_to__id=user_to)
        frequest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestAccepter(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_from: int):
        other_user = get_object_or_404(User, id=user_from)
        friend_request = get_object_or_404(FriendRequest,
                                           user_from=other_user,
                                           user_to=request.user)
        make_friends(request.user, other_user, friend_request)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, user_from: int):
        other_user = get_object_or_404(User, id=user_from)
        friend_request = get_object_or_404(FriendRequest,
                                           user_from=other_user,
                                           user_to=request.user)
        if friend_request.status != FriendRequest.Status.REJ:
            friend_request.status = FriendRequest.Status.REJ
            friend_request.save()
        ser = FriendRequestSerializer(friend_request)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data=ser.data)

    def delete(self, request, user_from: int):
        other_user = get_object_or_404(User, id=user_from)
        friend_request = get_object_or_404(FriendRequest,
                                           user_from=other_user,
                                           user_to=request.user)
        friend_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
