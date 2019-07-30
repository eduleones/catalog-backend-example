from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser

from django_filters.rest_framework import DjangoFilterBackend

from shoes.models import Shoes, ImportShoes
from shoes.serializers import ShoesSerializer


class ShoesListCreateView(generics.ListCreateAPIView):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'


class ShoesViewSet(viewsets.ModelViewSet):
    queryset = Shoes.objects.all()
    serializer_class = ShoesSerializer


class ShoesImport(APIView):
    parser_classes = [FileUploadParser, MultiPartParser]

    def post(self, request, format=None):
        csv_file = request.data['file']

        ImportShoes().import_csv(csv_file)

        return Response(
            {"Success": "All records were successfully imported"},
            status=status.HTTP_201_CREATED
        )
