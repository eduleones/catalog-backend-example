import factory
from shoes.models import Shoes, Images


class ShoesFactory(factory.django.DjangoModelFactory):

    sku = factory.Sequence(lambda i: u'SKU {0}'.format(i))
    description = factory.Sequence(
        lambda i: u'Product {0} description'.format(i))
    sku = factory.Sequence(lambda i: u'sku {0}'.format(i))
    is_active = True

    class Meta:
        model = Shoes


class ImagesFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Images
