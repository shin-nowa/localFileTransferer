from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    # rota vazia -> /profile/
    path('', views.profile_view, name='profile'),
]
