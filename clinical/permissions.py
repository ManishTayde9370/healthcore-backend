from rest_framework.permissions import BasePermission

class IsOwnerPatient(BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj: Patient
        return getattr(obj, "created_by_id", None) == request.user.id
