from django import forms

class ProfilePictureForm(forms.Form):
    """
    Form simples para upload de imagem de perfil.
    Faz validação de tipo MIME e tamanho (limite configurável).
    """
    image = forms.ImageField(required=True)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError("Nenhuma imagem enviada.")

        # Validação de tipo (JPG ou PNG)
        content_type = image.content_type
        valid_types = ['image/jpeg', 'image/png']
        if content_type not in valid_types:
            raise forms.ValidationError("Tipo de arquivo inválido. Use JPG ou PNG.")

        # Tamanho máximo: 5 MB (alterar se desejar)
        max_size_mb = 5
        if image.size > max_size_mb * 1024 * 1024:
            raise forms.ValidationError(f"Arquivo muito grande. Tamanho máximo: {max_size_mb} MB.")

        return image
