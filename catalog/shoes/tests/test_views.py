import pytest
from decimal import Decimal

from django.urls import reverse as r
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status

from shoes.models import Shoes, Images
from .factories import ShoesFactory, ImagesFactory


@pytest.mark.django_db
class TestShoesViews:

    def setup(self):

        self.shoes = ShoesFactory(
            brand='Nike',
            model='Air',
            price=Decimal('399.99')
        )

    def test__get_shoes(
        self,
        authorized_client
    ):
        url = r('shoes:shoes')

        response = authorized_client.get(
            url,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()['data']
        assert data[0]['brand'] == self.shoes.brand
        assert data[0]['model'] == self.shoes.model
        assert data[0]['price'] == '399.99'
        assert len(data) == 1

    def test__get_shoes_with_queryset(
        self,
        authorized_client
    ):

        for i in range(1, 6):
            ShoesFactory(sku=str(i))

        url = r('shoes:shoes')

        response = authorized_client.get(
            url,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()['data']
        assert len(data) == 6

        response = authorized_client.get(
            url + '?sku=1',
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()['data']
        assert len(data) == 1

    def test__get_shoes_with_pagination(
        self,
        authorized_client
    ):

        for i in range(1, 16):
            ShoesFactory(sku=str(i))

        url = r('shoes:shoes')

        response = authorized_client.get(
            url,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['meta']['count'] == 16

        data = response.json()['data']
        assert len(data) == 10

    def test__create_new_shoes(
        self,
        authorized_client,
        shoes_payload
    ):

        url = r('shoes:shoes')

        payload = shoes_payload

        response = authorized_client.post(
            url,
            data=payload,
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()['data']
        assert payload['sku'] == data['sku']

    def test__create_new_shoes_with_invalid_payload(
        self,
        authorized_client,
        shoes_payload_invalid
    ):

        url = r('shoes:shoes')

        payload = shoes_payload_invalid

        response = authorized_client.post(
            url,
            data=payload,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test__get_shoes_with_pk(
        self,
        authorized_client
    ):

        for i in range(1, 5):
            ShoesFactory(sku=str(i))

        url = r('shoes:shoes_viewset', args=[1])
        response = authorized_client.get(
            url,
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()['data']

        assert data['brand'] == self.shoes.brand
        assert data['model'] == self.shoes.model
        assert data['price'] == '399.99'

    def test__get_shoes_not_found(
        self,
        authorized_client
    ):

        url = r('shoes:shoes_viewset', args=[198493])
        response = authorized_client.get(
            url,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test__put_shoes(
        self,
        authorized_client,
        shoes_payload
    ):

        shoes = ShoesFactory(sku='04594543')

        url = r('shoes:shoes_viewset', args=[shoes.pk])

        payload = shoes_payload

        response = authorized_client.put(
            url,
            data=payload,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()['data']
        assert payload['sku'] == data['sku']

    def test__put_shoes_with_partial_payload(
        self,
        authorized_client,
        shoes_payload_partial
    ):

        shoes = ShoesFactory(sku='04594543')

        url = r('shoes:shoes_viewset', args=[shoes.pk])

        payload = shoes_payload_partial

        response = authorized_client.put(
            url,
            data=payload,
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test__put_shoes_not_found(
        self,
        authorized_client
    ):

        url = r('shoes:shoes_viewset', args=[198493])
        response = authorized_client.put(
            url,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test__patch_shoes(
        self,
        authorized_client,
        shoes_payload_partial
    ):

        shoes = ShoesFactory(stock=0)

        url = r('shoes:shoes_viewset', args=[shoes.pk])

        payload = shoes_payload_partial

        response = authorized_client.patch(
            url,
            data=payload,
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK

        data = response.json()['data']
        assert data['stock'] == 33

    def test__patch_shoes_not_found(
        self,
        authorized_client
    ):

        url = r('shoes:shoes_viewset', args=[198493])
        response = authorized_client.patch(
            url,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test__delete_shoes(
        self,
        authorized_client,
    ):

        shoes = ShoesFactory()
        image = ImagesFactory(shoes=shoes)

        assert Images.objects.filter(pk=image.pk).count() == 1
        assert Shoes.objects.filter(pk=shoes.pk).count() == 1

        url = r('shoes:shoes_viewset', args=[shoes.pk])
        response = authorized_client.delete(
            url,
            format='json'
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Images.objects.filter(pk=image.pk).count() == 0
        assert Shoes.objects.filter(pk=shoes.pk).count() == 0

    def test__delete_shoes_not_found(
        self,
        authorized_client
    ):

        url = r('shoes:shoes_viewset', args=[198493])
        response = authorized_client.delete(
            url,
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestShoesUploadFileViews:

    def test__upload_file(
        self,
        authorized_client,
    ):
        filename = 'upload_file.csv'
        csv_file = File(open('files/upload_file.csv', 'rb'))

        uploaded_file = SimpleUploadedFile(
            filename,
            csv_file.read(),
            content_type='multipart/form-data',
        )

        url = r('shoes:shoes_import')
        data = {
            'file': uploaded_file,
        }

        headers = {
            'Content-Disposition': 'attachment;filename=upload_file.csv',
        }
        response = authorized_client.post(
            url,
            data,
            headers=headers
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Shoes.objects.all().count() == 3
        assert Shoes.objects.all()[0].brand == 'adidas'
