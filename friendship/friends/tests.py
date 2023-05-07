from rest_framework.test import APITestCase

from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from collections import OrderedDict


User = get_user_model()


class FriendShip(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='testuser1')
        cls.user1.set_password('testuser123')
        cls.friend = User.objects.create(username='testuser2')
        cls.user1.friends.add(cls.friend)
        cls.subscriber = User.objects.create(username='testuser3')
        FriendRequest.objects.create(user_from=cls.subscriber,
                                     user_to=cls.user1)
        cls.usr_is_wanted = User.objects.create(username='testuser4')
        FriendRequest.objects.create(user_from=cls.user1,
                                     user_to=cls.usr_is_wanted)
        cls.nothing_user = User.objects.create(username='testuser5')

    def test_get_status(self):
        self.client.force_authenticate(self.user1)

        with self.subTest():
            resp = self.client.get(reverse('friendship',
                                           args=(self.friend.id,)))
            self.assertEqual({'user_id': self.friend.id,
                              'status': 'friend'},
                             resp.json())

            resp = self.client.get(reverse('friendship',
                                           args=(self.subscriber.id,)))
            self.assertEqual({'user_id': self.subscriber.id,
                              'status': 'incoming_request'},
                             resp.json())

            resp = self.client.get(reverse('friendship',
                                           args=(self.usr_is_wanted.id,)))
            self.assertEqual({'user_id': self.usr_is_wanted.id,
                              'status': 'outgoing_request'},
                             resp.json())

            resp = self.client.get(reverse('friendship',
                                           args=(self.nothing_user.id,)))
            self.assertEqual({'user_id': self.nothing_user.id,
                              'status': 'nothing'},
                             resp.json())

    def test_remove_friend(self):
        friend = User.objects.create(username='testuserfriend')
        self.user1.friends.add(friend)
        self.client.force_authenticate(self.user1)
        resp = self.client.delete(reverse('friendship',
                                          args=(friend.id,)))
        self.assertEqual(resp.status_code, 204)
        self.assertSequenceEqual(self.user1.friends.filter(id=friend.id),
                                 [])


class TestFriendReqGet(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='testuser1')
        cls.user1.set_password('testuser123')
        user2 = User.objects.create(username='testuser2')
        user3 = User.objects.create(username='testuser3')
        user4 = User.objects.create(username='testuser4')
        user5 = User.objects.create(username='testuser5')
        cls.data = {
            'incoming': [
                FriendRequestSerializer(
                    FriendRequest.objects.create(user_to=cls.user1,
                                                 user_from=user2)
                ).data,
                FriendRequestSerializer(
                    FriendRequest.objects.create(user_to=cls.user1,
                                                 user_from=user3)
                ).data
            ],
            'outgoing': [
                FriendRequestSerializer(
                    FriendRequest.objects.create(user_to=user4,
                                                 user_from=cls.user1)
                ).data,
                FriendRequestSerializer(
                    FriendRequest.objects.create(user_to=user5,
                                                 user_from=cls.user1)
                ).data
            ]
        }

    def test_get_requests(self):
        self.client.force_authenticate(self.user1)
        resp = self.client.get(reverse('friend_request_list'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertCountEqual(data['incoming'], self.data['incoming'])
        self.assertCountEqual(data['outgoing'], self.data['outgoing'])


class TestFriendRequestSend(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='testuser1')
        cls.user1.set_password('testuser123')
        cls.user2 = User.objects.create(username='testuser2')
        cls.user2.set_password('testuser123')

    def test_send_friendreq(self):
        self.client.force_authenticate(self.user1)
        data = {'user_to': self.user2.id}
        resp = self.client.post(reverse('friend_request_list'),
                                 data=data)
        self.assertEqual(resp.status_code, 201)
        fr_req = FriendRequest.objects.get(user_from=self.user1,
                                           user_to=self.user2)
        self.assertEqual(fr_req.status, 'CN')

    def test_send_toself(self):
        self.client.force_authenticate(self.user1)
        data = {'user_to': self.user1.id}
        resp = self.client.post(reverse('friend_request_list'),
                                data=data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data['user_to']['message'],
                         'user cant send request to self')

    def test_user_to_is_not_provide(self):
        pass

    def test_send_to_not_existing_user(self):
        self.client.force_authenticate(self.user1)
        data = {'user_to': 155}
        resp = self.client.post(reverse('friend_request_list'),
                                data=data)
        self.assertEqual(resp.status_code, 404)

    def test_users_are_friends(self):
        self.user1.friends.add(self.user2)
        self.client.force_authenticate(self.user1)
        data = {'user_to': self.user2.id}
        resp = self.client.post(reverse('friend_request_list'),
                                data=data)
        self.assertEqual(resp.status_code, 409)
        self.assertEqual(resp.data['message'], 'users are friends')
        self.user1.friends.remove(self.user2)

    def test_incomming_rec_exist(self):
        frreq = FriendRequest.objects.create(user_to=self.user1,
                                             user_from=self.user2)
        self.client.force_authenticate(self.user1)
        data = {'user_to': self.user2.id}
        resp = self.client.post(reverse('friend_request_list'),
                                data=data)
        self.assertEqual(resp.status_code, 204)
        self.assertIn(self.user1, self.user2.friends.all())
        self.assertIn(self.user2, self.user1.friends.all())
        incoming = FriendRequest.objects.filter(user_to=self.user1,
                                                user_from=self.user2)
        outgoing = FriendRequest.objects.filter(user_to=self.user2,
                                                user_from=self.user2)
        self.assertSequenceEqual(incoming.all(), [])
        self.assertSequenceEqual(outgoing.all(), [])


class TestFriendRequestDetail(APITestCase):
    pass


class TestFriendRequestAccepter(APITestCase):
    pass