from rest_framework import serializers

from shoes.models import Shoes, Images


class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images

        fields = (
            'image_url',
            'ordering',
        )

        read_only_fields = ('id', )


class ShoesSerializer(serializers.ModelSerializer):

    images = ImagesSerializer(many=True, read_only=True)

    class Meta:
        model = Shoes
        fields = '__all__'

        read_only_fields = ('id', )
