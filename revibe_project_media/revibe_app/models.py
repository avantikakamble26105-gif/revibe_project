from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

MOOD_CHOICES = [
    ('Relaxed', 'Relaxed'),
    ('Focused', 'Focused'),
    ('Energetic', 'Energetic'),
    ('Melancholic', 'Melancholic'),
    ('Relaxed & Focused', 'Relaxed & Focused'),
    ('Energetic & Focused', 'Energetic & Focused'),
    ('Relaxed & Melancholic', 'Relaxed & Melancholic'),
]

class Song(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="songs/")
    def __str__(self):
        return self.title

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES)
    duration = models.PositiveIntegerField()
    songs = models.ManyToManyField(Song, blank=True)
    cover = models.ImageField(upload_to="playlist_cover/", blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} ({self.mood})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Contact from {self.name} <{self.email}>"

class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journals')
    title = models.CharField(max_length=200)
    content = models.TextField()
    quote = models.CharField(max_length=255, blank=True, null=True)        # 🆕 Added line
    listened_to = models.CharField(max_length=255, blank=True, null=True)  # 🆕 Added line
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"
