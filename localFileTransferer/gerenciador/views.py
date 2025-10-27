import os
import io
import zipfile
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden, FileResponse, JsonResponse
from django.urls import reverse
from .models import TransferLog, UserProfile

def is_path_safe(path):
    base_path = os.path.realpath(settings.BASE_DIRECTORY)
    requested_path = os.path.realpath(path)
    return requested_path.startswith(base_path)
@login_required
def browse(request, subpath=''):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    base_dir_from_profile = profile.active_directory
    
    items = []
    parent_path = None
    
    if base_dir_from_profile:
        current_path = os.path.join(base_dir_from_profile, subpath)
        if not os.path.realpath(current_path).startswith(os.path.realpath(base_dir_from_profile)):
            return HttpResponseForbidden("Access denied.")

        if not os.path.isdir(current_path):
            raise Http404("Directory not found.")
        
        for item_name in os.listdir(current_path):
            item_path = os.path.join(current_path, item_name)
            is_dir = os.path.isdir(item_path)
            items.append({'name': item_name, 'is_dir': is_dir})
            
        items.sort(key=lambda item: (not item['is_dir'], item['name'].lower()))
        if subpath:
            parent_path_str = os.path.dirname(subpath.strip('/'))
            if parent_path_str:
                parent_path = parent_path_str + '/'
            else:
                parent_path = ''
    
    context = {'items': items, 'current_path': subpath, 'parent_path': parent_path, 'current_base_directory': base_dir_from_profile}
    return render(request, 'gerenciador/index.html', context)

@login_required
def change_directory(request):
    if request.method == 'POST':
        new_path = request.POST.get('new_path', '')
        if os.path.isdir(new_path):
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            profile.active_directory = new_path
            profile.save()
            
    return redirect('browse_root')

@login_required
def download_file_view(request, filepath):
    profile, created = UserProfile.objects.get_or_create(user=  request.user)
    base_dir = profile.active_directory
    full_path = os.path.join(base_dir, filepath)
    
    if not os.path.realpath(full_path).startswith(os.path.realpath(base_dir)) or not os.path.isfile(full_path):
        raise Http404('File not Found')
    TransferLog.objects.create(
        user=request.user,
        action='DOWNLOAD',
        file_name=os.path.basename(full_path), # Pega só o nome do arquivo
        ip_address=get_client_ip(request)
    )
    return FileResponse(open(full_path, 'rb'), as_attachment=True)

def download_folder_view(request, folderpath):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    base_dir = profile.active_directory
    full_path = os.path.join(base_dir, folderpath)
    if not os.path.realpath(full_path).startswith(os.path.realpath(base_dir)) or not os.path.isdir(full_path):
        raise Http404("Folder Not Found.")

    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(full_path):
            for file in files:
                file_path = os.path.join(root, file)
                zf.write(file_path, os.path.relpath(file_path, full_path))
    
    memory_file.seek(0)
    
    response = HttpResponse(memory_file, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(folderpath)}.zip"'
    return response

@login_required
def upload_file_view(request, subpath=''):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    base_dir = profile.active_directory
    
    upload_path = os.path.join(base_dir, subpath)
    if not os.path.realpath(upload_path).startswith(os.path.realpath(base_dir)):
        return HttpResponseForbidden("Acess Denied")

    if request.method == 'POST':
        if 'file' not in request.FILES:
            return JsonResponse({'success': False, 'error': 'No File Uploaded'}, status = 400)
        
        uploaded_file = request.FILES['file']
        try:
                with open(os.path.join(upload_path, uploaded_file.name), 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                TransferLog.objects.create(
                    user=request.user,
                    action='UPLOAD',
                    file_name=uploaded_file.name,
                    ip_address=get_client_ip(request)
                )
                return JsonResponse({
                    'success': True,
                    'filename': uploaded_file.name,
                    'is_dir': False
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    if subpath:
        return redirect(reverse('browse_subpath', kwargs={'subpath': subpath}))
    else:
        return redirect(reverse('browse_root'))
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip