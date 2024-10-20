from django.core.cache import cache
from typing import List
from .models import UserInfo, Picture

def is_throttled(client_ip, image_uuid):
    THROTTLE_LIMIT = 1
    THROTTLE_PERIOD = 3600

    cache_key = f'throttle-{client_ip}-{image_uuid}'
    request_count = cache.get(cache_key, 0)

    if request_count >= THROTTLE_LIMIT:
        return True

    cache.set(cache_key, request_count + 1, THROTTLE_PERIOD)
    return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def show_image(image_uuid):
    # image_uuid = image_url
    cache_key, cached_image, picture, image_path, image_format = get_image(image_uuid)

    if not cached_image:
        cache.set(cache_key, {'id':str(picture.id), 'uuid':str(picture.uuid), 'format':picture.format, 'path':picture.image.path}, 60 * 5)

    return image_path, image_format


def get_image(image_uuid, message_uuid=None, user_uuid=None):
    if message_uuid:
        cache_key = [image_uuid, message_uuid]
    elif message_uuid and user_uuid:
        cache_key = [image_uuid, message_uuid, user_uuid]
    else:
        cache_key = [image_uuid]
        
    cached_image = cache.get(cache_key[0])

    picture = cached_image['id'] if cached_image else Picture.objects.get(uuid=image_uuid)
    image_path = cached_image['path'] if cached_image else picture.image.path
    image_format = cached_image['format'] if cached_image else picture.format

    return cache_key,cached_image,picture, image_path, image_format

def add_log(request, picture: Picture, image_uuid, message_uuid=None, user_uuid=None):
    client_ip = get_client_ip(request)
    if is_throttled(client_ip, image_uuid):
        pass
    
    else:

        user_info = UserInfo.objects.create(
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            ip=client_ip,
            picture=picture,
            message_id=message_uuid,
            user_id=user_uuid,
            # time=self.data.get('time')
        )
        return user_info

        # data = {
        #     'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        #     'ip': client_ip,
        #     'picture': picture,
        #     'message_id': message_uuid,
        #     'user_id': user_uuid,
        # }

        # serializer = UserInfoSerializer(data=data)
        # if serializer.is_valid():
        #     serializer.save()
            
        # else:
        #     return JsonResponse({'status': 'error', 'errors': serializer.errors}, status=400)
        
