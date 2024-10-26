from uuid import uuid4
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Picture

# Create your tests here.

class ServeImageByUUIDViewsTest(TestCase):
    def setUp(self):
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake_image_data',
            content_type='image/jpeg'
        )
        self.picture = Picture.objects.create(uuid=uuid4(), image=self.image)

    def test_serve_existing_image(self):
        # successful calling an existing image(uuid)
        response = self.client.get(reverse('serve-image-by-uuid', args=[self.picture.uuid, 'jpeg']))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response['Content-Type'].startswith('image/'))

    def test_serve_non_existent_image(self):
        # failing to call not existing image(uuid)
        non_existent_uuid = uuid4()
        response = self.client.get(reverse('serve-image-by-uuid', args=[non_existent_uuid, 'jpeg']))
        self.assertEqual(response.status_code, 404)
