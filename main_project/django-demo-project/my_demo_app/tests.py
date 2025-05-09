from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import LoggedInUser, UserTextData
from django.urls import reverse
from django.test import RequestFactory

# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.common.by import By
# from selenium.webdriver import Firefox
# from selenium.webdriver.firefox.options import Options

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
        self.assertTemplateUsed(response, "my_demo_app/document_list.html")

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


class LatexEditorViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.login(username="testuser", password="testpass")
        self.document = UserTextData.objects.create(
            user=self.user, name="Test Document", text_data="Initial content"
        )

    def test_latex_editor_view_get_valid_document(self):
        response = self.client.get(reverse("latex_editor", args=[self.document.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "my_demo_app/latex_editor.html")
        self.assertContains(response, self.document.name)
        self.assertContains(response, self.document.text_data)

    def test_latex_editor_view_get_invalid_document(self):
        response = self.client.get(reverse("latex_editor", args=[999]))
        self.assertEqual(response.status_code, 302)  # Redirects to "logged_in"

    def test_latex_editor_view_post_update_document(self):
        response = self.client.post(
            reverse("latex_editor", args=[self.document.id]),
            data={"content": "Updated content", "name": "Updated Name"},
        )
        self.assertEqual(response.status_code, 200)
        self.document.refresh_from_db()
        self.assertEqual(self.document.text_data, "Updated content")
        self.assertEqual(self.document.name, "Updated Name")

    def test_latex_editor_view_post_duplicate_name(self):
        # Create another document with the same user and name
        UserTextData.objects.create(user=self.user, name="Duplicate Name")
        response = self.client.post(
            reverse("latex_editor", args=[self.document.id]),
            data={"content": "New content", "name": "Duplicate Name"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Name already in use", response.json()["error"])


# class WritepadUITests(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         opts = Options()
#         opts.headless = True
#         cls.selenium = Firefox(options=opts)
#         cls.selenium.implicitly_wait(5)

#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()

#     def setUp(self):
#         User = get_user_model()
#         self.user = User.objects.create_user("uiuser", "ui@ex.com", "pass123")
#         self.document = UserTextData.objects.create(
#             user=self.user, name="UI Test Doc", text_data="Start"
#         )

#         self.selenium.get(self.live_server_url + reverse("login"))
#         self.selenium.find_element(By.NAME, "username").send_keys("uiuser")
#         self.selenium.find_element(By.NAME, "password").send_keys("pass123")
#         self.selenium.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

#         editor_url = self.live_server_url + reverse(
#             "latex_editor", args=[self.document.id]
#         )
#         self.selenium.get(editor_url)

#     def test_clear_writepad(self):
#         # draw a little square on the canvas via JS
#         self.selenium.execute_script(
#             """
#             const c = document.getElementById('writepadCanvas');
#             const ctx = c.getContext('2d');
#             ctx.fillStyle = '#000';
#             ctx.fillRect(0,0,5,5);
#         """
#         )
#         # capture the dataURL
#         before = self.selenium.execute_script(
#             "return document.getElementById('writepadCanvas').toDataURL();"
#         )
#         self.assertTrue(before.startswith("data:image/png"))

#         # click Clear
#         self.selenium.find_element(By.ID, "clearWritepadBtn").click()

#         after = self.selenium.execute_script(
#             "return document.getElementById('writepadCanvas').toDataURL();"
#         )
#         # after should differ from before (canvas is now blank)
#         self.assertNotEqual(after, before)

#     def test_download_writepad(self):
#         # draw again
#         self.selenium.execute_script(
#             """
#             const c = document.getElementById('writepadCanvas');
#             const ctx = c.getContext('2d');
#             ctx.fillStyle = '#000';
#             ctx.fillRect(0,0,5,5);
#         """
#         )

#         self.selenium.execute_script(
#             """
#             window._dlHref = null;
#             const orig = document.createElement.bind(document);
#             document.createElement = function(tag) {
#                 const el = orig(tag);
#                 if (tag === 'a') {
#                     Object.defineProperty(el, 'click', {
#                         value: function() { window._dlHref = el.href; }
#                     });
#                 }
#                 return el;
#             };
#         """
#         )
#         self.selenium.find_element(By.ID, "downloadWritepadBtn").click()


#         href = self.selenium.execute_script("return window._dlHref;")
#         self.assertTrue(href and href.startswith("data:image/png"))
class WritepadTemplateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="wpuser", password="testpass")
        self.client.login(username="wpuser", password="testpass")
        self.doc = UserTextData.objects.create(
            user=self.user, name="Writepad Doc", text_data="Some content"
        )

    def test_writepad_canvas_is_present(self):
        resp = self.client.get(reverse("latex_editor", args=[self.doc.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="writepadCanvas"')

    def test_clear_button_exists(self):
        resp = self.client.get(reverse("latex_editor", args=[self.doc.id]))
        self.assertContains(resp, 'id="clearWritepadBtn"')
        self.assertContains(resp, ">Clear<")

    def test_download_and_upload_buttons_exist(self):
        resp = self.client.get(reverse("latex_editor", args=[self.doc.id]))
        self.assertContains(resp, 'id="downloadWritepadBtn"')
        self.assertContains(resp, ">Download PNG<")
        self.assertContains(resp, 'id="uploadWritepadBtn"')
        self.assertContains(resp, ">Upload to OCR<")
