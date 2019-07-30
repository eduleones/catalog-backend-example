import pandas as pd
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db import IntegrityError
from django.utils import timezone

from shoes.exceptions import CsvFileFormatError, ImportCsvError


class Shoes(models.Model):

    TYPE_STYLE = (
        ('casual', 'Casual'),
        ('formal', 'Social'),
    )

    sku = models.CharField(
        unique=True,
        max_length=30,
        null=False,
        blank=False,
        db_index=True
    )
    brand = models.CharField(max_length=50, null=False)
    model = models.CharField(max_length=70, null=False)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal('00.00')
    )

    # product details
    description = models.TextField(null=True)
    main_color = models.CharField(max_length=30, null=False)
    style = models.CharField(
        max_length=10,
        choices=TYPE_STYLE,
        default='casual'
    )
    size = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(65),
            MinValueValidator(1)
        ]
    )

    # product material
    external_material = models.CharField(max_length=30, null=True)
    internal_material = models.CharField(max_length=30, null=True)
    sole_material = models.CharField(max_length=30, null=True)

    # product dimensions
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        default=Decimal('00.00')
    )  # in KG
    height = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        default=Decimal('00.00')
    )  # in meters
    width = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        default=Decimal('00.00')
    )  # in meters
    length = models.DecimalField(
        max_digits=8,
        decimal_places=3,
        default=Decimal('00.00')
    )  # in meters

    # stock
    stock = models.PositiveIntegerField(default=0)

    # express shipping
    express_shipping = models.BooleanField(default=False)

    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['brand']
        verbose_name_plural = 'shoes'

    def __str__(self):
        return self.model

    def save(self, *args, **kwargs):
        dimensions_sum = self.height + self.width + self.length
        if dimensions_sum < 10:
            self.express_shipping = True

        if not 1 <= self.size <= 65:
            raise TypeError

        return super(Shoes, self).save(*args, **kwargs)


class Images(models.Model):
    shoes = models.ForeignKey(
        Shoes,
        related_name='images',
        on_delete=models.CASCADE
    )
    image_url = models.CharField(max_length=128)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ('ordering',)

    def __str__(self):
        return self.image_url


class ImportShoes:

    def import_csv(self, csv_file):

        if not csv_file.name.endswith('csv'):
            raise CsvFileFormatError

        try:
            data = pd.read_csv(csv_file.open())

            df_records = data.to_dict('records')

            model_instances = [Shoes(
                sku=record['sku'],
                brand=record['brand'],
                model=record['model'],
                price=record['price'],
                description=record['description'],
                main_color=record['main_color'],
                style=record['style'],
                size=record['size'],
                external_material=record['external_material'],
                internal_material=record['internal_material'],
                sole_material=record['sole_material'],
                weight=record['weight'],
                height=record['height'],
                width=record['height'],
                length=record['length'],
                stock=record['stock']
            ) for record in df_records]

            Shoes.objects.bulk_create(model_instances)
            return True

        except (IntegrityError, KeyError) as error:
            raise ImportCsvError(str(error))
