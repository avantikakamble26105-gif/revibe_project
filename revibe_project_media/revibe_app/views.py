from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import  login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ContactForm, GeneratePlaylistForm
from .models import Playlist, Song
import random
import os
from django.conf import settings
STATIC_AUDIO = ['sample1.mp3','sample2.mp3','sample3.mp3']
def index(request):
    featured = Playlist.objects.all().order_by('id')[:4]
    return render(request, 'revibe_app/index.html', {'featured': featured})
def about(request):
    return render(request, 'revibe_app/about.html')
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent — thank you!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the form.')
    else:
        form = ContactForm()
    return render(request, 'revibe_app/contact.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'revibe_app/login.html', {'form': form})
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created — welcome!')
            return redirect('index')
        else:
            messages.error(request, 'Please fix the errors.')
    else:
        form = SignUpForm()
    return render(request, 'revibe_app/signup.html', {'form': form})
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('index')
import os
from django.conf import settings
def generate(request):
    results = []
    playlist_title = None
    playlist_cover = None  

    if request.method == 'POST':
        form = GeneratePlaylistForm(request.POST)
        if form.is_valid():
            mood = form.cleaned_data['mood']
            duration = form.cleaned_data['duration']
            save = form.cleaned_data['save'] 
            title = form.cleaned_data['title'] or f"{mood} — {duration}min Mix"

            # each song ~3 min
            approx_len = 3  
            count = max(1, duration // approx_len)

            # ✅ Only use playlists
            available_playlists = list(Playlist.objects.filter(mood__iexact=mood))

            if available_playlists:
                chosen = random.choice(available_playlists)
                results = list(chosen.songs.all()[:count])  # pick songs from playlist
                playlist_title = chosen.title
                playlist_cover = chosen.cover  
            else:
                messages.error(request, f"No playlists found for mood '{mood}'")

            # ✅ Save playlist if requested
            if save and results:
                if request.user.is_authenticated:
                    playlist = Playlist.objects.create(
                        title=title,
                        mood=mood,
                        duration=duration,
                        created_by=request.user,
                        cover=playlist_cover  
                    )
                    playlist.songs.set(results)
                    messages.success(request, 'Playlist saved to My Playlists.')
                else:
                    messages.error(request, 'Log in to save playlists.')
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = GeneratePlaylistForm()

    return render(request, 'revibe_app/generate.html', {
        'form': form,
        'results': results,
        'playlist_title': playlist_title,
        'playlist_cover': playlist_cover,
    })

@login_required
def myplaylist(request):
    playlists = Playlist.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'revibe_app/myplaylist.html', {'playlists': playlists})
@login_required
def playlist_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        mood = request.POST.get('mood')
        duration = request.POST.get('duration')
        songs = request.POST.get('songs')
        messages.success(request, 'Playlist created.')
        return redirect('myplaylist')
    return render(request, 'revibe_app/playlist_form.html')
@login_required
def playlist_detail(request, pk):
    p = get_object_or_404(Playlist, pk=pk)
    return render(request, 'revibe_app/playlist_detail.html', {'p': p})
@login_required
def playlist_edit(request, pk):
    p = get_object_or_404(Playlist, pk=pk)
    if p.created_by != request.user:
        messages.error(request, 'You do not have permission.')
        return redirect('myplaylist')
    if request.method == 'POST':
        p.title = request.POST.get('title')
        p.mood = request.POST.get('mood')
        p.duration = request.POST.get('duration')
        p.songs.set(Song.objects.filter(title__in=[s.strip() for s in request.POST.get('songs', '').split(',') if s.strip()]))
        messages.success(request, 'Playlist updated.')
        return redirect('playlist_detail', pk=p.pk)
    return render(request, 'revibe_app/playlist_form.html', {'p': p})
@login_required
def playlist_delete(request, pk):
    p = get_object_or_404(Playlist, pk=pk)
    if p.created_by != request.user:
        messages.error(request, 'You do not have permission.')
        return redirect('myplaylist')
    if request.method == 'POST':
        p.delete()
        messages.success(request, 'Playlist deleted.')
        return redirect('myplaylist')
    return render(request, 'revibe_app/playlist_confirm_delete.html', {'p': p})
