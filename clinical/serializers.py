from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient, Doctor, PatientDoctor

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    tokens = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "password", "tokens")
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

class PatientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    class Meta:
        model = Patient
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at", "created_by")
    def validate_age(self, value):
        if not 1 <= value <= 130:
            raise serializers.ValidationError("Age must be between 1 and 130.")
        return value
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

class PatientDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctor
        fields = ("id", "patient", "doctor", "assigned_by", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at", "assigned_by")
    def validate(self, attrs):
        request = self.context["request"]
        patient = attrs["patient"]
        if patient.created_by_id != request.user.id:
            raise serializers.ValidationError("You can only map doctors for your own patients.")
        return attrs
    def create(self, validated_data):
        validated_data["assigned_by"] = self.context["request"].user
        return super().create(validated_data)
