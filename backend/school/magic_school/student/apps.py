from django.apps import AppConfig
# from django.conf import settings
# import tensorflow as tf 
# import os 
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # disable tensorflow warnings

class StudentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student'
    # face_net = tf.keras.models.load_model(settings.FACENET_DIR,compile=True )