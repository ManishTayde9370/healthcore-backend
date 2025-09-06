from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView
from clinical.views import RegisterView, PatientViewSet, DoctorViewSet, MappingViewSet

router = DefaultRouter()
router.register(r"patients", PatientViewSet, basename="patient")
router.register(r"doctors", DoctorViewSet, basename="doctor")
router.register(r"mappings", MappingViewSet, basename="mapping")

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/login/", TokenObtainPairView.as_view(), name="login"),   # returns {access, refresh}
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API
    path("api/", include(router.urls)),

    # OpenAPI & docs (bonus polish)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularRedocView.as_view(url_name="schema"), name="docs"),
]
