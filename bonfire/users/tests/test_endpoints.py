from unittest.mock import patch

from django.core.cache import cache
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .. import models
from . import factories


class UserMeViewTests(APITestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-me")

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            "email": "newmail@example.com",
        }
        self.assertNotEqual(self.user.email, data["email"])
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])

    def test_destroy(self):
        password = "bolag123"
        self.user.set_password(password)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.url, data={"password": password})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(models.User.DoesNotExist):
            self.user.refresh_from_db()


class UserTokenObtainPairTests(APITestCase):
    GOOGLE_TOKEN_DATA = {
        "at_hash": "h46HpYet04rK7hLcKPO9iQ",
        "aud": "474738356780-loiphgfpim9nbp0gpvp2mvncrskstksv.apps.googleusercontent.com",
        "azp": "474738356780-loiphgfpim9nbp0gpvp2mvncrskstksv.apps.googleusercontent.com",
        "email": "appshack@appshack.se",
        "email_verified": True,
        "exp": 1709237236,
        "family_name": "App",
        "given_name": "Shack",
        "hd": "appshack.se",
        "iat": 1709233636,
        "iss": "https://accounts.google.com",
        "locale": "en",
        "name": "App Shack",
        "nonce": "zmNQ_2vPlGO2b_9IKrK65ZFDLRKIqss-ITKe5_q3Bxg",
        "picture": "https://lh3.googleusercontent.com/a/ACg8ocL8p8jepdeucKpAMvaHWnOYr6d42E9FWj1FoheXrIU8Rg=s96-c",
        "sub": "116853902888273942150",
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = factories.UserFactory(email=cls.GOOGLE_TOKEN_DATA["email"])
        cls.user.set_unusable_password()
        cls.user.save()

        cls.url = reverse("users:token_obtain_pair")

    def setUp(self):
        cache.clear()

        self.client.force_authenticate(None)

        google_verify_patcher = patch(
            "google_client.client.verify_oauth2_token", autospec=True
        )
        self.addCleanup(google_verify_patcher.stop)
        self.google_verify_mock = google_verify_patcher.start()
        self.google_verify_mock.return_value = self.GOOGLE_TOKEN_DATA.copy()

        google_validate_patcher = patch(
            "google_client.client.validate_token", autospec=True
        )
        self.addCleanup(google_validate_patcher.stop)
        self.google_validate_mock = google_validate_patcher.start()

    def test_create_not_existing(self):
        data = {"token": "token", "client_id": "client_id"}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        AccessToken(response.data["access"], verify=True)
        RefreshToken(response.data["refresh"], verify=True)

        self.google_validate_mock.assert_called_once()
        self.google_verify_mock.assert_called_once()

        user = models.User.objects.get(email=self.GOOGLE_TOKEN_DATA["email"])

        self.assertFalse(user.has_usable_password())

    def test_create_existing(self):
        data = {"token": "token", "client_id": "client_id"}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        AccessToken(response.data["access"], verify=True)
        RefreshToken(response.data["refresh"], verify=True)

        self.google_validate_mock.assert_called_once()
        self.google_verify_mock.assert_called_once()

        user = models.User.objects.get(email=self.GOOGLE_TOKEN_DATA["email"])

        self.assertFalse(user.has_usable_password())


class UserTokenRefreshTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = factories.UserFactory()
        cls.refresh = RefreshToken.for_user(cls.user)

        cls.url = reverse("users:token_refresh")

    def setUp(self):
        self.client.force_authenticate(None)

    def test_create(self):
        data = {"refresh": str(self.refresh)}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        AccessToken(response.data["access"], verify=True)

        data = {"refresh": str(self.refresh.access_token)[1:]}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_invalid_token(self):
        url = reverse("users:user-me")
        self.client.logout()

        default_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.refresh.access_token}"}
        self.client.credentials(**default_headers)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        default_headers = {
            "HTTP_AUTHORIZATION": f"Bearer {str(self.refresh.access_token)[1:]}"
        }
        self.client.credentials(**default_headers)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
