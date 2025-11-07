from django.apps import AppConfig

class ProfilesConfig(AppConfig):
    # Ajuste: nome do pacote corresponde ao diretório 'perfil'
    name = 'perfil'

    def ready(self):
        # Import signals so they are registered when app is ready
        import perfil.signals  # noqa: F401
