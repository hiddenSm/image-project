from django.views import View
from django.core.cache import cache
from django.http import FileResponse, Http404
from sentry_sdk import capture_exception, capture_message
import uuid

from .models import Picture
from .utils import add_log, show_image, get_image

# Create your views here.

class ImageLoaderView(View):
    def get(self, request, image_url, format=None):
        try:
            if '_' in image_url:
                image_id_parts = image_url.split('_')

                if len(image_id_parts) == 2:
                    image_uuid = image_id_parts[0]
                    message_uuid = str(uuid.UUID(image_id_parts[1]))  

                    cache_key, cached_image, picture, image_path, image_format = get_image(image_uuid, message_uuid)

                    if not cached_image:
                        cache.set(cache_key, {'id':str(picture.id), 'uuid':str(picture.uuid), 'format':picture.format, 'path':picture.image.path}, 60 * 5)

                    try:
                        add_log(request, picture, image_uuid, message_uuid)
                    except Exception as ex:
                        capture_exception(ex)
                        image_path, image_format = show_image(image_uuid)
                        pass

                elif len(image_id_parts) == 3:
                    image_uuid = image_id_parts[0]
                    message_uuid = str(uuid.UUID(image_id_parts[1])) 
                    user_uuid = str(uuid.UUID(image_id_parts[2])) 

                    cache_key, cached_image, picture, image_path, image_format = get_image(image_uuid, message_uuid, user_uuid)

                    if not cached_image:
                        cache.set(cache_key, {'id':str(picture.id), 'uuid':str(picture.uuid), 'format':picture.format, 'path':picture.image.path}, 60 * 5)

                    
                    try:
                        add_log(request, picture, image_uuid, message_uuid, user_uuid)
                    except Exception as ex:
                        capture_exception(ex)
                        image_path, image_format = show_image(image_uuid)
                        pass

            else:
                image_uuid = image_url

                cache_key, cached_image, picture, image_path, image_format = get_image(image_uuid)
         
                if not cached_image:
                    cache.set(cache_key, {'id':str(picture.id), 'uuid':str(picture.uuid), 'format':picture.format, 'path':picture.image.path}, 60 * 5)

                try:
                    add_log(request, picture, image_uuid)
                except Exception as ex:
                    capture_exception(ex)
                    image_path, image_format = show_image(image_uuid)
                    pass

        except ValueError as ev:
            capture_exception(ev)
            image_path, image_format = show_image(image_uuid)
            pass

        except Exception as ex:
            capture_exception(ex)            
            raise Http404("Image not found")

        
        return FileResponse(open(image_path, 'rb'), content_type=f'image/{image_format}')