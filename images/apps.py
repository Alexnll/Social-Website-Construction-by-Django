from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    # load the signal when start the image app
    def ready(self):
        import images.signals