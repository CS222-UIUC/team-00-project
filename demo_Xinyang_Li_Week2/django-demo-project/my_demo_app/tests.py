from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import LoggedInUser, UserTextData
from django.urls import reverse
from django.test import RequestFactory

User = get_user_model()


class ModelTests(TestCase):

    def test_logged_in_user_str(self):
        user = User.objects.create_user(username="testuser", password="testpass")
        logged_in = LoggedInUser.objects.create(user=user)
        self.assertEqual(str(logged_in), "testuser")

    def test_user_text_data_str(self):
        user = User.objects.create_user(username="testuser2", password="testpass")
        data = UserTextData.objects.create(
            user=user, name="Note", text_data="Some text"
        )
        self.assertIn("testuser2", str(data))


class ViewTests(TestCase):

    def test_root_view_no_user(self):
        response = self.client.get(reverse("root"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_demo_app/index.html")

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_demo_app/register.html")

    def test_register_view_post_valid(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirects on success

    def test_register_view_post_invalid(self):
        response = self.client.post(
            reverse("register"),
            {"username": "", "password1": "pass", "password2": "differentpass"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_demo_app/register.html")

    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_view_post_valid(self):
        User.objects.create_user(username="testuser", password="testpass")
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_invalid(self):
        response = self.client.post(
            reverse("login"), {"username": "fakeuser", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password.")

    def test_forgot_password_view_get(self):
        response = self.client.get(reverse("forgot_password"))
        self.assertEqual(response.status_code, 200)

    def test_forgot_password_view_post_valid_user(self):
        User.objects.create_user(username="forgotuser", password="testpass")
        response = self.client.post(
            reverse("forgot_password"), {"username": "forgotuser"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password reset instructions")

    def test_forgot_password_view_post_invalid_user(self):
        response = self.client.post(reverse("forgot_password"), {"username": "nouser"})
        self.assertContains(response, "Account does not exist.")

    def test_logged_in_view_get(self):
        User.objects.create_user(username="loguser", password="testpass")
        self.client.login(username="loguser", password="testpass")
        response = self.client.get(reverse("logged_in"))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        user = User.objects.create_user(username="loguser", password="testpass")
        self.client.login(username="loguser", password="testpass")
        LoggedInUser.objects.create(user=user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)


class AdditionalViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="pass")
        self.client.login(username="testuser", password="pass")

    def test_logged_in_view_post_valid(self):
        response = self.client.post(
            reverse("logged_in"),
            data={"name": "Example", "text_data": "Hello World"},
        )
        self.assertEqual(response.status_code, 302)  # Redirects after save

    def test_logged_in_view_post_invalid(self):
        response = self.client.post(
            reverse("logged_in"),
            data={"name": "", "text_data": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_demo_app/logged_in_main.html")

    def test_logout_view(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, "/")

    def test_register_post_invalid(self):
        response = self.client.post(reverse("register"), data={"username": ""})
        self.assertContains(response, "Registration failed.")

    def test_login_post_invalid(self):
        response = self.client.post(
            reverse("login"), data={"username": "x", "password": "y"}
        )
        self.assertContains(response, "Invalid username or password.")

    def test_forgot_password_view_post_invalid(self):
        response = self.client.post(
            reverse("forgot_password"), data={"username": "nobody"}
        )
        self.assertContains(response, "Account does not exist.")

    def test_root_view_logged_in_user(self):
        LoggedInUser.objects.create(user=self.user)
        response = self.client.get(reverse("root"))
        self.assertEqual(response.status_code, 302)


    def test_login_view_logs_out_existing_logged_user(self):
        existing_user = User.objects.create_user(username="olduser", password="oldpass")
        LoggedInUser.objects.create(user=existing_user)
        new_user = User.objects.create_user(username="newuser", password="newpass")
        response = self.client.post(
            reverse("login"), {"username": "newuser", "password": "newpass"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(LoggedInUser.objects.filter(user=existing_user).exists())
        self.assertTrue(LoggedInUser.objects.filter(user=new_user).exists())

    def test_demo_view(self):
        response = self.client.get(reverse("demo"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, world!"})

    def test_oauth_success_view(self):
        response = self.client.get(reverse("oauth_success"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")
