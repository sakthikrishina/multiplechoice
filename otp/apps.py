from django.apps import AppConfig


class OtpAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'otp_app'
    
    def ready(self):
        import otp_app.signals


path("", include("otp_app.urls")),

AUTH_USER_MODEL = 'otp_app.CustomUser'