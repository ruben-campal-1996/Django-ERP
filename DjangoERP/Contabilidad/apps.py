from django.apps import AppConfig


class ContabilidadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Contabilidad'

    '''def ready(self):
        import Contabilidad.signals  # Carga los signals'''
