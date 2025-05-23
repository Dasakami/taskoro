from rest_framework import serializers
from .models import Note, NoteCategory

class NoteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteCategory
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']
