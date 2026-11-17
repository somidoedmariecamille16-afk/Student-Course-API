import unittest
from app import app


class StudentCourseAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")
        self.assertEqual(response.get_json()["service"], "Student Course API")

    def test_courses_endpoint_returns_six_courses(self):
        response = self.client.get("/api/courses")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["count"], 6)
        self.assertEqual(len(payload["courses"]), 6)
        for course in payload["courses"]:
            for field in ("id", "code", "name", "description"):
                self.assertIn(field, course)

    def test_course_one_endpoint(self):
        response = self.client.get("/api/courses/1")
        self.assertEqual(response.status_code, 200)
        course = response.get_json()
        self.assertEqual(course["id"], 1)
        self.assertEqual(course["code"], "CS101")

    def test_missing_course_returns_json_404(self):
        response = self.client.get("/api/courses/9999")
        self.assertEqual(response.status_code, 404)
        payload = response.get_json()
        self.assertEqual(payload["error"], "Course not found")
        self.assertIn("9999", payload["message"])

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Student Course API", response.data)
        self.assertIn(b"/api/courses/9999", response.data)

    def test_unknown_route_returns_json_404(self):
        response = self.client.get("/not-a-route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")

    def test_cors_header_is_enabled(self):
        response = self.client.get("/api/health", headers={"Origin": "https://example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Access-Control-Allow-Origin", response.headers)


if __name__ == "__main__":
    unittest.main()
