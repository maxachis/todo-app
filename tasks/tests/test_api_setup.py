from django.test import Client, TestCase


class APICSRFTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_api_get_sets_csrf_cookie(self):
        response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", response.cookies)

    def test_api_post_requires_csrf_token(self):
        response = self.client.post("/api/csrf-check/", data={}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

    def test_api_post_accepts_valid_csrf_token(self):
        get_response = self.client.get("/api/health/")
        token = get_response.cookies["csrftoken"].value

        post_response = self.client.post(
            "/api/csrf-check/",
            data={},
            content_type="application/json",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(post_response.status_code, 200)
