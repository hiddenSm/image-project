from django.urls import path
from .views import ImageLoaderView

urlpatterns = [
    # <uuid:uuid> ==> <image_id>:image_id>
    path('image/<str:image_url>.<format>', ImageLoaderView.as_view(), name='image-loader')
]