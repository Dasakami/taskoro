from django.db import models
from django.contrib.auth.models import User
from tasks.models import Task  # если у тебя есть модель Task

class NoteCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_categories')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    category = models.ForeignKey(NoteCategory, on_delete=models.SET_NULL, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)  # прикрепить к задаче опционально
    title = models.CharField(max_length=255)
    content = models.TextField()  # markdown контент
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
