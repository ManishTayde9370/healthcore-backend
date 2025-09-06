from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Patient, Doctor, PatientDoctor
from .serializers import (
    RegisterSerializer, PatientSerializer, DoctorSerializer, PatientDoctorSerializer
)
from .permissions import IsOwnerPatient

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerPatient]
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    def perform_destroy(self, instance):
        self.check_object_permissions(self.request, instance)
        return super().perform_destroy(instance)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # POST/PUT/DELETE: auth only; GET: public (as per spec)
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class MappingViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDoctorSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        # Show mappings tied to the current user's patients (privacy-friendly)
        return PatientDoctor.objects.select_related("patient", "doctor").filter(
            patient__created_by=self.request.user
        )
