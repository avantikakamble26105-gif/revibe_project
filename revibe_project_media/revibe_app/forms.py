from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage
from .models import Journal
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username','email','password1','password2')
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name','email','message']
class GeneratePlaylistForm(forms.Form):
    MOODS = [('Relaxed','Relaxed'),('Focused','Focused'),('Energetic','Energetic'),('Melancholic','Melancholic')]
    mood = forms.ChoiceField(choices=MOODS)
    duration = forms.IntegerField(min_value=1, max_value=360, initial=30)
    save = forms.BooleanField(required=False)
    title = forms.CharField(required=False)
class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['title', 'content', 'quote', 'listened_to']  # 🆕 Added fields
