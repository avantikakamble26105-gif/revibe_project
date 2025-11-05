from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('generate/', views.generate, name='generate'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('myplaylist/', views.myplaylist, name='myplaylist'),
    path('playlist/create/', views.playlist_create, name='playlist_create'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk>/edit/', views.playlist_edit, name='playlist_edit'),
    path('playlist/<int:pk>/delete/', views.playlist_delete, name='playlist_delete'),
    path('journal/', views.journal_view, name='journal'),
    path('profile/', views.profile_view, name='profile'),
    path('myjournals/', views.users_journals, name='users_journals'),
    path('journal/<int:pk>/edit/', views.journal_edit, name='journal_edit'),
    path('journal/<int:pk>/delete/', views.journal_delete, name='journal_delete'),
    path('journal/<int:pk>/', views.journal_detail, name='journal_detail'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]
