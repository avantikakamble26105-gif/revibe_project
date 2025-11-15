from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import  login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, GeneratePlaylistForm, JournalForm

from .models import Playlist, Song, Journal
import random
import os
from django.conf import settings
STATIC_AUDIO = ['sample1.mp3','sample2.mp3','sample3.mp3']
def index(request):
    featured = Playlist.objects.all().order_by('id')[:4]
    return render(request, 'revibe_app/index.html', {'featured': featured})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        if 'next' in request.GET:
            messages.info(request, 'Please log in to continue.')
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
@login_required
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

            approx_len = 3  # each song ~3 min
            count = max(1, duration // approx_len)

            available_playlists = list(Playlist.objects.filter(mood__iexact=mood))

            if available_playlists:
                chosen = random.choice(available_playlists)
                results = chosen.songs.all()[:count]
                playlist_title = chosen.title
                playlist_cover = chosen.cover  
            else:
                messages.error(request, f"No playlists found for mood '{mood}'")

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
        song_ids = request.POST.getlist('songs')   # get selected songs from form
        songs = Song.objects.filter(id__in=song_ids)
        p.songs.set(songs)
        p.save()
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
@login_required
def journal_view(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.user = request.user
            journal.save()
            messages.success(request, 'Your journal entry has been saved.')
            return redirect('journal')
    else:
        form = JournalForm()

    journals = Journal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'revibe_app/journal.html', {'form': form, 'journals': journals})
@login_required
def profile_view(request):
    playlists = Playlist.objects.filter(created_by=request.user)
    journals = Journal.objects.filter(user=request.user)
    return render(request, 'revibe_app/profile.html', {
        'user': request.user,
        'playlists': playlists,
        'journals': journals
    })
@login_required
def users_journals(request):
    journals = Journal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'revibe_app/users_journals.html', {'journals': journals})

@login_required
def journal_edit(request, pk):
    journal = get_object_or_404(Journal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = JournalForm(request.POST, instance=journal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Journal updated successfully!')
            return redirect('users_journals')
    else:
        form = JournalForm(instance=journal)
    return render(request, 'revibe_app/journal_edit.html', {'form': form})
    

@login_required
def journal_delete(request, pk):
    journal = get_object_or_404(Journal, pk=pk, user=request.user)
    if request.method == 'POST':
        journal.delete()
        messages.success(request, 'Journal deleted successfully!')
        return redirect('users_journals')
    return render(request, 'revibe_app/journal_confirm_delete.html', {'journal': journal})

@login_required
def journal_detail(request, pk):
    journal = get_object_or_404(Journal, pk=pk, user=request.user)
    return render(request, 'revibe_app/journal_detail.html', {'journal': journal})

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        if username and email:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')

    return render(request, 'revibe_app/edit_profile.html', {'user': user})


