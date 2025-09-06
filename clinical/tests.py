from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class Smoke(APITestCase):
    def setUp(self):
        self.username = "manish"
        self.password = "Password@123"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def auth(self):
        url = reverse("login")
        res = self.client.post(url, {"username": self.username, "password": self.password}, format="json")
        self.assertEqual(res.status_code, 200)
        return res.data["access"]

    def test_patient_flow(self):
        token = self.auth()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # create doctor
        res = self.client.post("/api/doctors/", {"name":"Gregory House","email":"g@h.com"})
        self.assertEqual(res.status_code, 201)
        doc_id = res.data["id"]

        # create patient
        res = self.client.post("/api/patients/", {"first_name":"John","age":30,"gender":"M"})
        self.assertEqual(res.status_code, 201)
        pat_id = res.data["id"]

        # mapping
        res = self.client.post("/api/mappings/", {"patient":pat_id,"doctor":doc_id})
        self.assertEqual(res.status_code, 201)

        # list patients (scoped)
        res = self.client.get("/api/patients/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)
