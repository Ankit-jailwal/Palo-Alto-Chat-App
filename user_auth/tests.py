from rest_framework.test import APITestCase
from .views import get_random, get_access_token, get_refresh_token
from .models import CustomUser, UserProfile
from chat_control.tests import create_image, SimpleUploadedFile


class TestGenericFunctions(APITestCase):

    def test_get_random(self):

        rand1 = get_random(10)
        rand2 = get_random(10)
        rand3 = get_random(15)

        # check that we are getting a result
        self.assertTrue(rand1)

        # check that rand1 is not equal to rand2
        self.assertNotEqual(rand1, rand2)

        # check that the length of result is what is expected
        self.assertEqual(len(rand1), 10)
        self.assertEqual(len(rand3), 15)

    def test_get_access_token(self):
        payload = {
            "id": 1
        }

        token = get_access_token(payload)

        # check that we obtained a result
        self.assertTrue(token)

    def test_get_refresh_token(self):

        token = get_refresh_token()

        # check that we obtained a result
        self.assertTrue(token)


class TestAuth(APITestCase):
    login_url = "/user/login"
    register_url = "/user/register"
    refresh_url = "/user/refresh"

    def test_register(self):
        payload = {
            "username": "ankitjailwal",
            "password": "12345",
            "email": "ankitjailwal@gmail.com"
        }

        response = self.client.post(self.register_url, data=payload)

        # check that we obtain a status of 201
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        payload = {
            "username": "ankitjailwal",
            "password": "12345",
            "email": "ankitjailwal@gmail.com"
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()
        print(result)
        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])

    def test_refresh(self):
        payload = {
            "username": "ankitjailwal",
            "password": "12345",
            "email": "ankitjailwal@gmail.com"
        }

        # register
        self.client.post(self.register_url, data=payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        refresh = response.json()["refresh"]
        print(refresh)
        # get refresh
        response = self.client.post(
            self.refresh_url, data={"refresh": refresh})
        result = response.json()

        
        # check that we obtain a status of 200
        self.assertEqual(response.status_code, 200)

        # check that we obtained both the refresh and access token
        self.assertTrue(result["access"])
        self.assertTrue(result["refresh"])


class TestUserInfo(APITestCase):
    profile_url = "/user/profile"
    file_upload_url = "/message/file-upload"
    login_url = "/user/login"

    def setUp(self):
        payload = {
            "username": "ankitjailwal",
            "password": "12345",
            "email": "ankitjailwal@gmail.com"
        }

        self.user = CustomUser.objects.create_user(**payload)

        # login
        response = self.client.post(self.login_url, data=payload)
        result = response.json()

  
        self.bearer = {
            'HTTP_AUTHORIZATION': 'Bearer {}'.format(result['access'])}

    def test_post_user_profile(self):

        payload = {
            "user_id": self.user.id,
            "first_name": "Ankit",
            "last_name": "Jailwal",
            "caption": "Being alive is different from living",
            "about": "Just vibing!"
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Ankit")
        self.assertEqual(result["last_name"], "Jailwal")
        self.assertEqual(result["user"]["username"], "ankitjailwal")

    def test_post_user_profile_with_profile_picture(self):

        # upload image
        avatar = create_image(None, 'avatar.png')
        avatar_file = SimpleUploadedFile('front.png', avatar.getvalue())
        data = {
            "file_upload": avatar_file
        }

        # processing
        response = self.client.post(
            self.file_upload_url, data=data, **self.bearer)
        result = response.json()

        payload = {
            "user_id": self.user.id,
            "first_name": "Ankit",
            "last_name": "Jailwal",
            "caption": "Being alive is different from living",
            "about": "Just vibing!",
            "profile_picture_id": result["id"]
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result["first_name"], "Ankit")
        self.assertEqual(result["last_name"], "Jailwal")
        self.assertEqual(result["user"]["username"], "ankitjailwal")
        self.assertEqual(result["profile_picture"]["id"], 1)

    def test_update_user_profile(self):
        # create profile

        payload = {
            "user_id": self.user.id,
            "first_name": "Ankit",
            "last_name": "Jailwal",
            "caption": "Being alive is different from living",
            "about": "Just vibing!"
        }

        response = self.client.post(
            self.profile_url, data=payload, **self.bearer)
        result = response.json()

        # --- created profile

        payload = {
            "first_name": "AJ",
            "last_name": "Styles",
        }

        response = self.client.patch(
            self.profile_url + f"/{result['id']}", data=payload, **self.bearer)
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["first_name"], "AJ")
        self.assertEqual(result["last_name"], "Styles")
        self.assertEqual(result["user"]["username"], "ankitjailwal")

    def test_user_search(self):

        UserProfile.objects.create(user=self.user, first_name="Ankit", last_name="Jailwal",
                                   caption="live is all about living", about="I'm a student")

        user2 = CustomUser.objects.create_user(
            username="tester", password="tester123", email="kacha@gmail.com")
        UserProfile.objects.create(user=user2, first_name="Kacha", last_name="Mango",
                                   caption="it's all about testing", about="I'm a student")

        user3 = CustomUser.objects.create_user(
            username="vasman", password="vasman123", email="adefemi@yahoo.com2")
        UserProfile.objects.create(user=user3, first_name="Bluah", last_name="Rey",
                                   caption="it's all about testing", about="I'm a student")

        # test keyword = adefemi oseni
        url = self.profile_url + "?keyword=adefemi oseni"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 0)

        # test keyword = ade
        url = self.profile_url + "?keyword=ade"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[1]["user"]["username"], "vasman")

        # test keyword = vester
        url = self.profile_url + "?keyword=vester"

        response = self.client.get(url, **self.bearer)
        result = response.json()["results"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["user"]["username"], "tester")
