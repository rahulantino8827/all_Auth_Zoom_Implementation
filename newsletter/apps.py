from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "newsletter"

    def ready(self):
        from scheduler_jobs import updater
        updater.start()
        return super().ready()
