from django.apps import AppConfig
from django.conf import settings
# import tensorflow as tf 

class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'
    # model = tf.keras.models.load_model(settings.FACENET_DIR,compile=True )
