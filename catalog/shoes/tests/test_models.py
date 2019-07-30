from decimal import Decimal
import pytest

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from shoes.models import Shoes, Images, ImportShoes
from shoes.exceptions import ImportCsvError, CsvFileFormatError

from .factories import ShoesFactory, ImagesFactory


@pytest.mark.django_db
class TestShoeModels:

    def test__shoe_model(self):
        shoes = ShoesFactory(
            price=100.00
        )
        assert shoes.price == 100.00
        assert Shoes.objects.all().count() == 1

    def test__shoe_model_with_express_shipping(self):
        shoes_1 = ShoesFactory(
            height=Decimal('0.131'),
            width=Decimal('0.65'),
            length=Decimal('0.09')
        )
        shoes_2 = ShoesFactory(
            height=Decimal('3.131'),
            width=Decimal('5.65'),
            length=Decimal('4.09')
        )
        assert shoes_1.express_shipping
        assert not shoes_2.express_shipping

    def test__shoe_model_invalid_size(self):
        with pytest.raises(TypeError):
            ShoesFactory(
                price=100.00,
                size=400
            )

    def test__image_model(self):
        shoes = ShoesFactory()
        images = ImagesFactory(shoes=shoes)

        assert images.shoes == shoes
        assert Images.objects.all().count() == 1


@pytest.mark.django_db
class TestImportShoesModels:

    def test__import_csv(self):

        filename = 'upload_file.csv'
        csv_file = File(open('files/upload_file.csv', 'rb'))

        uploaded_file = SimpleUploadedFile(
            filename,
            csv_file.read(),
            content_type='multipart/form-data',
        )
        ImportShoes().import_csv(uploaded_file)

        assert Shoes.objects.all().count() == 3
        assert Shoes.objects.all()[0].brand == 'adidas'

    def test__import_csv_invalid_file(self):

        filename = 'invalid_file.csv'
        csv_file = File(open('files/invalid_file.csv', 'rb'))

        uploaded_file = SimpleUploadedFile(
            filename,
            csv_file.read(),
            content_type='multipart/form-data',
        )
        with pytest.raises(ImportCsvError):
            ImportShoes().import_csv(uploaded_file)

    def test__import_csv_invalid_file_format(self):

        filename = 'invalid_format.dat'
        csv_file = File(open('files/invalid_format.dat', 'rb'))

        uploaded_file = SimpleUploadedFile(
            filename,
            csv_file.read(),
            content_type='multipart/form-data',
        )
        with pytest.raises(CsvFileFormatError):
            ImportShoes().import_csv(uploaded_file)
