from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class BikeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bike'

    def ready(self):
        logger.info("Bike app is ready.")  # Remove database queries
