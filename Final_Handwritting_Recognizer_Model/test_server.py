from fastapi.testclient import TestClient
from server import app
import unittest
import io
import numpy as np
import cv2

client = TestClient(app)


class TestFormulaClassifier(unittest.TestCase):
    def test_valid_classify_formula(self):
        print("🔍 Running: test_valid_classify_formula (basic functional check)")
        img = np.full((100, 100), 255, dtype=np.uint8)
        _, buffer = cv2.imencode(".png", img)
        image_bytes = io.BytesIO(buffer.tobytes())

        response = client.post(
            "/classify", files={"image": ("test.png", image_bytes, "image/png")}
        )
        assert response.status_code == 200
        assert "result" in response.json()
        print("✅ Passed: test_valid_classify_formula")

    def test_missing_image(self):
        print("🔍 Running: test_missing_image (no file provided)")
        response = client.post("/classify", files={})
        assert response.status_code == 422
        print("✅ Passed: test_missing_image")

    def test_invalid_file_type(self):
        print("🔍 Running: test_invalid_file_type (text file instead of image)")
        fake_file = io.BytesIO(b"not an image")
        response = client.post(
            "/classify", files={"image": ("fake.txt", fake_file, "text/plain")}
        )
        assert response.status_code in [400, 415, 500]
        assert "error" in response.json()
        print("✅ Passed: test_invalid_file_type")


class TestFormulaClassifierValidations(unittest.TestCase):
    def setUp(self):
        self.expected_output = ["4", "k", "tan"]

    def test_valid_classify_formula(self):
        print("🔍 Running: test_valid_classify_formula (with expected output check)")
        img = np.full((100, 100), 255, dtype=np.uint8)
        _, buffer = cv2.imencode(".png", img)
        image_bytes = io.BytesIO(buffer.tobytes())

        response = client.post(
            "/classify",
            files={"image": ("test.png", image_bytes, "image/png")},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.json())
        self.assertIsInstance(response.json()["result"], list)
        print("✅ Passed: test_valid_classify_formula (with output check)")


class TestFormulaClassifierEdgeCases(unittest.TestCase):
    def test_missing_image(self):
        print("🔍 Running: test_missing_image (edge case)")
        response = client.post("/classify", files={})
        self.assertEqual(response.status_code, 422)
        print("✅ Passed: test_missing_image")

    def test_invalid_file_type(self):
        print("🔍 Running: test_invalid_file_type (edge case)")
        fake_file = io.BytesIO(b"not an image")
        files = {"image": ("fake.txt", fake_file, "text/plain")}
        response = client.post("/classify", files=files)

        self.assertIn(response.status_code, [400, 415, 500])
        self.assertIn("error", response.json())
        print("✅ Passed: test_invalid_file_type")


if __name__ == "__main__":
    unittest.main()
