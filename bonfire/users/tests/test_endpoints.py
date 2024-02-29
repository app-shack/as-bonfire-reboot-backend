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
    @classmethod
    def setUpTestData(cls):
        cls.user = factories.UserFactory(password="hej123")
        cls.url = reverse("users:token_obtain_pair")

    def setUp(self):
        self.client.force_authenticate(None)

    def test_create(self):
        data = {"email": self.user.email, "password": "hej123"}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        AccessToken(response.data["access"], verify=True)
        RefreshToken(response.data["refresh"], verify=True)


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
