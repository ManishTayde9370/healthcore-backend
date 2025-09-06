from django.conf import settings
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Patient(TimeStampedModel):
    GENDER = [("M", "Male"), ("F", "Female"), ("O", "Other")]
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100, blank=True)
    age        = models.PositiveIntegerField()
    gender     = models.CharField(max_length=1, choices=GENDER)
    address    = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patients"
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

class Doctor(TimeStampedModel):
    name           = models.CharField(max_length=150)
    specialization = models.CharField(max_length=120, blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(unique=True)
    def __str__(self):
        return f"Dr. {self.name}"

class PatientDoctor(TimeStampedModel):
    patient     = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="assignments")
    doctor      = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patients")
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        unique_together = ("patient", "doctor")
