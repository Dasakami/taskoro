from rest_framework import viewsets, permissions
from .models import Note, NoteCategory
from .serializers import NoteSerializer, NoteCategorySerializer

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user, is_deleted=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = NoteCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return NoteCategory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
