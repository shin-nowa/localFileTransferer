import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from .forms import ProfilePictureForm
from .models import Profile
from gerenciador.models import TransferLog
from django.apps import apps
from django.db.models import Sum

def human_readable(bytes_amount):
    try:
        b = float(bytes_amount)
    except Exception:
        b = 0.0
    
    if b < 1024**2: # Menor que 1 MB
        return f"{b/1024:.2f} KB"
    elif b < 1024**3: # Menor que 1 GB
        return f"{b/1024**2:.2f} MB"
    else: # Gigabytes
        return f"{b/1024**3:.2f} GB" 
@login_required
def profile_view(request):
    profile = request.user.profile
    """
    View para a página /profile.
    - Exibe nome do usuário.
    - Exibe foto atual (ou imagem padrão em static/assets/default-user.png).
    - Aceita upload de nova foto (validação via ProfilePictureForm).
    - Calcula estatísticas agregadas de upload/download com base em modelos existentes
      de transferência de arquivos (procura por nomes comuns).
    """
    user_logs = TransferLog.objects.filter(user=request.user).order_by('-timestamp')
    
    # Contagens das transferências

    user = request.user

    # obtém/cria o profile do usuário (safety)
    profile, _ = Profile.objects.get_or_create(user=user)

    upload_error = None
    if request.method == "POST":
        form = ProfilePictureForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            # remover imagem antiga (opcional)
            if profile.profile_picture:
                try:
                    old_path = profile.profile_picture.path
                    if os.path.exists(old_path):
                        os.remove(old_path)
                except Exception:
                    # não falha o processo caso não seja possível remover
                    pass
            # salvar nova imagem
            profile.profile_picture = image
            profile.save()
            # redireciona para GET para evitar reenvio de formulário
            return redirect(reverse('profiles:profile'))
        else:
            upload_error = form.errors.as_text()
    else:
        form = ProfilePictureForm()

    # URL da imagem a ser exibida: se não existir, usar estática default
    if profile.profile_picture:
        # Em produção, use serviço de arquivos (S3, etc.). Aqui usamos MEDIA_URL.
        profile_image_url = profile.profile_picture.url
    else:
        profile_image_url = settings.STATIC_URL + 'assets/default-user.png'
        
    upload_count = user_logs.filter(action='UPLOAD').count()
    download_count = user_logs.filter(action='DOWNLOAD').count()
    
    total_upload_bytes = user_logs.filter(action='UPLOAD').aggregate(total=Sum('file_size'))['total'] or 0
    total_download_bytes = user_logs.filter(action='DOWNLOAD').aggregate(total=Sum('file_size'))['total'] or 0
    
    context = {
        'profile': profile,
        'logs': user_logs,
        'upload_count': upload_count,
        'download_count': download_count,
        'user_full_name': user.get_full_name() or user.username,
        'profile_image_url': profile_image_url,
        'form': form,
        'upload_error': upload_error,
        'total_upload_human': human_readable(total_upload_bytes),
        'total_download_human': human_readable(total_download_bytes),
    }

    return render(request, 'profiles/profile.html', context)
