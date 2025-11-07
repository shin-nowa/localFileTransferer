from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='gerenciador/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('change-directory/', views.change_directory, name='change_dir'),
    
    re_path(r'^upload/(?P<subpath>.*)$', views.upload_file_view, name='upload_file'),
    path('download/file/<path:filepath>', views.download_file_view, name='download_file'),
    path('download/folder/<path:folderpath>', views.download_folder_view, name='download_folder'),
    
    #Rota de páginas
    path('about/', views.about_page, name='about'),
    path('', views.browse, name='browse_root'),
    
    path('<path:subpath>/', views.browse, name='browse_subpath'),
]