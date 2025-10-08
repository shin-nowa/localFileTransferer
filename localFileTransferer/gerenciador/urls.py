from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^upload/(?P<subpath>.*)$', views.upload_file_view, name='upload_file'),
    path('change-directory/', views.change_directory, name='change_dir'),
    
    path('', views.browse, name='browse_root'),
    path('<path:subpath>/', views.browse, name='browse_subpath'),
    path('download/file/<path:filepath>', views.download_file_view, name='download_file'),
    path('download/folder/<path:folderpath>', views.download_folder_view, name='download_folder'),
]