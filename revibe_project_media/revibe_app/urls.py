from django.urls import path
from . import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('generate/', views.generate, name='generate'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('myplaylist/', views.myplaylist, name='myplaylist'),
    path('playlist/create/', views.playlist_create, name='playlist_create'),
    path('playlist/<int:pk>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk>/edit/', views.playlist_edit, name='playlist_edit'),
    path('playlist/<int:pk>/delete/', views.playlist_delete, name='playlist_delete'),
]
