from django.apps import AppConfig


class ApiConfig(AppConfig):
    # default_site = 'app.admin.CustomAdminSite'
    name = 'app'
    verbose_name = 'app'

    def ready(self):
        import app.signals
